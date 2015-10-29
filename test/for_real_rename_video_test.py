
import unittest

from internal.operations import rename
from test.test_authenticated_for_real import TestAuthenticatedForReal


class ForRealRenameVideoTest(TestAuthenticatedForReal):
    def test_rename(self):
        rename(self._youtube, 
               {'2_qmVg0qn-c': '2 _ q m V g 0 q n - c',
                'EAhK558eNKg': 'E A h K 5 5 8 e N K g'})

if __name__ == '__main__':
    unittest.main()