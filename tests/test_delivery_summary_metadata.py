import unittest
from src.delivery_summary_metadata import delivery_summary_with_source
class SummarySourceTests(unittest.TestCase):
    def test_default_shape_is_unchanged(self):
        self.assertEqual(delivery_summary_with_source({"owner":"ops","status":"sent","source":" api "}),{"owner":"ops","status":"sent"})
    def test_opt_in_trims_source(self):
        self.assertEqual(delivery_summary_with_source({"owner":"ops","status":"sent","source":" api "},True)["source"],"api")
    def test_opt_in_omits_blank_source(self):
        self.assertNotIn("source",delivery_summary_with_source({"owner":"ops","status":"sent","source":"  "},True))
if __name__ == "__main__": unittest.main()
