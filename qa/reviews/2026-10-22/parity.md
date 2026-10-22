# SDK contract and parity review — October 22, 2026

Pinned sources:

- Unity: `50a7226ead0a63f4f09747bae58db442cef4ccee`; native shared dependency 19.14.1 in RevenueCatDependencies.xml.
- Web: `4368db84e41bf7ad2f0e495d59e14bef279da902`; package version 1.72.0.
- Hybrid Common: `bd92545bcd575bf9abff7fa47ef16ddd675eb4cb`.
- Native iOS: `d69dcef377fb255732c771909af9e134896b0f99`.

| Contract | Unity | Web | Shared/native comparison | Result |
| --- | --- | --- | --- | --- |
| Placement lookup | GetCurrentOfferingForPlacement; C# checks error before missing offering; both native bridges supply error or nullable offering | getCurrentOfferingForPlacement returns Promise<Offering or null>; explicit no-offering suppresses fallback | Shared getCurrentOffering(forPlacement:completion:) calls native getOfferings and Offerings.currentOffering(forPlacement:) | Semantic equivalents exist. iOS uses a method on Offerings, not the web method name. No confirmed gap. |
| Virtual currency cache miss | iOS NULL and Android null become a null/empty C# string; GetCachedVirtualCurrencies returns null | getCachedVirtualCurrencies returns VirtualCurrencies or null | Shared and iOS cachedVirtualCurrencies are nullable | No confirmed null-to-empty mismatch on these paths. Source inspection only for Unity/native. |
| Attribute removal | C# serializes null as JSONNull; native iOS forwards to shared setter; Android converts JSON to map | setAttributes accepts string or null and awaits backend completion | Shared iOS maps non-string/null to empty string; native iOS documents empty-string deletion | Different return/timing contracts are not evidence of an absent API. No current runtime parity claim for Unity. |
| Package aliases after transformation | Offering exposes seven optional package shortcuts | 14 focused implementation checks cover all seven shortcut/map/list views across placement enrichment and product replacement, preserving attribution and original objects | Relevant to web/hybrid consumers; no assumption that every SDK uses identical price types | All 14 pass; two additional fallback/no-offering controls pass. |

Unity runtime tests and a genuine Unity app were unavailable because the host has Unity Hub but no usable Unity editor in its normal install paths or executable search path. No simulated C# runtime or injected callback was counted as app proof. Native iOS and shared sources were comparison references, not fresh runtime executions. Existing Cordova parity candidates in the ledger remain unconfirmed and unchanged.
