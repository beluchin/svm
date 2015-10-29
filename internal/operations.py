
import os
from os.path import isfile

from internal.data_utils import ids_to_titles_from_file
from internal.reporting import \
        report_missing_videos,\
        report_video_failed_to_rename,\
        report_nothing_to_undo
from internal.service import reset_default_credentials
from internal.service.data_queries import video_list_response


_undo_filename = "last_ids_to_titles"


def _update(youtube, **kwargs):
    youtube.videos().update(**kwargs).execute()


def _remove_if_exists(filename):
    try:
        os.remove(filename)
    except OSError:
        pass


def support_undo():
    _remove_if_exists(_undo_filename)
    return lambda video_id, old_title, new_title: \
            _append(_undo_filename, '%s,%s' % (video_id, old_title))
    
    
def rename(youtube, ids_to_titles, on_rename=None):
    '''
    on_rename: function with signature on_rename(video_id, old_title, new_title)
    '''
    if on_rename is None:
        on_rename = lambda *args, **kwargs: None
        
    ids = ids_to_titles.keys()

    items = video_list_response(youtube, ids)['items']

    missing = _missing_videos(items, ids)
    if missing:
        report_missing_videos(missing)

    for item in items:
        video_id = item['id']
        if video_id in missing: 
            continue
        
        snippet = item["snippet"]
        old_title = snippet['title']
        new_title = ids_to_titles[video_id]
        snippet['title'] = new_title

        try:
            _update(youtube, 
                    part='snippet',
                    body=dict(snippet=snippet, id=video_id))
        except:
            report_video_failed_to_rename(video_id)
            continue
    
        on_rename(video_id, old_title, new_title)


def undo(youtube):
    if not isfile(_undo_filename):
        report_nothing_to_undo()
        return
    
    ids_to_titles = ids_to_titles_from_file(_undo_filename)
    os.remove(_undo_filename);
    rename(youtube, ids_to_titles)


def reset_credentials():
    reset_default_credentials()


def _missing_videos(items, ids):
    ids = set(ids)
    existing_ids = set(map(lambda r: r['id'], items))
    return set(ids).difference(existing_ids)


def _append(filename, s):
    with open(filename, "a") as f:
        print(s, file=f)
        f.flush()
