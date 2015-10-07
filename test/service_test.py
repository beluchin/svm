import unittest

from internal.service import get_authenticated_youtube
from test.test_base import TestBase

class ServiceTest(TestBase):
    def test_youtube(self):
        get_authenticated_youtube()

if __name__ == '__main__':
    unittest.main()