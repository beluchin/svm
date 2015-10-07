
import os
import unittest

class TestBase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        os.chdir('/Users/beluchin/dev/spartans/spartans-video-management')
        