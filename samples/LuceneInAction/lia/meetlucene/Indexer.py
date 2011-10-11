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

from time import time
from datetime import timedelta
from lucene import \
    IndexWriter, StandardAnalyzer, Document, Field, \
    InputStreamReader, FileInputStream, Version, SimpleFSDirectory, File


class Indexer(object):

    def main(cls, argv):

        if len(argv) != 3:
            print "Usage: python Indexer.py <index dir> <data dir>"

        else:
            indexDir = argv[1]
            dataDir = argv[2]

            start = time()
            numIndexed = cls.index(indexDir, dataDir)
            duration = timedelta(seconds=time() - start)

            print "Indexing %s files took %s" %(numIndexed, duration)

    def index(cls, indexDir, dataDir):

        if not (os.path.exists(dataDir) and os.path.isdir(dataDir)):
            raise IOError, "%s does not exist or is not a directory" %(dataDir)

        dir = SimpleFSDirectory(File(indexDir))
        writer = IndexWriter(dir, StandardAnalyzer(Version.LUCENE_CURRENT),
                             True, IndexWriter.MaxFieldLength.LIMITED)
        writer.setUseCompoundFile(False)

        cls.indexDirectory(writer, dataDir)

        numIndexed = writer.numDocs()
        writer.optimize()
        writer.close()
        dir.close()

        return numIndexed

    def indexDirectory(cls, writer, dir):

        for name in os.listdir(dir):
            path = os.path.join(dir, name)
            if os.path.isfile(path):
                if path.endswith('.txt'):
                    cls.indexFile(writer, path)
            elif os.path.isdir(path):
                cls.indexDirectory(writer, path)

    def indexFile(cls, writer, path):

        try:
            reader = InputStreamReader(FileInputStream(path), 'iso-8859-1')
        except IOError, e:
            print 'IOError while opening %s: %s' %(path, e)
        else:
            print 'Indexing', path
            doc = Document()
            doc.add(Field("contents", reader))
            doc.add(Field("path", os.path.abspath(path),
                          Field.Store.YES, Field.Index.NOT_ANALYZED))
            writer.addDocument(doc)
            reader.close()

    main = classmethod(main)
    index = classmethod(index)
    indexDirectory = classmethod(indexDirectory)
    indexFile = classmethod(indexFile)


if __name__ == "__main__":
    import sys
    Indexer.main(sys.argv)
