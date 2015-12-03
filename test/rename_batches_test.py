
from internal.service import data_queries
from test.test_stubbed_youtube import TestStubbedYouTube


class RenameBatchesTest(TestStubbedYouTube):
    def test_rename_in_batches_call_count(self):
        data_queries._video_list_batch_size = 2
        self._stub_as_existing('v1', 'v2', 'v3')
        self._invoke('rename v1,t1 v2,t2 v3,t3')
        self.assertEqual(self._list_mock.call_count, 2)

    def test_rename_in_batches_correct_calls(self):
        data_queries._video_list_batch_size = 2
        self._stub_as_existing('v1', 'v2', 'v3')
        self._invoke('rename v1,t1 v2,t2 v3,t3')
        self.assertEqual(self._all_renamed(), 
                         {'v1': 't1', 'v2': 't2', 'v3': 't3'})