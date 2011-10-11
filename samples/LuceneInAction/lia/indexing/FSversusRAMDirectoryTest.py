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

from unittest import TestCase
from time import time
from datetime import timedelta

from lucene import \
     IndexWriter, SimpleAnalyzer, Document, Field, System, File, \
     SimpleFSDirectory, RAMDirectory


class FSversusRAMDirectoryTest(TestCase):

    def __init__(self, *args):

        super(FSversusRAMDirectoryTest, self).__init__(*args)
        self.docs = self.loadDocuments(3000, 5)

    def setUp(self):

        fsIndexDir = os.path.join(System.getProperty("java.io.tmpdir", "tmp"),
                                  "fs-index")
        self.rmdir(fsIndexDir)
        self.ramDir = RAMDirectory()
        self.fsDir = SimpleFSDirectory(File(fsIndexDir))

    def rmdir(self, dir):

        for dir, dirnames, filenames in os.walk(dir):
            for filename in filenames:
                os.remove(os.path.join(dir, filename))
            for dirname in dirnames:
                os.rmdir(os.path.join(dir, dirname))

    def testTiming(self):

        ramTiming = self.timeIndexWriter(self.ramDir)
        fsTiming = self.timeIndexWriter(self.fsDir)

        #self.assert_(fsTiming > ramTiming)

        print "RAMDirectory Time:", ramTiming
        print "FSDirectory Time :", fsTiming

    def timeIndexWriter(self, dir):

        start = time()
        self.addDocuments(dir)

        return timedelta(seconds=time() - start)

    def addDocuments(self, dir):

        writer = IndexWriter(dir, SimpleAnalyzer(), True,
                             IndexWriter.MaxFieldLength.UNLIMITED)

        #
        # change to adjust performance of indexing with FSDirectory
        # writer.mergeFactor = writer.mergeFactor
        # writer.maxMergeDocs = writer.maxMergeDocs
        # writer.minMergeDocs = writer.minMergeDocs
        #

        for word in self.docs:
            doc = Document()
            doc.add(Field("keyword", word,
                          Field.Store.YES, Field.Index.NOT_ANALYZED))
            doc.add(Field("unindexed", word,
                          Field.Store.YES, Field.Index.NO))
            doc.add(Field("unstored", word,
                          Field.Store.NO, Field.Index.ANALYZED))
            doc.add(Field("text", word,
                          Field.Store.YES, Field.Index.ANALYZED))
            writer.addDocument(doc)

        writer.optimize()
        writer.close()

    def loadDocuments(self, numDocs, wordsPerDoc):

        return ["Bibamus " * wordsPerDoc] * numDocs
