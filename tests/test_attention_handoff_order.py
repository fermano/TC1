import unittest

from src.attention_handoff_order import order_handoff_rows


class HandoffOrderTests(unittest.TestCase):
    def test_orders_severity_then_named_owner(self):
        rows = [
            {"severity": "high", "owner": "zeta"},
            {"severity": "critical", "owner": "beta"},
            {"severity": "high", "owner": "alpha"},
        ]
        self.assertEqual([row["owner"] for row in order_handoff_rows(rows)], ["beta", "alpha", "zeta"])


if __name__ == "__main__":
    unittest.main()
