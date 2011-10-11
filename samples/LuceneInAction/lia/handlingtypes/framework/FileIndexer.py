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

import os
import lia.handlingtypes as handlingtypes

from time import time
from datetime import timedelta
from lucene import IndexWriter, StandardAnalyzer

from lia.util.ClassLoader import ClassLoader

 #
 # A File Indexer capable of recursively indexing a directory tree.
 # Based on lia.meetlucene.Indexer, but handling more than plaintext.
 #

class FileIndexer(object):

    def main(cls, argv):

        if len(argv) != 3:
            print "Usage: python FileIndexer.py <index dir> <data dir>"
            return

        indexDir = argv[1]
        dataDir = argv[2]

        propsFile = os.path.join(os.path.dirname(handlingtypes.__file__),
                                 'framework', 'handler.properties')
        input = file(propsFile)
        props = {}
        while True:
            line = input.readline().strip()
            if not line:
                break
            if line.startswith('#'):
                continue
            name, value = line.split('=')
            props[name.strip()] = value.strip()
        input.close()
        cls.handlerProps = props

        start = time()
        numIndexed = cls.index(indexDir, dataDir)
        duration = timedelta(seconds=time() - start)

        print "Indexing %s files took %s" %(numIndexed, duration)

    def index(cls, indexDir, dataDir):

        if not (os.path.exists(dataDir) and os.path.isdir(dataDir)):
            raise IOError, "%s does not exist or is not a directory" %(dataDir)

        writer = IndexWriter(indexDir, StandardAnalyzer(), True,
                             IndexWriter.MaxFieldLength.UNLIMITED)
        writer.setUseCompoundFile(False)

        numIndexed = cls.indexDirectory(writer, dataDir)
        writer.optimize()
        writer.close()

        return numIndexed

    def indexDirectory(cls, writer, dir):

        count = 0
        dirs = []

        for name in os.listdir(dir):
            path = os.path.join(dir, name)
            if os.path.isfile(path):
                doc = cls.indexFile(writer, path)
                if doc is not None:
                    count += 1
            elif os.path.isdir(path) and not name.startswith('.'):
                dirs.append(path)

        for dir in dirs:
            count += cls.indexDirectory(writer, dir)

        return count

    def indexFile(cls, writer, path):

        name, ext = os.path.splitext(path)
        if ext.startswith(os.path.extsep):
            ext = ext[len(os.path.extsep):]

        if ext:
            handlerClassName = cls.handlerProps.get(ext, None)
            if handlerClassName is None:
                print "error indexing %s: no handler for %s files" %(path, ext)
                return None

            try:
                handlerClass = ClassLoader.loadClass(handlerClassName)
                handler = handlerClass()

                doc = handler.indexFile(writer, path)
                if doc is not None:
                    print 'indexed', path

                return doc
            except SyntaxError:
                raise
            except Exception, e:
                print 'error indexing %s: %s' %(path, e)
                return None

    main = classmethod(main)
    index = classmethod(index)
    indexDirectory = classmethod(indexDirectory)
    indexFile = classmethod(indexFile)
