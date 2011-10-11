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
    SimpleAnalyzer, Document, TermQuery, QueryParser, IndexSearcher, Term, \
    Version


class BasicSearchingTest(LiaTestCase):

    def testTerm(self):

        searcher = IndexSearcher(self.directory, True)
        t = Term("subject", "ant")
        query = TermQuery(t)
        scoreDocs = searcher.search(query, 50).scoreDocs
        self.assertEqual(1, len(scoreDocs), "JDwA")

        t = Term("subject", "junit")
        scoreDocs = searcher.search(TermQuery(t), 50).scoreDocs
        self.assertEqual(2, len(scoreDocs))

        searcher.close()

    def testKeyword(self):

        searcher = IndexSearcher(self.directory, True)
        t = Term("isbn", "1930110995")
        query = TermQuery(t)
        scoreDocs = searcher.search(query, 50).scoreDocs
        self.assertEqual(1, len(scoreDocs), "JUnit in Action")

    def testQueryParser(self):

        searcher = IndexSearcher(self.directory, True)

        query = QueryParser(Version.LUCENE_CURRENT, "contents",
                            SimpleAnalyzer()).parse("+JUNIT +ANT -MOCK")
        scoreDocs = searcher.search(query, 50).scoreDocs
        self.assertEqual(1, len(scoreDocs))
        d = searcher.doc(scoreDocs[0].doc)
        self.assertEqual("Java Development with Ant", d.get("title"))

        query = QueryParser(Version.LUCENE_CURRENT, "contents",
                            SimpleAnalyzer()).parse("mock OR junit")
        scoreDocs = searcher.search(query, 50).scoreDocs
        self.assertEqual(2, len(scoreDocs), "JDwA and JIA")
