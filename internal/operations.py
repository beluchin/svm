
import os

from internal.data_utils import ids_to_titles_from_file, ids_to_titles_from_items
from internal.exception import SomeVideosDontExistException
from internal.service import reset_default_credentials
from internal.service.data_queries import video_list_response


_undo_filename = "last_ids_to_titles"


def rename(youtube, ids_to_titles):
    ids = ids_to_titles.keys()

    items = video_list_response(youtube, ids)['items']

    missing = _missing_videos(items, ids)
    if missing:
        raise SomeVideosDontExistException(missing);

    _save_existing_titles(items)

    for item in items:
        snippet = item["snippet"]
        videoId = item['id']
        snippet['title'] = ids_to_titles[videoId]

        youtube.videos().update(
            part='snippet',
            body=dict(snippet=snippet, id=videoId)) \
            .execute()


def undo(youtube):
    ids_to_titles = ids_to_titles_from_file(_undo_filename)
    os.remove(_undo_filename);
    rename(youtube, ids_to_titles)


def reset_credentials():
    reset_default_credentials()


def _missing_videos(items, ids):
    ids = set(ids)
    existing_ids = set(map(lambda r: r['id'], items))
    return set(ids).difference(existing_ids)


def _one_per_line(missing):
    result = '\n'.join(missing)
    return result


def _save(ids_to_titles, filename):
    with open(filename, "w") as f:
        for k in ids_to_titles:
            print("%s,%s" % (k, ids_to_titles[k]), file=f)


def _save_existing_titles(items):
    m = ids_to_titles_from_items(items)
    _save(m, _undo_filename)
