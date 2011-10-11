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

from lucene import \
     IndexWriter, IndexReader, IndexSearcher, \
     WhitespaceAnalyzer, Document, Field, Term, TermQuery

from lia.indexing.BaseIndexingTestCase import BaseIndexingTestCase


class DocumentUpdateTest(BaseIndexingTestCase):

    def testUpdate(self):

        self.assertEqual(1, self.getHitCount("city", "Amsterdam"))

        reader = IndexReader.open(self.dir, False)
        reader.deleteDocuments(Term("city", "Amsterdam"))
        reader.close()

        writer = IndexWriter(self.dir, self.getAnalyzer(), False,
                             IndexWriter.MaxFieldLength.UNLIMITED)
        doc = Document()
        doc.add(Field("id", "1", Field.Store.YES, Field.Index.NOT_ANALYZED))
        doc.add(Field("country", "Russia",
                      Field.Store.YES, Field.Index.NO))
        doc.add(Field("contents", "St. Petersburg has lots of bridges",
                      Field.Store.NO, Field.Index.ANALYZED))
        doc.add(Field("city", "St. Petersburg",
                      Field.Store.YES, Field.Index.ANALYZED))
        writer.addDocument(doc)
        writer.optimize()
        writer.close()

        self.assertEqual(0, self.getHitCount("city", "Amsterdam"))
        self.assertEqual(1, self.getHitCount("city", "Petersburg"))


    def getAnalyzer(self):

        return WhitespaceAnalyzer()

    def getHitCount(self, fieldName, searchString):

        searcher = IndexSearcher(self.dir, True)
        t = Term(fieldName, searchString)
        query = TermQuery(t)
        hitCount = len(searcher.search(query, 50).scoreDocs)
        searcher.close()

        return hitCount
