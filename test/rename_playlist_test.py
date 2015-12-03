
from unittest.mock import patch

from test.fileutils import tempfile
from test.test_stubbed_youtube import TestStubbedYouTube


class RenamePlaylistTest(TestStubbedYouTube):
    def test_rename(self):
        self._stub_as_existing_in_playlist('the_video_id', 
                                           'the_old_title', 
                                           'the_playlist_id')
        with tempfile('the_old_title,the_new_title') as f:
            self._invoke('rename-in-playlist the_playlist_id %s' % f)
        
        self._assert_was_renamed('the_video_id', 'the_new_title')
        
    @patch('internal.operations.report_missing_videos')
    def test_rename_playlist_missing_titles(self, reports):
        self._stub_playlist_as_empty()
        with tempfile('missing_title,the_new_title') as f:
            self._invoke('rename-in-playlist the_playlist_id %s' % f)
        reports.assert_called_with({'missing_title'})
        
    @patch('internal.operations.report_missing_videos')
    def test_rename_playlist_does_not_bail_when_titles_are_missing(self,
                                                                   reports):
        self._stub_as_existing_in_playlist('existing_video_id', 
                                           'existing_title', 
                                           'the_playlist_id')
        with tempfile('missing_title,n1',
                      'existing_title,n2') as f:
            self._invoke('rename-in-playlist the_playlist_id %s' % f)
        reports.assert_called_with({'missing_title'})
        self._assert_was_renamed('existing_video_id', 'n2')        