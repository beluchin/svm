from internal.exception import TooManyCommasException


def ids_to_titles_from_items(items):
    '''items: items in a video list response from youtube'''
    result = dict()
    for item in items:
        video_id = item['id']
        title = item['snippet']['title']
        result[video_id] = title
    return result


def validate_mapping(line):
    if (_contains_too_many_commas(line)):
        raise TooManyCommasException(line)


def _contains_too_many_commas(s):
    return s.count(',') > 1


def _remove_quotes(s):
    c = s[0]
    return s[1:-1] if c in {'\'', '"'} and s[-1] == c else s


def _strip(*ss):
    return [_remove_quotes(s.rstrip()) for s in ss]

    
def mappings(n):
    result = dict()
    with open(n) as f:
        for line in f:
            validate_mapping(line)
            videoid, title = _strip(*line.split(','))
            result[videoid] = title

    return result