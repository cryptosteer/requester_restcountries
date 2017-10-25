from collections import defaultdict
from datetime import datetime
import getpass
import os
import json
import requests
import socket
import uuid


class Stats(dict):

    def __init__(self):
        super(Stats, self).__init__()
        self['execution'] = {
            'time_start': self.nowstamp(),
            'time_end': None,
            'machine': socket.gethostname(),
            'user': getpass.getuser(),
        }

    def nowstamp(self):
        return datetime.now().isoformat()

    def script(self, name, version, flags):
        self['script'] = {
            'name': name,
            'version': version,
            'flags': flags
        }

    def count(self, dic, key='recordCount'):
        if key not in self:
            self[key] = defaultdict(int)
        for k, v in dic.items():
            self[key][k] += len(v)

    def finish(self):
        self['execution']['time_end'] = self.nowstamp()


class ChunksFinishedException(Exception):
    pass


class ChunkedIngesterLink:

    def __init__(self, path, docid=None):
        self.path = os.path.join(path, 'v2/chunk')
        self.docid = docid or str(uuid.uuid4())
        self.chunkid = 0
        self.done = False

    def _send(self, data):
        requests.post(self.path, json.dumps(data))

    def chunk(self, root, items):
        if (self.done):
            raise ChunksFinishedException()
        self._send({
            'id': self.docid,
            'chunkId': self.chunkid,
            'payload': {
                root: items
            },
        })
        self.chunkid += 1

    def stats(self, stats):
        if (self.done):
            raise ChunksFinishedException()
        self._send({
            'id': self.docid,
            'chunkId': self.chunkid,
            'stats': stats,
        })
        self.done = True

    def chunk_dict(self, dic, pagesize=100):
        for root, data in dic.items():
            if isinstance(data, list):
                left = 0
                while left < len(data):
                    right = min(len(data), left + pagesize)
                    self.chunk(root, data[left:right])
                    left += pagesize
            else:
                self.chunk(root, [data])
