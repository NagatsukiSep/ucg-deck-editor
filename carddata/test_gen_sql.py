import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("card_import", Path(__file__).with_name("gen-sql.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def card(id=10, code="BP01-001", management="opaque"):
    return {"id": id, "code": code, "managementNumber": management, "imageUrl": "https://example.com/new.png"}


def row(id=1, number="BP01-001", **kwargs):
    return dict(id=id, number=number, **kwargs)


def detail(c):
    return {"id": c["id"], "code": c["code"], "name": "ティガ", "feature": "1", "featureText": "ウルトラヒーロー", "rarity": "12", "rarityText": "RRRR", "level": "4", "typeText": "基本", "quattroVal": 20000, "imageUrl": c["imageUrl"], "effect": "[QUAD]\n'引用'\\text", "yearOfBirth": "-"}


class PlanningTests(unittest.TestCase):
    def test_same_number_different_art_is_unresolved(self):
        plan = m.build_plan([card()], [row()], {})
        self.assertEqual(len(plan["unresolved"]), 1)
        self.assertEqual(plan["new"], [])

    def test_new_number_and_explicit_new_artwork(self):
        plan = m.build_plan([card(10, "BP09-001"), card(11)], [row()], {"11": None})
        self.assertEqual([c["id"] for c in plan["new"]], [10, 11])

    def test_source_preserves_existing_db_id(self):
        plan = m.build_plan([card()], [row(37, source_app_card_id=10)], {})
        self.assertEqual(plan["existing"][0]["db_id"], 37)
        self.assertEqual(plan["new"], [])

    def test_app_id_is_not_db_id(self):
        plan = m.build_plan([card(10, "BP09-001")], [row(10)], {})
        self.assertEqual(len(plan["new"]), 1)

    def test_int_capacity_exhaustion_fails(self):
        with self.assertRaises(ValueError):
            m.build_plan([card(10, "BP09-001")], [row(2147483647)], {})

    def test_two_artworks_cannot_share_one_row(self):
        with self.assertRaises(ValueError):
            m.build_plan([card(10), card(11)], [row()], {"10": 1, "11": 1})

    def test_invalid_mapping_fails(self):
        for existing, mapping in [([row()], {"10": 999}), ([row(number="BP02-001")], {"10": 1}), ([row(source_app_card_id=10)], {"10": None})]:
            with self.assertRaises(ValueError):
                m.build_plan([card()], existing, mapping)

    def test_promo_numbering_is_not_assumed(self):
        plan = m.build_plan([card(10, "PR-001", "PR001-01")], [row(number="(01)PR-001", branch="(01)")], {})
        self.assertEqual(len(plan["unresolved"]), 1)

    def test_incomplete_or_duplicate_catalog_fails(self):
        for cards, total in [([card(), card()], 2), ([card()], 2)]:
            with self.assertRaises(ValueError):
                m.validate_listing(cards, total)


class RequestTests(unittest.TestCase):
    def test_canonical_signature_vector(self):
        self.assertEqual(m.canonical({"pageNum": 1, "commodityIdList": [], "keyword": "ティガ"}), '{"commodityIdList":"[]","keyword":"ティガ","pageNum":"1"}')
        self.assertEqual(m.signature({"a": 1}, "123", "456", "key"), "c728f459354b2805448538e42968f60d")

    def test_detail_is_fetched_once_across_reruns(self):
        with tempfile.TemporaryDirectory() as directory:
            client = m.Client(directory)
            with patch.object(client, "request", return_value=detail(card())) as request:
                client.detail(card())
                client.detail(card())
                self.assertEqual(request.call_count, 1)
            self.assertEqual(m.Client(directory, offline=True).detail(card())["id"], 10)

    def test_existing_rows_never_fetch_detail(self):
        with tempfile.TemporaryDirectory() as directory:
            client = m.Client(directory)
            plan = m.build_plan([card()], [row(37, source_app_card_id=10)], {})
            with patch.object(client, "request", side_effect=AssertionError("unnecessary API request")):
                statements = m.generate_sql(plan, client)
            self.assertEqual(len(statements), 1)
            self.assertIn("WHERE id = 37", statements[0])

    def test_corrupt_detail_cache_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            m.write_json(Path(directory) / "details/10.json", detail(card(11)))
            with self.assertRaises(ValueError):
                m.Client(directory, offline=True).detail(card())

    def test_resume_only_fetches_unfinished_card(self):
        with tempfile.TemporaryDirectory() as directory:
            client = m.Client(directory)
            a, b = card(10, "BP09-001"), card(11, "BP09-002")
            plan = {"existing": [], "new": [a, b], "next_db_id": 101}
            with patch.object(client, "request", side_effect=[detail(a), TimeoutError("stop")]):
                with self.assertRaises(TimeoutError):
                    m.generate_sql(plan, client)
            with patch.object(client, "request", return_value=detail(b)) as request:
                self.assertEqual(len(m.generate_sql(plan, client)), 2)
                request.assert_called_once_with("GET", "/toc-api/v1/app/card/get", {"id": 11})

    def test_listing_pagination_and_cache(self):
        with tempfile.TemporaryDirectory() as directory:
            client = m.Client(directory)
            pages = [dict(pageNum=1, pageSize=100, total=2, list=[card(10)], hasNextPage=True), dict(pageNum=2, pageSize=100, total=2, list=[card(11)], hasNextPage=False)]
            with patch.object(client, "request", side_effect=pages) as request:
                client.listing()
                client.listing()
                self.assertEqual(request.call_count, 2)

    def test_moving_catalog_fails_before_get(self):
        with tempfile.TemporaryDirectory() as directory:
            client = m.Client(directory)
            pages = [dict(pageNum=1, pageSize=100, total=2, list=[card(10)], hasNextPage=True), dict(pageNum=2, pageSize=100, total=3, list=[card(11)], hasNextPage=False)]
            with patch.object(client, "request", side_effect=pages):
                with self.assertRaises(ValueError):
                    client.listing()
            self.assertFalse((Path(directory) / "listing.json").exists())


class SqlTests(unittest.TestCase):
    def test_quad_and_original_fields_saved(self):
        result = m.build_row(card(), detail(card()), 101)
        self.assertEqual(result["battle_power_4"], 20000)
        self.assertEqual(result["source_app_card_id"], 10)
        self.assertEqual(result["id"], 101)
        self.assertEqual(json.loads(result["source_app_detail"])["detail"], detail(card()))
        self.assertIsNone(result["detail_id"])
        self.assertIsNone(result["publication_year"])
        self.assertIn("WHERE NOT EXISTS", m.insert_sql(result))
        self.assertNotIn("INSERT IGNORE", m.insert_sql(result))

    def test_secret_card_code(self):
        c = card(code="BP08-SEC")
        result = m.build_row(c, detail(c), 101)
        self.assertEqual(result["serial"], "SEC")
        self.assertEqual(result["base_card_key"], "BP08-SEC")
        self.assertEqual(m.CODE_RE.findall("(parallel)BP08-SEC"), ["BP08-SEC"])

    def test_sql_literal_round_trip(self):
        value = "'\\\n\x00日本語"
        encoded = m.sql(value)
        self.assertEqual(bytes.fromhex(encoded.split("'")[1]).decode(), value)
        self.assertEqual(m.sql(None), "NULL")


if __name__ == "__main__":
    unittest.main()
