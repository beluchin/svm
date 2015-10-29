from tempfile import NamedTemporaryFile
 
def tempfile(*args):
    t = NamedTemporaryFile(mode='w+', delete=False)
    result = t.name
    for l in args:  
        print(l, file=t)
    t.close()
    return result


