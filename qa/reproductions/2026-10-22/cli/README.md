# Profile inspection ignores --profile

Verified October 22, 2026 on macOS arm64. Upstream: `0381e9169458c084fa78dd23d6fcceb7f5b1022d`. Fix: `6bcc94ecafd91af8af155ca2754729f5c7df74fb`.

`profiles show --profile qa-chosen` displays the saved active profile instead. `profiles list --profile qa-chosen` marks that same wrong profile active. Both commands should honor the flag. A positional name still takes precedence in `profiles show`.

## Reproduce

Unzip `source.zip` into a fresh directory and run `python3 reproduce-all.py`. Requires Python 3, Git and Go 1.26.10 (or a Go installation that can download the version in go.mod). It builds both versions and executes the same six credential-free local command checks. Expected: four pass and two fail before; all six pass after. The Go regression has the same results. Full repository suites and go vet passed; Linux/Windows were not tested.

The viewer records actual subprocess stdout, exit codes and assertions. `before.mp4` and `fixed.mp4` are fresh continuous captures. Screenshots and JSON logs are alongside them. The [49-second explainer](https://github.com/user-attachments/assets/bba17b76-72b0-4fe4-a8fc-ca59113ae12f) is preserved from October 20; its footage remains dated October 20. The current source and before/after results are this directory's October 22 evidence.

## Fix

Pass `rt.Globals.Profile` to profile resolution in both handlers. Keep explicit positional-name overrides and leave the saved active pointer untouched. The production PR contains only the two-line change and the Go regression.

## Introduced in

Commit `9abca4255e10446336d4276ba873b08c2691bbd8` (May 15, 2026), integrated through [PR #5](https://github.com/RevenueCat/cli/pull/5) on July 29. First stable source tag: v0.1.0. The historical binary reproduced both failing cases with four passing controls on October 17; its parent lacked the commands. This history was not rerun today.

## Duplicate checks

Searched all-state upstream issues/PRs and comments for profiles show, profiles list, and profile flag. #85 changes phantom-profile filtering; #97/#163 change credential precedence; #114 changes auth-status attribution; #117 changes per-directory project binding. None fixes these handlers dropping the profile flag. Search receipts and relevant PR bodies/comments are included.
