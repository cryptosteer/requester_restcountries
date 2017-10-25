import cache
import conf
from collections import namedtuple
import json
import logging
import re
import requests
from urllib.parse import urljoin


Response = namedtuple('Response', 'ok status url headers content')


headers = {
    'Accept': 'application/json;charset=utf-8'
}


def path2url(path):
    return urljoin(conf.API_PATH, path.strip('/'))


def _get_request(url):
    logging.info('GET {}'.format(url))
    for i in range(conf.REQUEST_RETRIES):
        try:
            response = requests.get(url, headers=headers, timeout=conf.REQUEST_TIMEOUT)
            if response is not None:
                if response.ok or int(response.status_code) in (conf.CACHE_STATUS or []):
                    return Response(ok=response.ok,
                                    status=response.status_code,
                                    url=url,
                                    headers=dict(response.headers),
                                    content=response.text)
                break
        except:
            logging.warning('Request failed (attempt {} of {}), trying again ...'.\
                            format(i+1, conf.REQUEST_RETRIES))
    logging.error('{} requesting {}'.format(response.status_code, url))
    if response.headers.get('Content-Type') == 'application/json':
        logging.error(response.text)
    raise requests.exceptions.RequestException()


def get_item(url=None, path=None):
    if path:
        url = path2url(path)
    src = cache.load(url)
    if src:
        d = json.loads(src)
        response = Response(*d)
    else:
        response = _get_request(url)
        cache.store(url, json.dumps(response))
    if not response.ok:
        logging.error('Status {} on {}'.format(response.status, response.url))
        return None
    return json.loads(response.content)


def get_list(url=None, path=None, limit=None):
    if path:
        url = path2url(path)
    entries = []
    if url:
        try:
            data = get_item(url=url)
            if not data:
                raise requests.exceptions.RequestException
            entries += data
            return entries
        except requests.exceptions.RequestException:
            logging.error('Aborting list after {} entries: {}'.format(len(entries), url))


def get_lists(urls=None, paths=None, limit=None):
    urls = urls or []
    for path in paths or []:
        urls.append(path2url(path))
    result = []
    for url in urls:
        result += get_list(url=url, limit=limit)
    return result
