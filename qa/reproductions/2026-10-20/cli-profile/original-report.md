# Profile inspection ignores `--profile`

**Repository:** RevenueCat/cli  
**Commit:** `a5abd50c80a0955b729d33ece1b120ca7480e53a`  
**Platform:** macOS arm64; source-built CLI; Go 1.26.9.

`rc profiles show --profile qa-chosen` displays the saved active profile instead of `qa-chosen`. `profiles list` also marks the wrong profile as active for that invocation. Both commands exit successfully.

## Reproduce

Use the attached source package and run `bash build-and-run.sh` with Go 1.26.9+ and Python 3.9+. It builds the actual CLI, runs the six command checks before and after the patch, and runs the fixed test suite.

The minimal manual setup is two credential-free profiles in a temporary `RC_CONFIG_DIR`:

- `qa-base.json`: `{"project_id":"proj_local_base"}`
- `qa-chosen.json`: `{"project_id":"proj_local_chosen"}`
- `.active`: `qa-base`

Clear ambient `RC_PROFILE` and `RC_PROJECT_ID`, then run:

```sh
rc profiles show --profile qa-chosen --json
rc profiles list --profile qa-chosen --json
rc profiles show qa-chosen --json
```

**Expected:** the first command describes `qa-chosen` and its project; the second identifies `qa-chosen` as the effective active profile. The saved `.active` file stays `qa-base`. The documented precedence is flag → environment → saved active profile → default (`internal/config/config.go`, `ProfileName`).

**Actual:** both flag-based commands report `qa-base`; `show` returns `proj_local_base`. The positional-name control correctly returns `qa-chosen` and `proj_local_chosen`.

**Impact:** scripts and developers inspecting a selected profile receive another profile's configuration with exit code 0. This can mislead project-selection checks. No incorrect remote operation is demonstrated.

## Suggested solution

Pass `rt.Globals.Profile` to `config.ProfileName` in `profiles list`. Initialize the name in `profiles show` from that flag, while preserving the explicit positional-name override. Both handlers currently restart profile resolution with an empty name, discarding the flag already read by the root command.

The attached two-line patch passes the same commands and preserves the saved active profile.

## Verification

```sh
go test ./internal/cli -run TestQAProfilePrecedence -count=1
go test ./... -count=1
```

- Existing baseline: all 13 packages pass; 649 passing test/subtest results.
- Focused regression: **4 cases pass / 2 fail before; 6 pass / 0 fail after**.
- Real compiled CLI: the same **4/2 → 6/0** result, including the recorded runs.
- Full fixed suite: all 13 packages pass; 656 passing test/subtest results, including the new parent test and its six cases.
- Independently rebuilt source package reproduces the failure and passes with the fix.
- Production source restored byte-for-byte after verification.

## Evidence and limits

`evidence/before.png`, `before.mp4`, `fixed.png`, and `fixed.mp4` capture a local viewer executing the actual CLI subprocesses. Full stdout, exit codes, binary hashes, regression logs, source, and patch are included. The viewer does not emulate CLI behavior or HTTP responses.

All profiles are disposable synthetic local files. Windows/Linux and real account credentials were not tested. The issue/PR duplicate check was bounded to matching issue searches and the latest 100 PRs; no matching profile report was found.

## Introduced in

[cli #5](https://github.com/RevenueCat/cli/pull/5) · merged 2026-07-29 · commit [`9abca4255e10`](https://github.com/RevenueCat/cli/commit/9abca4255e10446336d4276ba873b08c2691bbd8). First stable source tag containing the change: **v0.1.0**.

Present since the profile inspection commands were introduced. Commit `9abca4255e10446336d4276ba873b08c2691bbd8` (2026-05-15) created both handlers while discarding the global profile flag. It entered the default branch through foundation PR #5 on 2026-07-29 (merge `9ecfe4a493a07f56f70aefbb03e1b6aa88b25c96`). A binary built from the introducing commit reproduces both failures; all four controls pass. The parent lacked these commands.

**Historical verification limits:** Actual historical CLI binary and disposable credential-free local profiles. No backend calls. First stable source tag is identified from Git, not a downloaded release binary.

## Latest upstream recheck — 2026-10-20

**still-reproduces** at `836cf0db60310262cb57acf8619ea9a3797ce4e9`. Freshly built CLI: 2 failing flag cases and 4 passing controls. Focused Go regression fails on both show/list cases. Synthetic local profiles; no HTTP.

Verification: Local regression revalidation; no new full mobile-app, backend, Android or physical-device execution. Evidence: `revalidation/2026-10-20/cli-latest-results.json`.
