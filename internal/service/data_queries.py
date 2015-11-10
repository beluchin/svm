
from internal.data_utils import ids_to_titles_from_items
from internal.exception import FailedToGetVideosFromPlaylistException


def video_titles(youtube, video_ids):
    items = video_list_response(youtube, video_ids)['items']
    return ids_to_titles_from_items(items) 


def video_list_response(youtube, video_ids):
    return youtube.videos() \
        .list(id=','.join(video_ids), part='snippet') \
        .execute()


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
        snippets = map(lambda i: i['snippet'], response['items'])
        m = map(lambda s: (s['resourceId']['videoId'], s['title']),
                snippets)
        return (dict(m), 
                response['pageInfo']['totalResults'],
                response['pageInfo']['resultsPerPage'],
                response.get('nextPageToken'))
    except:
        raise FailedToGetVideosFromPlaylistException(playlistId)

