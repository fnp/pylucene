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

from unittest import TestCase, main
from lucene import *


class FilteredQueryTestCase(TestCase):
    """
    Unit tests ported from Java Lucene
    """

    def setUp(self):

        self.directory = RAMDirectory()
        writer = IndexWriter(self.directory, WhitespaceAnalyzer(), True,
                             IndexWriter.MaxFieldLength.LIMITED)

        doc = Document()
        doc.add(Field("field", "one two three four five",
                      Field.Store.YES, Field.Index.ANALYZED))
        doc.add(Field("sorter", "b",
                      Field.Store.YES, Field.Index.ANALYZED))
                      
        writer.addDocument(doc)

        doc = Document()
        doc.add(Field("field", "one two three four",
                      Field.Store.YES, Field.Index.ANALYZED))
        doc.add(Field("sorter", "d",
                      Field.Store.YES, Field.Index.ANALYZED))

        writer.addDocument(doc)

        doc = Document()
        doc.add(Field("field", "one two three y",
                      Field.Store.YES, Field.Index.ANALYZED))
        doc.add(Field("sorter", "a",
                      Field.Store.YES, Field.Index.ANALYZED))

        writer.addDocument(doc)

        doc = Document()
        doc.add(Field("field", "one two x",
                      Field.Store.YES, Field.Index.ANALYZED))
        doc.add(Field("sorter", "c",
                      Field.Store.YES, Field.Index.ANALYZED))
                      
        writer.addDocument(doc)

        writer.optimize()
        writer.close()

        self.searcher = IndexSearcher(self.directory, True)
        self.query = TermQuery(Term("field", "three"))

        class filter(PythonFilter):
            def getDocIdSet(self, reader):
                bitset = BitSet(5)
                bitset.set(1)
                bitset.set(3)
                return DocIdBitSet(bitset)

        self.filter = filter()

    def tearDown(self):

        self.searcher.close()
        self.directory.close()

    def testFilteredQuery(self):

        filteredquery = FilteredQuery(self.query, self.filter)
        topDocs = self.searcher.search(filteredquery, 50)
        self.assertEqual(1, topDocs.totalHits)
        self.assertEqual(1, topDocs.scoreDocs[0].doc)

        topDocs = self.searcher.search(filteredquery, None, 50,
                                       Sort(SortField("sorter",
                                                      SortField.STRING)))
        self.assertEqual(1, topDocs.totalHits)
        self.assertEqual(1, topDocs.scoreDocs[0].doc)

        filteredquery = FilteredQuery(TermQuery(Term("field", "one")),
                                      self.filter)
        topDocs = self.searcher.search(filteredquery, 50)
        self.assertEqual(2, topDocs.totalHits)

        filteredquery = FilteredQuery(TermQuery(Term("field", "x")),
                                      self.filter)
        topDocs = self.searcher.search(filteredquery, 50)
        self.assertEqual(1, topDocs.totalHits)
        self.assertEqual(3, topDocs.scoreDocs[0].doc)

        filteredquery = FilteredQuery(TermQuery(Term("field", "y")),
                                      self.filter)
        topDocs = self.searcher.search(filteredquery, 50)
        self.assertEqual(0, topDocs.totalHits)

    def testRangeQuery(self):
        """
        This tests FilteredQuery's rewrite correctness
        """

        rq = TermRangeQuery("sorter", "b", "d", True, True)
        filteredquery = FilteredQuery(rq, self.filter)
        scoreDocs = self.searcher.search(filteredquery, 1000).scoreDocs
        self.assertEqual(2, len(scoreDocs))


if __name__ == "__main__":
    import sys, lucene
    lucene.initVM()
    if '-loop' in sys.argv:
        sys.argv.remove('-loop')
        while True:
            try:
                main()
            except:
                pass
    else:
         main()
