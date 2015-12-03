
from builtins import len

from internal.data_utils import ids_to_titles_from_items
from internal.exception import FailedToGetVideosFromPlaylistException


def video_titles(youtube, video_ids):
    items = video_list_response_items(youtube, video_ids)
    return ids_to_titles_from_items(items) 


_video_list_batch_size = 50
def video_list_response_items(youtube, video_ids):
    video_ids = list(video_ids)
    size = len(video_ids)
    total = 0
    result = []
    while total < size:
        batch = video_ids[total:total + _video_list_batch_size]
        result.extend(youtube.videos() \
                .list(id=','.join(batch), part='snippet') \
                .execute()\
                ['items'])
        total += _video_list_batch_size
    return result


def id_to_title_mapping_from_playlist(youtube, playlistId, **kwargs):
    result, total, rpp, npt = _id_to_title_mapping_from_playlist_multiple(
            youtube, playlistId, **kwargs)
    sum_ = rpp
    while total > sum_:
        r, _, rpp, npt = _id_to_title_mapping_from_playlist_multiple(
                youtube, playlistId, pageToken=npt, **kwargs)
        result.update(r)
        sum_ += rpp
    return result

def _id_to_title_mapping_from_playlist_multiple(youtube, 
                                                playlistId, 
                                                **kwargs):
    try:
        response = youtube.playlistItems()\
                .list(playlistId=playlistId, 
                      part='snippet',
                      **kwargs)\
                .execute()
    except:
        raise FailedToGetVideosFromPlaylistException(playlistId)

    snippets = map(lambda i: i['snippet'], response['items'])
    m = map(lambda s: (s['resourceId']['videoId'], s['title']),
            snippets)
    return (dict(m), 
            response['pageInfo']['totalResults'],
            response['pageInfo']['resultsPerPage'],
            response.get('nextPageToken'))

