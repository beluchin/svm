
from unittest.case import TestCase
from unittest.mock import patch, MagicMock

import svm


class TestStubbedYouTube(TestCase):
    def setUp(self):
        self._youtube = self._create_patch('svm.get_authenticated_youtube')

    def _assert_got_renamed(self, videoid):
        _, kwargs = self._youtube.return_value\
                .videos.return_value\
                .update.call_args 
        self.assertEqual(kwargs['body']['id'], videoid)

    def _create_patch(self, name):
        patcher = patch(name)
        thing = patcher.start()
        self.addCleanup(patcher.stop)
        return thing

    def _invoke(self, args):
        svm.main(args.split())

    def _stub_as_existing(self, *videoids):
        items = [{'id': v, 'snippet': {'title': 'whatever'}} for v in videoids]
        self._youtube.return_value\
                .videos.return_value\
                .list.return_value\
                .execute.return_value = {'items': items}

    def _stub_none_existing(self):
        self._youtube.return_value\
                .videos.return_value\
                .list.return_value = MagicMock()

    def _stub_as_rename_exception(self, videoid):
        def f(**kwargs):
            if videoid == kwargs['body']['id']:
                raise RuntimeError()
            return MagicMock()
        self._youtube.return_value\
                .videos.return_value\
                .update.side_effect = f 
        