# ====================================================================
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
# ====================================================================

import os, sys, unittest, shutil
from threading import RLock
import test_PyLucene 

from lucene import \
    PythonLock, PythonLockFactory, \
    PythonIndexInput, PythonIndexOutput, PythonDirectory, \
    JavaError, IOException, JArray, String

"""
The Directory Implementation here is for testing purposes only, not meant
as an example of writing one, the implementation here suffers from a lack
of safety when dealing with concurrent modifications as it does away with 
the file locking in the default lucene fsdirectory implementation.
"""

DEBUG = False

class DebugWrapper(object):

    def __init__(self, obj):
        self.obj = obj

    def __getattr__(self, name):
        print self.obj.__class__.__name__, self.obj.name, name
        sys.stdout.flush()
        return getattr(self.obj, name)
        
class DebugFactory(object):
    
    def __init__(self, klass):
        self.klass = klass
        
    def __call__(self, *args, **kw):
        instance = self.klass(*args, **kw)
        return DebugWrapper(instance)


class PythonDirLock(PythonLock):
    # only safe for a single process
    
    def __init__(self, name, path, lock):
        super(PythonDirLock, self).__init__()

        self.name = name
        self.lock_file = path
        self.lock = lock

    def isLocked(self):
        return self.lock.locked()

    def obtain(self):
        return self.lock.acquire()

    def release(self):
        return self.lock.release()


class PythonDirLockFactory(PythonLockFactory):

    def __init__(self, path):
        super(PythonDirLockFactory, self).__init__()
        
        self.path = path
        self._locks = {}

    def makeLock(self, name):

        lock = self._locks.get(name)
        if lock is None:
            lock = PythonDirLock(name, os.path.join(self.path, name), RLock())
            self._locks[name] = lock

        return lock

    def clearLock(self, name):

        lock = self._locks.pop(name, None)
        if lock is not None:
            lock.release()


class PythonFileStreamInput(PythonIndexInput):

    def __init__(self, name, fh, size, clone=False):
        if not clone:
            super(PythonFileStreamInput, self).__init__()
        self.name = name
        self.fh = fh
        self._length = size
        self.isOpen = True
        self.isClone = clone

    def length(self):
        return long(self._length)

    def clone(self):
        clone = PythonFileStreamInput(self.name, self.fh, self._length, True)
        return super(PythonFileStreamInput, self).clone(clone)

    def close(self):
        if self.isOpen:
            self.isOpen = False
            if not self.isClone:
                self.fh.close()

    def readInternal(self, length, pos):
        self.fh.seek(pos)
        return JArray('byte')(self.fh.read(length))

    def seekInternal(self, pos):
        self.fh.seek(pos)


class PythonFileStreamOutput(PythonIndexOutput):

    def __init__(self, name, fh):
        super(PythonFileStreamOutput, self).__init__()
        self.name = name
        self.fh = fh
        self.isOpen = True
        self._length = 0

    def close(self):
        if self.isOpen:
            super(PythonFileStreamOutput, self).close()
            self.isOpen = False
            self.fh.close()

    def length(self):
        return long(self._length)

    def seekInternal(self, pos):
        self.fh.seek(pos)

    def flushBuffer(self, bytes):

        self.fh.write(bytes.string_)
        self.fh.flush()
        self._length += len(bytes)


class PythonFileDirectory(PythonDirectory):

    def __init__(self, path):
        super(PythonFileDirectory, self).__init__(PythonDirLockFactory(path))

        self.name = path
        assert os.path.isdir(path)
        self.path = path
        self._streams = []

    def close(self):
        for stream in self._streams:
            stream.close()
        del self._streams[:]

    def createOutput(self, name):
        file_path = os.path.join(self.path, name)
        fh = open(file_path, "wb")
        stream = PythonFileStreamOutput(name, fh)
        self._streams.append(stream)
        return stream

    def deleteFile(self, name):
        if self.fileExists(name):
            os.unlink(os.path.join(self.path, name))

    def fileExists(self, name):
        return os.path.exists(os.path.join(self.path, name))

    def fileLength(self, name):
        file_path = os.path.join(self.path, name)
        return long(os.path.getsize(file_path))

    def fileModified(self, name):
        file_path = os.path.join(self.path, name)
        return os.path.getmtime(file_path)

    def listAll(self):
        return os.listdir(self.path)

    def sync(self, name):
        pass

    def openInput(self, name, bufferSize=0):
        file_path = os.path.join(self.path, name)
        try:
            fh = open(file_path, "rb")
        except IOError:
            raise JavaError, IOException(name)
        stream = PythonFileStreamInput(name, fh, os.path.getsize(file_path))
        self._streams.append(stream)
        return stream

    def touchFile(self, name):
        file_path = os.path.join(self.path, name)
        os.utime(file_path, None)


if DEBUG:
    _globals = globals()
    _globals['PythonFileDirectory'] = DebugFactory(PythonFileDirectory)
    _globals['PythonFileStreamInput'] = DebugFactory(PythonFileStreamInput)
    _globals['PythonFileStreamOutput'] = DebugFactory(PythonFileStreamOutput)
    _globals['PythonDirLock'] = DebugFactory(PythonDirLock)
    del _globals

class PythonDirectoryTests(unittest.TestCase, test_PyLucene.Test_PyLuceneBase):

    STORE_DIR = "testpyrepo"

    def setUp(self):
        if not os.path.exists(self.STORE_DIR):
            os.mkdir(self.STORE_DIR)

    def tearDown(self):
        if os.path.exists(self.STORE_DIR):
            shutil.rmtree(self.STORE_DIR)

    def openStore(self):
        return PythonFileDirectory(self.STORE_DIR)

    def closeStore(self, store, *args):
        for arg in args:
            if arg is not None:
                arg.close()
        store.close()

    def test_IncrementalLoop(self):
        print "Testing Indexing Incremental Looping"
        for i in range(100):
            print "indexing ", i
            sys.stdout.flush()
            self.test_indexDocument()
                       

if __name__ == "__main__":
    import sys, lucene
    env = lucene.initVM()
    if '-loop' in sys.argv:
        sys.argv.remove('-loop')
        while True:
            try:
                unittest.main()
            except:
                pass
            print 'inputs', env._dumpRefs(True).get('class org.osafoundation.lucene.store.PythonIndexOutput', 0)
            print 'outputs', env._dumpRefs(True).get('class org.osafoundation.lucene.store.PythonIndexInput', 0)
            print 'locks', env._dumpRefs(True).get('class org.osafoundation.lucene.store.PythonLock', 0)
            print 'dirs', env._dumpRefs(True).get('class org.osafoundation.lucene.store.PythonLock', 0)
    else:
        unittest.main()
