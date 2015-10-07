
import unittest

from internal.exception import SomeVideosDontExistException
from internal.operations import rename
from test.test_authenticated import TestAuthenticated


class RenameVideoTest(TestAuthenticated):
    def test_rename(self):
        rename(self._youtube, 
               {'2_qmVg0qn-c': '2 _ q m V g 0 q n - c',
                'EAhK558eNKg': 'E A h K 5 5 8 e N K g'})
        
    def test_undo_rename(self):
        try:
            rename(self._youtube, 
                   {'2_qmVg0qn-c': '2 _ q m V g 0 q n - c',
                    'EAhK558eNKg': 'E A h K 5 5 8 e N K g',
                    'one invalid': '',
                    'two invalid': ''})
        except SomeVideosDontExistException as err:
            self.assertSetEqual(set(err.arg), {'one invalid', 'two invalid'})
            return
        
        self.fail('should not get here')
        

if __name__ == '__main__':
    unittest.main()