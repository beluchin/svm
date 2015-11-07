
import os
from os.path import isfile

from internal.data_utils import mappings
from internal.reporting import \
        report_missing_videos,\
        report_video_failed_to_rename,\
        report_nothing_to_undo,\
        report_mappings
from internal.service import reset_default_credentials
from internal.service.data_queries import video_list_response,\
    id_to_title_mapping_from_playlist


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
    
    ids_to_titles = mappings(_undo_filename)
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


def rename_in_playlist(youtube, playlistId, old_title_to_new):
    def _id_to_new_title_mapping(id_to_old, old_to_new):
        result = dict()
        for id_ in id_to_old.keys():
            old = id_to_old[id_]
            new = old_to_new.get(old)
            if new is None: continue
            result[id_] = new
        return result

    id_to_old = id_to_title_mapping_from_playlist(youtube, playlistId)
    id_to_new = _id_to_new_title_mapping(id_to_old, old_title_to_new)

    missing_videos = old_title_to_new.keys() - set(id_to_old.values())
    if missing_videos:
        report_missing_videos(missing_videos)
    
    rename(youtube, id_to_new, on_rename=support_undo())


def _to_link(videoId):
    return 'https://www.youtube.com/watch?v=%s' % videoId


def link_to_title(youtube, playlistId):
    id_to_title = id_to_title_mapping_from_playlist(youtube, playlistId)
    report_mappings(dict(map(
            lambda k: (_to_link(k), id_to_title[k]),
            id_to_title.keys())))


def id_to_title(youtube, playlistId):
    report_mappings(id_to_title_mapping_from_playlist(
            youtube, playlistId))
