import os
from tempfile import NamedTemporaryFile


def tempfile(*args):
    class File:
        def __enter__(self):
            t = NamedTemporaryFile(mode='w+', delete=False)
            self._name = t.name
            for l in args:  
                print(l, file=t)
            t.close()
            return self
            
        def __exit__(self, *args, **kwargs):
            os.remove(self._name)
            
        def __str__(self):
            return self._name

    return File()


