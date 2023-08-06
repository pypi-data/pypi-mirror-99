import atexit
import socket
import struct
from queue import Queue
from threading import Thread
from typing import Sequence
from functools import lru_cache
import os
import subprocess
from time import time, sleep
from .csobject import CsObject
from .protocol import rpc, MAGIC_NUMBER, UNITON_VERSION
from .csutil import BrokenPromiseException


TLIST = (
  (int, rpc.INT32, struct.Struct("i")),
  (float, rpc.FLOAT32, struct.Struct("f")),
  (bool, rpc.BOOL, struct.Struct("?")),
)
TMAP = {x[0]: x[1:] for x in TLIST}
RMAP = {x[1]: x[2] for x in TLIST}
TCODE = struct.Struct("i")
SHOBJ = struct.Struct("i")  # should technically be I (unsigned int)


def recvall(sock, n):
  data = b''
  while len(data) < n:
    try:
      packet = sock.recv(n - len(data))
    except OSError:
      packet = None

    if not packet:
      return None
    data += packet
  return data



def get_free_port():
  """Not 100% guaranteed to be free but good enough"""
  s = socket.socket()
  s.bind(('', 0))
  port = s.getsockname()[1]
  s.close()
  return port


class UnityProc:
  """
  Representing a running Unity program
  Doubles as root namespace of that program, i.e. cs.System will return the 'System' namespace
  """

  _return_thread = None
  _cmd_queue = None
  _proc = None
  _sock = None

  def __init__(self, path=None, host=None, port=None):
    atexit.register(self.close)

    if path is not None:
      host = '127.0.0.1'
      port = get_free_port() if port is None else port
      env = os.environ.copy()

      env["UNITON_PORT"] = str(port)
      # TODO: allow to set cmd line args
      # TODO: figure out how to set -screen-height -screen-width robustly
      self._proc = subprocess.Popen([path], env=env)
      # self._proc = subprocess.Popen([path, '-batchmode'])  # while this still renders on Mac OS it's much slower

    else:
      host = '127.0.0.1' if host is None else host
      port = 11000 if port is None else port

    self._id_c = 2  # the first two elements are manually set

    # connect
    timeout = time() + 10

    while True:
      try:
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.connect((host, port))
        break
      except ConnectionRefusedError:
        if not self._proc:
          raise
        elif self._proc.poll() is not None:
          raise RuntimeError(f"Process {path} died before Uniton could connect!")
        elif time() > timeout:
          raise ConnectionRefusedError(f"Is {path} missing Uniton?")
        else:
          sleep(0.1) # wait, then repeat

    # self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack('ii', 1, 0))

    # bootstrap

    # magic exchange
    self._sock.sendall(struct.pack("i", MAGIC_NUMBER))
    magic_number, = struct.unpack('i', recvall(self._sock, 4))
    if magic_number != MAGIC_NUMBER:
      raise ConnectionError("Could not connect.")
    # bootstrap, = struct.unpack('i', recvall(self._sock, 4))

    # if bootstrap:
    from importlib import resources
    dll = resources.read_binary("uniton", "core.dll")

    self._sock.sendall(struct.pack("i", len(dll)))
    self._sock.sendall(dll)
    # zero, = struct.unpack('i', recvall(self._sock, 4))  # wait for a 0 as confirmation (so we don't move on to quickly)
    # assert zero == 0


    # sleep(1)  # give the server some time to close and reopen the port
    # self._sock.shutdown(socket.SHUT_WR)
    # self._sock.recv(0)

    # self._sock.close()
    # print("closed, waiting..")

    # sleep(4)  # We need to wait, otherwise we'll get "Adress already in use" on the server. I've tried to close the socket quicker but nothing worked.
    #
    #
    # # reconnect now to core.dll
    # self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # self._sock.connect((host, port))

    # self._sock.sendall(struct.pack("i", MAGIC_NUMBER))
    # magic_number, = struct.unpack('i', recvall(self._sock, 4))
    # if magic_number != MAGIC_NUMBER:
    #   raise ConnectionError("Could not connect.")
    # bootstrap, = struct.unpack('i', recvall(self._sock, 4))
    # assert not bootstrap, "We should have already bootstrapped!"

    #
    # else:
    #   print("Warning: This Uniton process has been connected to before. This could lead to strange behaviour.")



    # version compatibility check
    remote_version_tuple = struct.unpack('iii', recvall(self._sock, 4 * 3))
    self._remote_version = ".".join(str(x) for x in remote_version_tuple)
    local_version_macro = ".".join(UNITON_VERSION.split(".")[:2])
    remote_version_macro = ".".join(self._remote_version.split(".")[:2])
    if remote_version_macro != local_version_macro:
      # try:
      #   import urllib.request, json
      #   with urllib.request.urlopen("https://pypi.org/pypi/uniton/json") as url:
      #     data = json.loads(url.read().decode())
      #     all_versions = data["info"]["releases"].keys()
      #     best_compatible_local_version = sorted(v for v in all_versions if v.startswith(".".join(remote_version_tuple[:2])))[-1]
      # finally:
      raise ConnectionError(f'Remote Uniton version {self._remote_version} is not compatible with local version {UNITON_VERSION}. Change remote version to {local_version_macro}.* or local version to {remote_version_macro}.* via\n\npip install "uniton=={remote_version_macro}.*" --force-reinstall\n')


    # sponsorship check
    sponsor_error_len, = struct.unpack('i', recvall(self._sock, 4))
    if sponsor_error_len:
      msg = recvall(self._sock, sponsor_error_len).decode("utf-8", "strict")
      raise PermissionError(msg)


    # init object management
    self._garbage_objects = []

    # bootstrap
    self._cs_type = CsObject(self, id=0)  # C# System.Type
    self._backend = CsObject(self, id=1)

    from .namespace import Namespace
    self._ns = Namespace(self)
    # from .unity_old import UnityEngine
    # self._ns.ue = self._ns.UnityEngine = UnityEngine(self)

    # self.Uniton.Log.level = 2  # only print INFO and ERROR

  @property
  @lru_cache(maxsize=None)
  def _null(self):
    # TODO: probably better provide this from the c sharp side
    return CsObject(self, id=self.cmd(rpc.NOOP, b''))

  def waitall(self):
    # TODO: this is obviously hacky
    str(self._backend)

  @property
  def _pid(self):
    return self.System.Diagnostics.Process.GetCurrentProcess().Id

  def __getattr__(self, item):
    return getattr(self._ns, item)
    # return self._ns.__getattr__(item)  # Warning: this line breaks the namespace caching!

  def __dir__(self):
    return list(super().__dir__()) + dir(self._ns)

  def __del__(self):
    self.close()

  def close(self):
    atexit.unregister(self.close)
    if self._sock is not None:
      self._sock.close()

    if self._proc is not None:
      self._proc.kill()

  def delete_object(self, x):
    self._garbage_objects.append(x)
    # print("del", x.id)

    # if len(self.garbage_objects) > 10000000:  # Don't delete because we recycle
    #   # print("garbage collect")
    #   ids = tuple(obj.id for obj in self.garbage_objects)  # also copy is necessary to avoid recursion
    #   self.garbage_objects.clear()
    #   self._del_objects(ids) # this will create new garbage

  def make_id(self):
    # print(tuple(x.id for x in self.garbage_objects))
    if self._garbage_objects:
      x = self._garbage_objects.pop()
      # print("recycle", x.id)
    else:
      x = self._id_c
      self._id_c += 1  # TODO: check for overflow
      # print('mk', x.id)
    return x

  def run_cmds(self):
    # TODO: make separate class for this
    try:
      while True:
        # get length
        d = recvall(self._sock, 4)
        if d is None: break
        n, = struct.unpack('i', d)

        # get data
        d = recvall(self._sock, n)
        if d is None: break  # TODO: shouldn't this be an error?
        exc, = struct.unpack_from('i', d, 0)
        if exc:
          # raise RemoteException(self.deserialize(d[4:]))
          print("C# " + self.deserialize(d[4:]))
          print("------------------\n")
          break
        else:
          # self.response_queue.put(self.deserialize(d[4:]))
          p = self.promise_queue.get_nowait()
          assert p is not None, 'Received unexpected data from C#'
          p.resolve(self.deserialize(d[4:]))
    finally:
      while not self.promise_queue.empty():
        p = self.promise_queue.get_nowait()
        p.resolve(BrokenPromiseException("The command stream was closed before this promise could be resolved."))

      # print("Shutting down return thread")

  def cmd(self, method, data, out=None):
    if self._return_thread is None or not self._return_thread.is_alive():
      # if self.rit is None:
      # self.cmd_queue = Queue(1000)
      self.promise_queue = Queue()
      self.response_queue = Queue(1)
      self._return_thread = Thread(target=self.run_cmds, daemon=True)  # TODO: remove daemon and shut down properly
      self._return_thread.start()

      # self.rit = self.cmd_it()
      CsObject(self, self.cmd(rpc.OPEN_CMD_STREAM, b''))  # cmd stream open

    rid = self.make_id() if out is None else 0  # if out is not None then remote object is sent and then  discarded

    # self.cmd_queue.put(rpc.Cmd(method=method, rid=rid, args=self.deflate(args)))  # block if full
    data = struct.pack('ii', method, rid) + data
    # self.cmd_queue.put(rpc.Cmd(method=method, rid=rid, data=data))  # block if full

    data = struct.pack('i', len(data)) + data  # send length information

    if out is None:
      out = rid
    else:
      # print("blocking!")
      # return self.response_queue.get()  # block
      # self.garbage_objects.append(rid) # prevent memory leak!

      self.promise_queue.put(out)

    self._sock.sendall(data)

    return out

  import sys
  assert sys.byteorder == "little", "We only support little endian systems"

  def deserialize(self, x):
    # vi = x.WhichOneof("Value")
    # if vi == "list":
    #   return [self.deserialize(e) for e in x.list.items]

    t, = TCODE.unpack_from(x)
    offset = TCODE.size
    if t in RMAP:
      r, = RMAP[t].unpack_from(x, offset)
      return r
    elif t == rpc.BYTES:
      return x[offset:]
    elif t == rpc.STRING:
      return x[offset:].decode("utf-8", "strict")
    else:
      raise AttributeError(f"Can't decode type {t}")

    # if vi == "obj":
    #   if x.obj.id not in self.objs:"
    #     cls = None if x.obj.tid == 0 else CsObject()
    #     r = CsObject(id=x.obj.id, _con=self)
    #     self.objs[x.obj.id] = weakref.ref(r)
    #     return r
      # else:
      #   return self.objs[x.obj.id]()

    # return getattr(x, vi)

  def serialize_objs(self, *args):  # TODO: rename to serialize_obj_ids
    # important: we need to create all RObjects and only afterwards query the ids
    # if we immediatly get the ids and then forget about each RObject, they will be garbage collected and ids might be reused
    obj = tuple(self.tocs(e) for e in
                args)  # this can't be a generator because of the above reason
    ids = (e.id for e in obj)
    data = b"".join(SHOBJ.pack(id) for id in ids)
    return data
  
  def tocs(self, x):
    """Send Python object to C#"""
    # Serialization / Deserialization from bytes
    # https://docs.python.org/3.6/library/struct.html

    num_type = TMAP.get(type(x), None)
    if num_type is not None:
      rpc_fn, st = num_type
      # return rpc.Value(int32=x)
      id = self.cmd(rpc_fn, st.pack(x))
    elif isinstance(x, str):
      # return rpc.Value(str=x)
      id = self.cmd(rpc.STRING, x.encode())  # utf8
    # elif isinstance(x, bytes):
    #   return rpc.Value(bytes=x)
    # elif isinstance(x, bool):
    #   return rpc.Value(bool=x)
    # elif x is None:
    #   return rpc.Value(null=rpc.Null())
    elif isinstance(x, CsObject):
      return x

    elif hasattr(x, '_wrapped_cs_object'):
      return x._wrapped_cs_object

    elif isinstance(x, bytes):
      id = self.cmd(rpc.BYTES, x)

    elif isinstance(x, Sequence):
      print("sequence")
      # return rpc.Value(list=rpc.List(items=(self.deflate(e) for e in x)))
      id = self.cmd(rpc.TUPLE, self.serialize_objs(*x))
    else:
      raise AttributeError(f"Can't serialize {type(x)}")

    return CsObject(self, id)
