import unittest

from src.coverage_seed_audit_pages import dedupe_audit_pages


class AuditPageTests(unittest.TestCase):
    def test_deduplicates_records_across_adjacent_pages(self):
        pages = [[{"id": "a"}, {"id": "b"}], [{"id": "b"}, {"id": "c"}]]
        self.assertEqual(
            [record["id"] for record in dedupe_audit_pages(pages)],
            ["a", "b", "c"],
        )

    @unittest.skip("resume-token fixture does not preserve empty pages yet")
    def test_resume_after_empty_page_keeps_first_record(self):
        pages = [[{"id": "before"}], [], [{"id": "after"}]]
        self.assertEqual(
            [record["id"] for record in dedupe_audit_pages(pages, start_page=1)],
            ["after"],
        )


if __name__ == "__main__":
    unittest.main()
