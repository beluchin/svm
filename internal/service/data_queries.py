
from internal.data_utils import ids_to_titles_from_items


def video_titles(youtube, video_ids):
    items = video_list_response(youtube, video_ids)['items']
    return ids_to_titles_from_items(items) 


def video_list_response(youtube, video_ids):
    return youtube.videos() \
        .list(id=','.join(video_ids), part='snippet') \
        .execute()


def id_to_title_mapping_from_playlist(youtube, playlistId):
    response = youtube.playlistItems()\
            .list(playlistId=playlistId, part='snippet')\
            .execute()
    snippets = map(lambda i: i['snippet'], response['items'])
    m = map(lambda s: (s['resourceId']['videoId'], s['title']),
            snippets)
    return dict(m)

