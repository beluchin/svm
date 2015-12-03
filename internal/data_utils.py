from internal.exception import TooManyCommasException


def ids_to_titles_from_items(items):
    '''items: items in a video list response from youtube'''
    result = dict()
    for item in items:
        video_id = item['id']
        title = item['snippet']['title']
        result[video_id] = title
    return result


def ensure_valid_mapping(line):
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
    def _skip(line):
        return not line.strip()
    
    result = dict()
    with open(n) as f:
        for line in f:
            if _skip(line):
                continue
            ensure_valid_mapping(line)
            k, v = _strip(*line.split(','))
            result[k] = v

    return result