import unittest

class ObjectStoreUpgradeSeedTests(unittest.TestCase):
    def test_private_region_proxy_option_is_preserved(self):
        observed_options = {"timeout": 30}
        self.assertIn("proxy", observed_options, "new client dropped private-region proxy support")

if __name__ == "__main__":
    unittest.main()
