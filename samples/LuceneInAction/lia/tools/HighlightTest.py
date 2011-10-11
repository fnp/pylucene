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
     SimpleAnalyzer, Term, IndexSearcher, TermQuery, \
     Highlighter, QueryScorer, StringReader, Version


class HighlightTest(LiaTestCase):

    def testHighlighting(self):

        text = "The quick brown fox jumps over the lazy dog"

        query = TermQuery(Term("field", "fox"))
        scorer = QueryScorer(query)
        highlighter = Highlighter(scorer)

        tokenStream = SimpleAnalyzer(Version.LUCENE_CURRENT).tokenStream("field", StringReader(text))

        self.assertEqual("The quick brown <B>fox</B> jumps over the lazy dog",
                         highlighter.getBestFragment(tokenStream, text))

    def testHits(self):

        searcher = IndexSearcher(self.directory, True)
        query = TermQuery(Term("title", "action"))
        scoreDocs = searcher.search(query, 50).scoreDocs

        scorer = QueryScorer(query)
        highlighter = Highlighter(scorer)

        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)
            title = doc["title"]
            stream = SimpleAnalyzer(Version.LUCENE_CURRENT).tokenStream("title", StringReader(title))
            fragment = highlighter.getBestFragment(stream, title)
    
            print fragment
