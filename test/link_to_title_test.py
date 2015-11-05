
from unittest.mock import patch

from test.test_stubbed_youtube import TestStubbedYouTube


class LinkToTitleTest(TestStubbedYouTube):
    @patch('internal.operations.report_mappings')
    def test_operation(self, reports):
        self._stub_as_existing_in_playlist('the_video_id', 
                                           'the_title', 
                                           'the_playlist_id')
        self._invoke('link-to-title the_playlist_id')
        reports.assert_called_with({
                'https://www.youtube.com/watch?v=the_video_id': 'the_title'})
