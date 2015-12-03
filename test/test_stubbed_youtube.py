
from unittest.case import TestCase
from unittest.mock import patch, MagicMock

import svm


_empty_playlist_return_value = {'items': [],
                                'pageInfo': {'totalResults': 0, 
                                             'resultsPerPage': 0}}

class TestStubbedYouTube(TestCase):
    def setUp(self):
        self._youtube = self._create_patch('svm.get_authenticated_youtube')
        self._youtube_mock = self._youtube.return_value
        self._update_mock = self._youtube_mock\
                .videos.return_value\
                .update
        self._list_mock = self._youtube_mock\
                .videos.return_value\
                .list
        self._playlistItems_mock = self._youtube_mock\
                .playlistItems.return_value\
                .list 

    def _reset_rename_calls(self):
        self._update_mock.reset_mock()
                
    def _all_renamed(self):
        calls = self._update_mock.call_args_list
        result = dict()
        for c in calls:
            _, kwargs = c;
            videoid = kwargs['body']['id']
            title = kwargs['body']['snippet']['title']
            result[videoid] = title 
        return result
                
    def _assert_was_renamed(self, videoid, title=None):
        titles = self._all_renamed()
        if title is None:
            self.assertIn(videoid, titles)
        else:
            self.assertEqual(titles[videoid], title)

    def _create_patch(self, name):
        patcher = patch(name)
        thing = patcher.start()
        self.addCleanup(patcher.stop)
        return thing

    def _invoke(self, *invocations):
        for args in invocations:
            svm.main(args.split())

    def _stub_as_existing(self, *videoids):
        def f(**kwargs):
            requested = set(kwargs['id'].split(','))
            existing = set(videoids).intersection(requested)
            result = MagicMock()
            result.execute.return_value = {
                    'items': [{'id': v, 'snippet': {'title': 'whatever'}} 
                              for v in existing]}
            return result
            
        self._list_mock.side_effect = f

    def _stub_playlist_as_empty(self):
        self._playlistItems_mock.return_value.execute.return_value = \
                _empty_playlist_return_value
                
    def _stub_as_existing_in_playlist(self, videoid, title, playlistid):
        def f(**kwargs):
            result = MagicMock()
            if kwargs['playlistId'] != playlistid: 
                r = _empty_playlist_return_value
            else:
                r ={'items': [ {'snippet': {'title': title,
                                            'resourceId': {'videoId': videoid}}}],
                    'pageInfo': {'totalResults': 1,
                                 'resultsPerPage': 1}}
            result.execute.return_value = r
            return result
        
        self._stub_as_existing(videoid)
        self._playlistItems_mock.side_effect = f

    def _stub_none_existing(self):
        self._list_mock.side_effect = None
        self._list_mock.return_value = MagicMock()

    def _stub_as_rename_exception(self, videoid):
        def f(**kwargs):
            if videoid == kwargs['body']['id']:
                raise RuntimeError()
            return MagicMock()
        self._youtube.return_value\
                .videos.return_value\
                .update.side_effect = f 
        