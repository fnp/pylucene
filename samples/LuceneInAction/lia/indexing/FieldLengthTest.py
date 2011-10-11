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

from itertools import izip
from unittest import TestCase
from time import time
from datetime import timedelta

from lucene import \
     IndexWriter, SimpleAnalyzer, Document, Field, System, File, \
     Term, TermQuery, IndexSearcher, SimpleFSDirectory


class FieldLengthTest(TestCase):

    keywords = ["1", "2"]
    unindexed = ["Netherlands", "Italy"]
    unstored = ["Amsterdam has lots of bridges",
                "Venice has lots of canals"]
    text = ["Amsterdam", "Venice"]

    def setUp(self):

        indexDir = os.path.join(System.getProperty("java.io.tmpdir", "tmp"),
                                "index-dir")
        self.dir = SimpleFSDirectory(File(indexDir))

    def testFieldSize(self):

        self.addDocuments(self.dir, 10)
        self.assertEqual(1, self.getHitCount("contents", "bridges"))

        self.addDocuments(self.dir, 1)
        self.assertEqual(0, self.getHitCount("contents", "bridges"))

    def getHitCount(self, fieldName, searchString):

        searcher = IndexSearcher(self.dir, True)
        t = Term(fieldName, searchString)
        query = TermQuery(t)
        hitCount = len(searcher.search(query, 50).scoreDocs)
        searcher.close()

        return hitCount

    def addDocuments(self, dir, maxFieldLength):

        writer = IndexWriter(dir, SimpleAnalyzer(), True,
                             IndexWriter.MaxFieldLength(maxFieldLength))
        
        for keyword, unindexed, unstored, text in \
                izip(self.keywords, self.unindexed, self.unstored, self.text):
            doc = Document()
            doc.add(Field("id", keyword,
                          Field.Store.YES, Field.Index.NOT_ANALYZED))
            doc.add(Field("country", unindexed,
                          Field.Store.YES, Field.Index.NO))
            doc.add(Field("contents", unstored,
                          Field.Store.NO, Field.Index.ANALYZED))
            doc.add(Field("city", text,
                          Field.Store.YES, Field.Index.ANALYZED))
            writer.addDocument(doc)

        writer.optimize()
        writer.close()
