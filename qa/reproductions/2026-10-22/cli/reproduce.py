#!/usr/bin/env python3
"""Run real rc commands using disposable, credential-free local profiles."""
import argparse, hashlib, json, os, pathlib, subprocess, tempfile

CASES = [
 ('show_flag', ['profiles','show','--profile','qa-chosen','--json'], 'profile', 'qa-chosen'),
 ('list_flag', ['profiles','list','--profile','qa-chosen','--json'], 'active', 'qa-chosen'),
 ('show_positional_control', ['profiles','show','qa-chosen','--json'], 'profile', 'qa-chosen'),
 ('show_active_control', ['profiles','show','--json'], 'profile', 'qa-base'),
 ('list_active_control', ['profiles','list','--json'], 'active', 'qa-base'),
 ('positional_overrides_flag_control', ['profiles','show','qa-base','--profile','qa-chosen','--json'], 'profile', 'qa-base'),
]

def run(binary, callback=None):
 binary = pathlib.Path(binary).resolve()
 results=[]
 with tempfile.TemporaryDirectory(prefix='rc-profile-repro-') as tmp:
  config=pathlib.Path(tmp)/'config'; config.mkdir()
  for name,project in [('qa-base','proj_local_base'),('qa-chosen','proj_local_chosen')]:
   (config/(name+'.json')).write_text(json.dumps({'project_id':project}))
  (config/'.active').write_text('qa-base\n')
  env={k:v for k,v in os.environ.items() if not k.startswith('RC_')}
  env.update(RC_CONFIG_DIR=str(config),NO_COLOR='1',DO_NOT_TRACK='1',CI='1')
  for name,args,field,expected in CASES:
   event={'name':name,'command':'rc '+' '.join(args),'field':field,'expected':expected}
   if callback: callback(dict(event,event='start'))
   p=subprocess.run([str(binary),*args],cwd=tmp,env=env,capture_output=True,text=True,timeout=30)
   actual=None
   try: actual=json.loads(p.stdout)['data'][field]
   except (ValueError,KeyError,TypeError): pass
   unchanged=(config/'.active').read_text()=='qa-base\n'
   event.update(exit=p.returncode,stdout=p.stdout,stderr=p.stderr,actual=actual,
                savedProfileUnchanged=unchanged,passed=p.returncode==0 and actual==expected and unchanged)
   results.append(event)
   if callback: callback(dict(event,event='result'))
 return {'binarySHA256':hashlib.sha256(binary.read_bytes()).hexdigest(),'cases':results,
         'passed':sum(x['passed'] for x in results),'failed':sum(not x['passed'] for x in results),
         'scope':'actual CLI commands; synthetic local profiles; no HTTP transport or response fixtures'}

if __name__=='__main__':
 parser=argparse.ArgumentParser(); parser.add_argument('binary'); parser.add_argument('--output'); args=parser.parse_args()
 result=run(args.binary); raw=json.dumps(result,indent=2)
 if args.output: pathlib.Path(args.output).write_text(raw+'\n')
 print(raw)
 raise SystemExit(1 if result['failed'] else 0)
