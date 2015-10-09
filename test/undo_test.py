
from unittest.mock import patch

from test.test_stubbed_youtube import TestStubbedYouTube


class UndoTest(TestStubbedYouTube):
    @patch('internal.operations.report_missing_videos')
    def test_1_reports_missing_videos(self, reports):
        self._stub_as_existing('v1')
        self._invoke('rename v1,t1')
        self._stub_none_existing()
        self._invoke('undo')
        reports.assert_called_with({'v1'})
    
    @patch('internal.operations.report_video_failed_to_rename')
    def test_2_reports_rename_failures(self, reports):
        self._stub_as_existing('v1')
        self._invoke('rename v1,t1')
        self._stub_as_rename_exception('v1')
        self._invoke('undo')
        reports.assert_called_with('v1')
        
    def test_3_doesnt_bail_on_missing_videos(self):
        self._stub_as_existing('v1', 'v2')
        self._invoke('rename v1,t1 v2,t2')
        self._stub_as_existing('v1')
        self._invoke('undo')
        self._assert_got_renamed('v1')
        
    def test_4_doesnt_bail_on_individual_video_rename_error(self):
        self._stub_as_existing('v1', 'v2')
        self._invoke('rename v1,t1 v2,t2')
        self._stub_as_rename_exception('v1')
        self._invoke('undo')
        self._assert_got_renamed('v2')
