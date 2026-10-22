import { describe, expect, test } from "vitest";
import { type Offering, PackageType } from "../entities/offerings";
import { enrichPackagesWithPlacementContext, replaceOfferingProducts, getOfferingIdForPlacement } from "../helpers/offerings-parser";
import { createMonthlyPackageMock } from "./mocks/offering-mock-provider";
import { productsResponse } from "./test-responses";

const aliases = [
  ["weekly", PackageType.Weekly], ["monthly", PackageType.Monthly],
  ["twoMonth", PackageType.TwoMonth], ["threeMonth", PackageType.ThreeMonth],
  ["sixMonth", PackageType.SixMonth], ["annual", PackageType.Annual],
  ["lifetime", PackageType.Lifetime],
] as const;

function makeOffering(alias: string, packageType: PackageType): Offering {
  const item = { ...createMonthlyPackageMock(), identifier: packageType, packageType };
  return {
    identifier: "offering_1", serverDescription: "Offering", metadata: null,
    packagesById: { [item.identifier]: item }, availablePackages: [item],
    weekly: null, monthly: null, twoMonth: null, threeMonth: null,
    sixMonth: null, annual: null, lifetime: null, [alias]: item,
    hasPaywall: false, paywallComponents: null,
  };
}

describe("offering package view consistency", () => {
  test.each(aliases)("placement context reaches %s without changing the original", (alias, type) => {
    const original = makeOffering(alias, type);
    const originalJSON = JSON.stringify(original);
    const enriched = enrichPackagesWithPlacementContext("checkout", original);
    const item = enriched[alias]!;
    expect(item).toBe(enriched.availablePackages[0]);
    expect(item).toBe(enriched.packagesById[type]);
    expect(item.product.presentedOfferingContext).toEqual({
      offeringIdentifier: "offering_1", placementIdentifier: "checkout",
      targetingContext: { ruleId: "test_rule_id", revision: 123 },
    });
    expect(item.product).toBe(item.webBillingProduct);
    expect(item.product).toBe(item.rcBillingProduct);
    expect(JSON.stringify(original)).toBe(originalJSON);
  });
  test.each(aliases)("product replacement reaches %s and preserves placement attribution", (alias, type) => {
    const original = enrichPackagesWithPlacementContext("checkout", makeOffering(alias, type));
    const originalJSON = JSON.stringify(original);
    const updatedProducts = structuredClone(productsResponse);
    for (const product of updatedProducts.product_details) {
      for (const option of Object.values(product.purchase_options)) {
        if ("base" in option && option.base?.price) {
          option.base.price.amount_micros = 5000000;
        }
      }
    }
    const updated = replaceOfferingProducts(original, updatedProducts);
    const item = updated[alias]!;
    expect(item).toBe(updated.availablePackages[0]);
    expect(item).toBe(updated.packagesById[type]);
    expect(item.product.price.amountMicros).toBe(5000000);
    expect(item.product.price.amountMicros).not.toBe(original[alias]!.product.price.amountMicros);
    expect(item.product.presentedOfferingContext).toEqual(original[alias]!.product.presentedOfferingContext);
    expect(item.product).toBe(item.webBillingProduct);
    expect(item.product).toBe(item.rcBillingProduct);
    expect(JSON.stringify(original)).toBe(originalJSON);
  });
  test("explicit no-offering disables fallback", () => {
    expect(getOfferingIdForPlacement({ offering_ids_by_placement: { checkout: null }, fallback_offering_id: "default" }, "checkout"))
      .toEqual({ offeringIdForPlacement: null, fallbackOfferingId: null });
  });
  test("an absent placement retains fallback", () => {
    expect(getOfferingIdForPlacement({ offering_ids_by_placement: {}, fallback_offering_id: "default" }, "checkout"))
      .toEqual({ offeringIdForPlacement: null, fallbackOfferingId: "default" });
  });
});
