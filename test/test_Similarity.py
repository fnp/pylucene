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


class SimpleSimilarity(PythonSimilarity):

    def computeNorm(self, field, state):
        return 1.0

    def queryNorm(self, sumOfSquaredWeights):
        return 1.0

    def tf(self, freq):
        return freq

    def sloppyFreq(self, distance):
        return 2.0

    def idfTerms(self, terms, searcher):
        return 1.0

    def idf(self, docFreq, numDocs):
        return 1.0

    def coord(self, overlap, maxOverlap):
        return 1.0

    def scorePayload(self, docId, fieldName, start, end, payload,
                     offset, length):
        return 1.0


class SimilarityTestCase(TestCase):
    """
    Unit tests ported from Java Lucene
    """

    def testSimilarity(self):

        store = RAMDirectory()
        writer = IndexWriter(store, SimpleAnalyzer(), True,
                             IndexWriter.MaxFieldLength.LIMITED)
        writer.setSimilarity(SimpleSimilarity())
    
        d1 = Document()
        d1.add(Field("field", "a c", Field.Store.YES, Field.Index.ANALYZED))

        d2 = Document()
        d2.add(Field("field", "a b c", Field.Store.YES, Field.Index.ANALYZED))
    
        writer.addDocument(d1)
        writer.addDocument(d2)
        writer.optimize()
        writer.close()

        searcher = IndexSearcher(store, True)
        searcher.setSimilarity(SimpleSimilarity())

        a = Term("field", "a")
        b = Term("field", "b")
        c = Term("field", "c")

        class collector1(PythonCollector):
            def collect(_self, doc, score):
                self.assertEqual(1.0, score)
            def setNextReader(_self, reader, docBase):
                pass
            def acceptsDocsOutOfOrder(_self):
                return True

        searcher.search(TermQuery(b), collector1())


        bq = BooleanQuery()
        bq.add(TermQuery(a), BooleanClause.Occur.SHOULD)
        bq.add(TermQuery(b), BooleanClause.Occur.SHOULD)

        class collector2(PythonCollector):
            def collect(_self, doc, score):
                self.assertEqual(doc + _self.base + 1, score)
            def setNextReader(_self, reader, docBase):
                _self.base = docBase
            def acceptsDocsOutOfOrder(_self):
                return True

        searcher.search(bq, collector2())


        pq = PhraseQuery()
        pq.add(a)
        pq.add(c)

        class collector3(PythonCollector):
            def collect(_self, doc, score):
                self.assertEqual(1.0, score)
            def setNextReader(_self, reader, docBase):
                pass
            def acceptsDocsOutOfOrder(_self):
                return True

        searcher.search(pq, collector3())


        pq.setSlop(2)

        class collector4(PythonCollector):
            def collect(_self, doc, score):
                self.assertEqual(2.0, score)
            def setNextReader(_self, reader, docBase):
                pass
            def acceptsDocsOutOfOrder(_self):
                return True

        searcher.search(pq, collector4())


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
