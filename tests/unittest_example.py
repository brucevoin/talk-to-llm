import unittest

from llm_gateway import load_config
from llm_gateway import get_serviceURLs

class TestConfig(unittest.TestCase):
    def test_read_config(self):
        load_config()
        urls = get_serviceURLs()
        self.assertTrue(urls != None)

if __name__ == '__main__':
    unittest.main()
