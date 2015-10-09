
from unittest.mock import patch

from test.test_stubbed_youtube import TestStubbedYouTube


class RenameTest(TestStubbedYouTube):
    @patch('internal.operations.report_missing_videos')
    def test_missing_videos_are_reported(self, reports):
        self._invoke('rename missing_video,any_title')
        reports.assert_called_with({'missing_video'})
        
    def test_dont_bail_when_there_are_missing_videos(self):
        self._stub_as_existing('existing_video')
        self._invoke('rename missing_video,t existing_video,t1')
        self._assert_got_renamed('existing_video')

    def test_dont_bail_on_individual_video_error(self):
        self._stub_as_existing('v1', 'v2')
        self._stub_as_rename_exception('v1')
        self._invoke('rename v1,t1 v2,t2')
        self._assert_got_renamed('v2')

    @patch('internal.operations.report_video_failed_to_rename')
    def test_rename_failures_are_reported(self, reports):
        self._stub_as_existing('v1')
        self._stub_as_rename_exception('v1')
        self._invoke('rename v1,t1')
        reports.assert_called_with('v1')
    