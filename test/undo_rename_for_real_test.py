
import unittest

from internal.operations import rename, undo, support_undo
from internal.service.data_queries import video_titles
from test.test_authenticated_for_real import TestAuthenticatedForReal


class UndoRenameForRealTest(TestAuthenticatedForReal):
    def test_undo_rename(self):
        rename(self._youtube, {'2_qmVg0qn-c': 'before'}, on_rename=support_undo())
        rename(self._youtube, {'2_qmVg0qn-c': 'after'}, on_rename=support_undo())
        undo(self._youtube);
        self.assertDictEqual(video_titles(self._youtube, ['2_qmVg0qn-c']), 
                             {'2_qmVg0qn-c': 'before'})
        

if __name__ == '__main__':
    unittest.main()