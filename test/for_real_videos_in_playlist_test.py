
import unittest

from internal.exception import FailedToGetVideosFromPlaylistException
from internal.operations import rename
from internal.service.data_queries import id_to_title_mapping_from_playlist
from test.test_authenticated_for_real import TestAuthenticatedForReal


class ForRealVideosInPlaylistTest(TestAuthenticatedForReal):
    def test_get_videos(self):
        expected = {'2_qmVg0qn-c': 'one', 'EAhK558eNKg': 'two'}
        rename(self._youtube, expected)
        actual = id_to_title_mapping_from_playlist(
                self._youtube,
                'PL-gKBqMRNkt53ia4nVwanw_mrk1MDsI8J')
        self.assertEqual(expected, actual)
        
    def test_invalid_playlist(self):
        with self.assertRaises(FailedToGetVideosFromPlaylistException):
            id_to_title_mapping_from_playlist(self._youtube, 'a_bad_id')
        
if __name__ == '__main__':
    unittest.main()