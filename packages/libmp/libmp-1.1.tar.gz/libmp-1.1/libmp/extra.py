import shelve
from functools import wraps


def __get_cache_filename__():
    return 'libmp.cache'


def cache(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        CACHE_ARQUIVO = __get_cache_filename__()
        if not CACHE_ARQUIVO:
            return func(*args)
        db = shelve.open(CACHE_ARQUIVO)
        key = ''
        try:
            key = "{0}-{1}".format(func.__name__, args)
            return db[key]
        except KeyError:
            print(f'Registrando novo cache {func.__name__}')
            result = func(*args)
            if result is not None:
                db[key] = result
                print(f'saving new data into cachedb {result}')
        finally:
            db.close()
        return result
    return wrapper


def clear_cache(chave):
    CACHE_ARQUIVO = __get_cache_filename__()
    db = shelve.open(CACHE_ARQUIVO)
    del db[chave]
