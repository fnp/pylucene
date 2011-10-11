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

from lucene import \
    SimpleFSDirectory, System, File, \
    Document, Field, SimpleAnalyzer, IndexWriter, IndexReader


class BaseIndexingTestCase(TestCase):

    keywords = ["1", "2"]
    unindexed = ["Netherlands", "Italy"]
    unstored = ["Amsterdam has lots of bridges",
                "Venice has lots of canals"]
    text = ["Amsterdam", "Venice"]

    def setUp(self):

        indexDir = os.path.join(System.getProperty('java.io.tmpdir', 'tmp'),
                                'index-dir')
        self.rmdir(indexDir)
        self.dir = SimpleFSDirectory(File(indexDir))
        self.addDocuments(self.dir)

    def rmdir(self, dir):

        for dir, dirnames, filenames in os.walk(dir):
            for filename in filenames:
                os.remove(os.path.join(dir, filename))
            for dirname in dirnames:
                os.rmdir(os.path.join(dir, dirname))

    def addDocuments(self, dir):

        writer = IndexWriter(dir, self.getAnalyzer(), True,
                             IndexWriter.MaxFieldLength.UNLIMITED)
        writer.setUseCompoundFile(self.isCompound())

        for i in xrange(len(self.keywords)):
            doc = Document()
            doc.add(Field("id", self.keywords[i],
                          Field.Store.YES, Field.Index.NOT_ANALYZED))
            doc.add(Field("country", self.unindexed[i],
                          Field.Store.YES, Field.Index.NO))
            doc.add(Field("contents", self.unstored[i],
                          Field.Store.NO, Field.Index.ANALYZED))
            doc.add(Field("city", self.text[i],
                          Field.Store.YES, Field.Index.ANALYZED))
            writer.addDocument(doc)

        writer.optimize()
        writer.close()

    def getAnalyzer(self):

        return SimpleAnalyzer()

    def isCompound(self):

        return True

    def testIndexWriter(self):

        writer = IndexWriter(self.dir, self.getAnalyzer(), False,
                             IndexWriter.MaxFieldLength.UNLIMITED)
        self.assertEqual(len(self.keywords), writer.numDocs())
        writer.close()

    def testIndexReader(self):

        reader = IndexReader.open(self.dir, True)
        self.assertEqual(len(self.keywords), reader.maxDoc())
        self.assertEqual(len(self.keywords), reader.numDocs())
        reader.close()
