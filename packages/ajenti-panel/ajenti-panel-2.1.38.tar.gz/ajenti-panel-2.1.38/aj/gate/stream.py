from gevent.lock import RLock
import binascii
import gevent.socket
import json
import os
import logging

MSG_SIZE_LIMIT = 1024 * 1024 * 128  # 128 MB
MSG_CONTINUATION_MARKER = '\x00\x00\x00continued\x00\x00\x00'


def _seq_split(to_split):
    while to_split:
        yield to_split[:MSG_SIZE_LIMIT] + (MSG_CONTINUATION_MARKER if len(to_split) > MSG_SIZE_LIMIT else '')
        to_split = to_split[MSG_SIZE_LIMIT:]


def _seq_is_continued(part):
    return part.endswith(MSG_CONTINUATION_MARKER)


def _seq_combine(parts):
    full_object = ''
    for part in parts[:-1]:
        full_object += part[len(MSG_CONTINUATION_MARKER):]
    full_object += parts[-1]
    return full_object


class GateStreamRequest():
    def __init__(self, obj, endpoint):
        self.id = binascii.hexlify(os.urandom(32)).decode()
        self.object = obj
        self.endpoint = endpoint

    def serialize(self):
        object_tmp = {k : (v.decode()  if isinstance(v, bytes) else v) for k, v in self.object.items()}
        return {
            'id': self.id,
            'object': object_tmp,
        }

    @classmethod
    def deserialize(cls, data):
        self = cls(data['object'], None)
        self.id = data['id']
        return self


class GateStreamResponse():
    def __init__(self, _id, obj):
        self.id = _id
        self.object = obj

    def serialize(self):
        return {
            'id': self.id,
            'object': self.object,
        }

    @classmethod
    def deserialize(cls, data):
        self = cls(data['id'], data['object'])
        return self


class GateStreamServerEndpoint():
    def __init__(self, pipe):
        self.pipe = pipe
        self.buffer = {}
        self.buffer_lock = RLock()
        self.log = False

    def send(self, obj):
        rq = GateStreamRequest(obj, self)
        if not self.pipe._reader._closed:
            for part in _seq_split(json.dumps(rq.serialize())):
                self.pipe.put(part)
        if self.log:
            logging.debug('%s: >> %s', self, rq.id)
        return rq

    def recv_single(self, timeout):
        try:
            if timeout:
                with gevent.Timeout(timeout) as t:
                    data = self.pipe.get(t)
            else:
                data = self.pipe.get()
            return data
        # pylint: disable=E0712
        except gevent.Timeout:
            return None
        except EOFError:
            return None

    def buffer_single_response(self, timeout):
        try:
            with self.buffer_lock:
                data = self.recv_single(timeout)
                if not data:
                    return
                resp = GateStreamResponse.deserialize(data)
                if self.log:
                    logging.debug('%s: << %s', self, resp.id)
                self.buffer[resp.id] = resp
                return resp
        except IOError:
            return None

    def list_responses(self):
        with self.buffer_lock:
            return list(self.buffer)

    def has_response(self, _id):
        with self.buffer_lock:
            return _id in self.buffer

    def ack_response(self, _id):
        with self.buffer_lock:
            return self.buffer.pop(_id)

    def destroy(self):
        self.pipe.close()

class GateStreamWorkerEndpoint():
    def __init__(self, pipe):
        self.pipe = pipe
        self.log = False

    def reply(self, request, obj):
        resp = GateStreamResponse(request.id if request else None, obj)
        self.pipe.put(resp.serialize())
        if self.log:
            logging.debug('%s: >> %s', self, resp.id)

    def recv(self):
        parts = [self.pipe.get()]
        while _seq_is_continued(parts[-1]):
            parts.append(self.pipe.get())

        rq = GateStreamRequest.deserialize(json.loads(_seq_combine(parts)))
        if self.log:
            logging.debug('%s: << %s', self, rq.id)
        return rq
