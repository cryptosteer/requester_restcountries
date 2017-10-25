from datetime import datetime
import hashlib
import logging
import os
import time


ENABLED = False
PATH = None
SECONDS = 0


def init(path, enabled=True, seconds=0):
    global ENABLED, PATH, SECONDS
    if enabled:
        logging.info('Cache enabled, max age {} seconds, path {}'.format(seconds, path))
    ENABLED = enabled
    PATH = path
    SECONDS = seconds


def ifenabled(f):
    def func(*args, **kwargs):
        if ENABLED:
            return f(*args, **kwargs)
        else:
            return None
    return func


def gen_hash(string):
    return '1%013i' % (int(hashlib.sha224(string.encode('utf-8')).hexdigest(), 16) % (10 ** 32))


@ifenabled
def load(slug):
    path = os.path.join(PATH, gen_hash(slug))
    try:
        ts = os.path.getmtime(path)
        if ts > time.mktime(datetime.now().timetuple()) - SECONDS:
            if not load.using_cache:
                load.using_cache = True
                logging.info('Using cache.')
            with open(path, 'r') as f:
                logging.debug('Cache LOAD  {} --> {}'.format(path, slug))
                return f.read()
    except:
        pass
    return None
load.using_cache = False


@ifenabled
def store(slug, content):
    path = os.path.join(PATH, gen_hash(slug))
    dn = os.path.dirname(path)
    if not os.path.exists(dn):
        os.makedirs(dn)
    with open(path, 'w') as f:
        f.write(content)
    logging.debug('Cache STORE {} <-- {}'.format(path, slug))
