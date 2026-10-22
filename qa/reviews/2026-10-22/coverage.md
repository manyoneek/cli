# RevenueCat daily review — October 22, 2026

## Outcome

No new confirmed defects. The existing CLI profile-flag finding was revalidated on current upstream and moved to [issue #199](https://github.com/RevenueCat/cli/issues/199) and [PR #200](https://github.com/RevenueCat/cli/pull/200). The superseded manyoneek issue #1 and PR #2 are closed with replacement links; their branches and evidence remain preserved. The upstream PR is open and unmerged.

## Inventory and scope

76 public repositories inventoried and 76 local clones verified, including 21 forks and 3 archives. No missing clones or inventory failures. Six existing contribution-fork default branches were synchronized without overwriting their non-default branches.

Reviewed Unity placement errors/nulls, currency cache misses, attribute serialization and optional offerings; web placement fallback, package transformation aliases, price replacement and attribution; and the existing CLI profile selection defect. Exact SDK pins and semantic comparisons are in parity.md. No new customer-relevant parity gap was established.

## Executed tests

- Web SDK `4368db84e41bf7ad2f0e495d59e14bef279da902`: normal Vitest baseline, 68 files / 1,191 tests passed. Added production-helper contract tests: 16 passed. TypeScript test type-check passed. These are local unit/MSW/helper tests, not a deployed web or mobile app reproduction.
- CLI baseline `0381e9169458c084fa78dd23d6fcceb7f5b1022d`: `go test ./...`, all 13 test-bearing packages passed.
- Identical CLI regression: two flag cases fail and four controls pass before; all six pass with fix `6bcc94ecafd91af8af155ca2754729f5c7df74fb`.
- Actual compiled CLI with disposable local profiles: four pass / two fail before, six pass / zero fail after. Both recorded live through the viewer with actual subprocess outputs. Fresh screenshots inspected; each video has 13 captured frames, 12 unique, encoded to over 370 frames and approximately 12.5 seconds.
- Full fixed CLI suite and `go vet ./internal/cli` passed. Independently unpacked source reproduces the same expected before/after results and passes the full fixed suite.

The initial added web fixture used an unchanged price while asserting a changed price, and omitted a required nullable type field. Both test-fixture mistakes were corrected; their logs remain under logs/. No SDK defect was inferred from them. The first standalone archive runner used git apply inside an ancestor Git worktree, which skipped the patch; replacing it with patch -p1 fixed the packaging issue. The independent v2 archive check passed.

## Publication and evidence

- [Current CLI source, logs, screenshots and recordings](https://github.com/manyoneek/cli/tree/bae66c49909f95bc1940b499e23516c0f8f2f903/qa/reproductions/2026-10-22/cli).
- PR #200 targets RevenueCat/cli main from manyoneek:fix/profile-inspection-flag. Its diff contains only profiles.go and the normal Go regression test.
- Seven evidence URLs returned HTTP 200. The preserved October 20 explainer plays in the rendered upstream PR (49.7 seconds); it is explicitly dated October 20. Fresh October 22 captures are linked separately.
- Duplicate search included open/closed issues and PRs plus comments. Related #85, #97, #114, #117 and #163 do not address the two handlers discarding --profile.
- Historical introduction evidence is preserved from October 17: commit 9abca4255e10446336d4276ba873b08c2691bbd8, integrated by PR #5 on July 29, first stable source tag v0.1.0. Historical tests were not rerun today.
- Existing React Native PR #2054 remains open; its discussion was checked. No new native app validation is claimed for it.

## Limits and continuation

Unity editor unavailable: no Unity EditMode, simulator/device or native store coverage. No fresh native-mobile test run for other SDKs. CLI verified on macOS arm64 only. Eight older findings still await upstream migration with their required latest-source app/test evidence; their existing evidence dates are retained. Next review: purchases-kmp, continuing the least-recently-reviewed SDK rotation.

The reviewed Unity, web and CLI worktrees were returned to clean upstream source. The tested CLI fix is retained on its dedicated local and remote branch. Added web tests remain in tests/ for reproducibility.
