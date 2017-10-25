import argparse
import cache
import importlib.util
import logging
import os


SCRIPT_NAME = 'restcountries'
SCRIPT_VERSION = '1.0.0'


def _load(filename='restcountries_config.py'):
    path = None
    candidates = [  # TODO: Windows
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'default_config.py'),
        os.path.realpath('/etc/{}'.format(filename)),
        os.path.realpath('{}/.{}'.format(os.path.expanduser('~'), filename)),
        os.path.realpath(filename),
    ]
    # Load all candidates into global namespace in sequence, if they exist
    for i, candidate in enumerate(candidates):
        if os.path.exists(candidate):
            spec = importlib.util.spec_from_file_location(
                'config_lvl{}'.format(i), candidate)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            globals().update(module.__dict__)

def _init_logging():
    formatter = logging.Formatter(LOG_FORMAT)
    logger = logging.getLogger()
    logger.setLevel(LOG_LEVEL)
    if LOG_TO_FILE:
        fh = logging.FileHandler(LOG_FILE)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    if LOG_TO_STDERR:
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--auth-user', help='username for authentication')
    parser.add_argument('-p', '--auth-pass', help='password for authentication')
    parser.add_argument('-U', '--username', help='username to scan')
    parser.add_argument('-a', '--include-auth-user', help='query authenticating user\'s repositories', action='store_true')
    parser.add_argument('-P', '--api-path', help='base URL of Bitbucket API')
    parser.add_argument('-i', '--ingester', help='address of ingester instance')
    parser.add_argument('-I', '--ingester-off', help='do not write to ingester', action='store_true')
    parser.add_argument('-l', '--limit', type=int, help='maximum number of commits per branch')
    parser.add_argument('-r', '--retries', type=int, help='number of retries per request (including first try)')
    parser.add_argument('-t', '--timeout', type=int, help='request timeout in seconds')
    parser.add_argument('-c', '--cache-on', help='enable caching', action='store_true')
    parser.add_argument('-C', '--cache-off', help='disable caching', action='store_true')
    parser.add_argument('-v', '--verbose', help='write data to stdout', action='store_true')
    args = parser.parse_args()

    global API_PATH
    global AUTH_USER
    global AUTH_PASS
    global INCLUDE_AUTH_USER
    global INGESTER_PATH
    global LIMIT
    global USERNAME
    global REQUEST_RETRIES
    global REQUEST_TIMEOUT
    global CACHE_ENABLED
    global VERBOSE

    if args.api_path:
        API_PATH = args.api_path
    if args.auth_user:
        AUTH_USER = args.auth_user
    if args.auth_pass:
        AUTH_PASS = args.auth_pass
    if args.include_auth_user:
        INCLUDE_AUTH_USER = True
    if args.ingester is not None:
        INGESTER_PATH = args.ingester
    if args.ingester_off:
        INGESTER_PATH = None
    if args.limit is not None:
        LIMIT = args.limit
    if args.username:
        USERNAME = args.username
    if args.retries is not None:
        REQUEST_RETRIES = args.retries
    if args.timeout is not None:
        REQUEST_TIMEOUT = args.timeout
    if args.cache_on:
        CACHE_ENABLED = True
    if args.cache_off:
        CACHE_ENABLED = False
    if args.verbose:
        VERBOSE = True


_load()
_parse_args()
_init_logging()
cache.init(CACHE_PATH, CACHE_ENABLED, CACHE_SECONDS)
