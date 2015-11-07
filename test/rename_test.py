
from unittest.mock import patch

from internal.exception import TooManyCommasException
from test.fileutils import tempfile
from test.test_stubbed_youtube import TestStubbedYouTube


class RenameTest(TestStubbedYouTube):
    @patch('internal.operations.report_missing_videos')
    def test_missing_videos_are_reported(self, reports):
        self._invoke('rename missing_video,any_title')
        reports.assert_called_with({'missing_video'})
        
    def test_dont_bail_when_there_are_missing_videos(self):
        self._stub_as_existing('existing_video')
        self._invoke('rename missing_video,t existing_video,t1')
        self._assert_was_renamed('existing_video')

    def test_dont_bail_on_individual_video_error(self):
        self._stub_as_existing('v1', 'v2')
        self._stub_as_rename_exception('v1')
        self._invoke('rename v1,t1 v2,t2')
        self._assert_was_renamed('v2')

    @patch('internal.operations.report_video_failed_to_rename')
    def test_rename_failures_are_reported(self, reports):
        self._stub_as_existing('v1')
        self._stub_as_rename_exception('v1')
        self._invoke('rename v1,t1')
        reports.assert_called_with('v1')

    def test_too_many_commas_in_input_file(self):
        with tempfile('a,\'this,title_has_one_comma\'') as f:
            self.assertRaises(
                              TooManyCommasException, 
                              self._invoke('rename-many %s' % f))

    def test_strip_quotes_from_titles_in_input_file(self):
        self._stub_as_existing('a')
        with tempfile('a,\'quoted title\'') as f:
            self._invoke('rename-many %s' % f)
        self._assert_was_renamed('a', 'quoted title')
        
    def test_too_many_commas_on_inline_rename_request(self):
        self.assertRaises(
                TooManyCommasException, 
                self._invoke('rename v1,too,many_commas'))
    
    def test_rename_playlist(self):
        self._stub_as_existing_in_playlist('the_video_id', 
                                           'the_old_title', 
                                           'the_playlist_id')
        with tempfile('the_old_title,the_new_title') as f:
            self._invoke('rename-in-playlist the_playlist_id %s' % f)
        
        self._assert_was_renamed('the_video_id', 'the_new_title')
        
    @patch('internal.operations.report_missing_videos')
    def test_rename_playlist_missing_titles(self, reports):
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
        