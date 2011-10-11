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

from lia.common.LiaTestCase import LiaTestCase

from lucene import \
     WhitespaceAnalyzer, Document, Field, IndexWriter, Term, Explanation, \
     FuzzyQuery, IndexSearcher, Similarity, TermQuery, WildcardQuery, \
     RAMDirectory, PythonSimilarity


class ScoreTest(LiaTestCase):

    def setUp(self):

        super(ScoreTest, self).setUp()
        self.directory = RAMDirectory()

    def testSimple(self):

        class SimpleSimilarity(PythonSimilarity):

            def lengthNorm(_self, field, numTerms):
                return 1.0

            def queryNorm(_self, sumOfSquaredWeights):
                return 1.0

            def tf(_self, freq):
                return freq

            def sloppyFreq(_self, distance):
                return 2.0

            def idfTerms(_self, terms, searcher):
                return 1.0

            def idf(_self, docFreq, numDocs):
                return 1.0

            def coord(_self, overlap, maxOverlap):
                return 1.0

            def scorePayload(_self, docId, fieldName, start, end, payload,
                             offset, length):
                return 1.0

        self.indexSingleFieldDocs([Field("contents", "x", Field.Store.YES,
                                         Field.Index.ANALYZED)])
        searcher = IndexSearcher(self.directory)
        searcher.setSimilarity(SimpleSimilarity())

        query = TermQuery(Term("contents", "x"))
        explanation = searcher.explain(query, 0)
        print explanation

        scoreDocs = searcher.search(query, 50).scoreDocs
        self.assertEqual(1, len(scoreDocs))

        self.assertEqual(scoreDocs[0].score, 1.0)
        searcher.close()

    def indexSingleFieldDocs(self, fields):

        writer = IndexWriter(self.directory, WhitespaceAnalyzer(), True,
                             IndexWriter.MaxFieldLength.UNLIMITED)

        for field in fields:
            doc = Document()
            doc.add(field)
            writer.addDocument(doc)

        writer.optimize()
        writer.close()

    def testWildcard(self):

        self.indexSingleFieldDocs([Field("contents", "wild", Field.Store.YES,
                                         Field.Index.ANALYZED),
                                   Field("contents", "child", Field.Store.YES,
                                         Field.Index.ANALYZED),
                                   Field("contents", "mild", Field.Store.YES,
                                         Field.Index.ANALYZED),
                                   Field("contents", "mildew", Field.Store.YES,
                                         Field.Index.ANALYZED)])

        searcher = IndexSearcher(self.directory)
        query = WildcardQuery(Term("contents", "?ild*"))
        scoreDocs = searcher.search(query, 50).scoreDocs
        self.assertEqual(3, len(scoreDocs), "child no match")

        self.assertEqual(scoreDocs[0].score, scoreDocs[1].score,
                         "score the same")
        self.assertEqual(scoreDocs[1].score, scoreDocs[1].score,
                         "score the same")

    def testFuzzy(self):

        self.indexSingleFieldDocs([Field("contents", "fuzzy", Field.Store.YES,
                                         Field.Index.ANALYZED),
                                   Field("contents", "wuzzy", Field.Store.YES,
                                         Field.Index.ANALYZED)])

        searcher = IndexSearcher(self.directory)
        query = FuzzyQuery(Term("contents", "wuzza"))
        scoreDocs = searcher.search(query, 50).scoreDocs
        self.assertEqual(2, len(scoreDocs), "both close enough")

        self.assert_(scoreDocs[0].score != scoreDocs[1].score,
                     "wuzzy closer than fuzzy")
        self.assertEqual("wuzzy",
                         searcher.doc(scoreDocs[0].doc).get("contents"),
                         "wuzza bear")
