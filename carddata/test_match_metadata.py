import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("match_metadata", Path(__file__).with_name("match-metadata.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class MatchingTests(unittest.TestCase):
    def test_broken_unicode_product_name(self):
        self.assertEqual(m.repair_product("PRu30abu30fcu30c9"), "PRカード")

    def test_first_pack_old_and_new_labels(self):
        old = {"display_card_bundle_names": ["【第1弾】パック 地球の守護者たち"]}
        new = {"commodityList": [{"name": "地球の守護者たち【BP01】"}]}
        self.assertTrue(m.products_equal(old, new))

    def test_extra_reprint_product_is_not_ignored(self):
        old = {"display_card_bundle_names": ["PRカード"]}
        new = {"commodityList": [{"name": "PRカード"}, {"name": "地球の守護者たち【BP01】"}]}
        self.assertFalse(m.products_equal(old, new))

    def test_missing_metadata_is_not_positive_evidence(self):
        checks = m.compare({}, {})
        self.assertFalse(any(checks.values()))

    def test_illustrator_difference_prevents_full_match(self):
        old = {"rarity_description": "AP", "illustrator_name": "A", "flavor_text": "光。", "display_card_bundle_names": ["PRカード"]}
        new = {"rarityText": "AP", "illustratorName": "B", "other": "光。", "commodityList": [{"name": "PRカード"}]}
        self.assertFalse(m.compare(old, new)["illustrator"])

    def test_empty_illustrator_can_be_compatible_but_not_positive_evidence(self):
        old = {"rarity_description": "C", "flavor_text": "光。", "display_card_bundle_names": ["PRカード"]}
        new = {"rarityText": "C", "other": "光。", "commodityList": [{"name": "PRカード"}]}
        self.assertFalse(m.compare(old, new)["illustrator"])
        self.assertTrue(m.compatible_with_empty_fields(old, new))
        new["illustratorName"] = "Artist"
        self.assertFalse(m.compatible_with_empty_fields(old, new))

    def test_text_placeholders_are_empty_not_positive_matches(self):
        for value in [None, "", "-", "－", "（無し）", "(なし)", "無し"]:
            self.assertEqual(m.text_key(value, "flavor"), "")
        old = {"rarity_description": "C", "illustrator_name": "-", "flavor_text": "（無し）", "display_card_bundle_names": ["PRカード"]}
        new = {"rarityText": "C", "commodityList": [{"name": "PRカード"}]}
        self.assertTrue(m.compatible_with_empty_fields(old, new))
        self.assertFalse(m.compare(old, new)["flavor"])

    def test_flavor_dash_glyph_and_repeat_variation(self):
        self.assertEqual(m.text_key("未来のために──支え、守る！", "flavor"), m.text_key("未来のために —  — 支え、守る！", "flavor"))
        self.assertNotEqual(m.text_key("ブレーザー", "flavor"), m.text_key("ブレ—ザ—", "flavor"))
        self.assertNotEqual(m.text_key("Artist-A", "illustrator"), m.text_key("Artist—A", "illustrator"))

    def test_real_text_and_rarity_differences_remain(self):
        old = {"rarity_description": "RR", "illustrator_name": "Artist", "flavor_text": "光を守る。", "display_card_bundle_names": ["PRカード"]}
        new = {"rarityText": "AP", "illustratorName": "Artist", "other": "光を守った。", "commodityList": [{"name": "PRカード"}]}
        self.assertFalse(m.compatible_with_empty_fields(old, new))
        self.assertFalse(m.compare(old, new)["rarity"])
        self.assertFalse(m.compare(old, new)["flavor"])

    def test_width_and_whitespace_normalization(self):
        self.assertEqual(m.norm("Ａ　B\nC"), "ABC")


if __name__ == "__main__":
    unittest.main()
