from internal.exception import TooManyCommasException


def ids_to_titles_from_items(items):
    '''items: items in a video list response from youtube'''
    result = dict()
    for item in items:
        video_id = item['id']
        title = item['snippet']['title']
        result[video_id] = title
    return result


def validate_rename_request(line):
    if (_contains_too_many_commas(line)):
        raise TooManyCommasException(line)


def _contains_too_many_commas(s):
    return s.count(',') > 1


def ids_to_titles_from_file(n):
    result = dict()
    with open(n) as f:
        for line in f:
            validate_rename_request(line)
            videoid, title = line.split(',')
            result[videoid] = title

    return result