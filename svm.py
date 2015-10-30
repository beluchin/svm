
import argparse
import re
import sys

from internal.data_utils import ids_to_titles_from_file, validate_rename_request
from internal.exception import DomainException
from internal.operations import support_undo
import internal.operations as operations
from internal.service.youtube import get_authenticated_youtube


def add_undo_parser(subparsers):
    p = subparsers.add_parser('undo', help='reverts the last rename')
    p.set_defaults(func=undo)


def add_reset_credentials_parser(subparsers):
    p = subparsers.add_parser(
            'reset-credentials', 
            help='resets existing credentials. Useful when accessing multiple accounts')
    p.set_defaults(func=reset_credentials)


def add_rename_many_parser(subparsers):
    p = subparsers.add_parser('rename-many', help='renames YouTube videos given a file')
    p.add_argument('filename', type=str, help='name of file with video mappings (id,title - one per line)')
    p.set_defaults(func=rename_many)


def add_rename_parser(subparsers):
    p = subparsers.add_parser('rename', help='renames YouTube videos')
    p.add_argument(
            metavar='videoid,title', 
            nargs='+', 
            action=ParseRenameRequest, 
            dest='pairs', 
            help='videoid-to-title mapping, comma-separated. Can enter many. Titles cannot have commas')
    p.set_defaults(func=rename)


def reset_credentials(args):
    operations.reset_credentials()
    

def undo(args):
    s = get_authenticated_youtube()
    operations.undo(s)
    

def rename(args):
    s = get_authenticated_youtube()
    operations.rename(s, args.pairs, on_rename=support_undo())


def rename_many(args):
    s = get_authenticated_youtube()
    operations.rename(s, 
                      ids_to_titles_from_file(args.filename), 
                      on_rename=support_undo())
    
    
class ParseRenameRequest(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        pairs = getattr(namespace, 'pairs', {})
        pairs = pairs if pairs is not None else {}
        for pair in values:
            validate_rename_request(pair)
            n, v = pair.split(',')
            pairs[n] = v
        setattr(namespace, 'pairs', pairs)
        
        
def convert_from_camelcase(s):
    s = re.sub('(.)([A-Z][a-z]+)', r'\1 \2', s)
    return re.sub('([a-z0-9])([A-Z])', r'\1 \2', s).lower()


def as_user_readable(e):
    ex = type(e).__name__
    ex = ex.replace('Exception', '', 1)
    ex = convert_from_camelcase(ex)
    return '%s: %s' % (ex, str(e))


def main(argv_):
    try:
        args = parser.parse_args(argv_)
        args.func(args)
    except DomainException as e:
        print(as_user_readable(e))

    
parser = argparse.ArgumentParser(
        prog='svm',
        description='manages Spartans swim team videos', 
        epilog='type $ svm <subcommand> -h for further help on the subcommands')
subparsers = parser.add_subparsers(title='subcommands')

add_rename_parser(subparsers)
add_rename_many_parser(subparsers)
add_reset_credentials_parser(subparsers)
add_undo_parser(subparsers)


if __name__ == '__main__':
    main(sys.argv[1:])