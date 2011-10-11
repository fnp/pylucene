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
     IndexWriter, SimpleAnalyzer, Document, Field, Term, FSDirectory, System


class IndexTuningDemo(object):

    def main(cls, argv):

        if len(argv) < 5:
            print "Usage: python IndexTuningDemo.py <numDocs> <mergeFactor> <maxMergeDocs> <maxBufferedDocs>"
            return
            
        docsInIndex  = int(argv[1])

        # create an index called 'index-dir' in a temp directory
        indexDir = os.path.join(System.getProperty('java.io.tmpdir', 'tmp'),
                                'index-dir')
        dir = FSDirectory.getDirectory(indexDir, True)
        analyzer = SimpleAnalyzer()
        writer = IndexWriter(dir, analyzer, True)

        # set variables that affect speed of indexing
        writer.setMergeFactor(int(argv[2]))
        writer.setMaxMergeDocs(int(argv[3]))
        writer.setMaxBufferedDocs(int(argv[4]))
        # writer.infoStream = System.out

        print "Merge factor:  ", writer.getMergeFactor()
        print "Max merge docs:", writer.getMaxMergeDocs()
        print "Max buffered docs:", writer.getMaxBufferedDocs()

        start = time()
        for i in xrange(docsInIndex):
            doc = Document()
            doc.add(Field("fieldname", "Bibamus",
                          Field.Store.YES, Field.Index.TOKENIZED))
            writer.addDocument(doc)

        writer.close()
        print "Time: ", timedelta(seconds=time() - start)

    main = classmethod(main)
