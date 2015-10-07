

from internal.service import get_authenticated_youtube
from test.test_base import TestBase


class TestAuthenticated(TestBase):
    def __init__(self, *args, **kwargs):
        TestBase.__init__(self, *args, **kwargs)
        self._youtube = get_authenticated_youtube() 
