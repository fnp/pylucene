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

from lucene import Integer, \
    Term, BooleanQuery, IndexSearcher, \
    NumericRangeQuery, TermQuery, BooleanClause


class BooleanQueryTest(LiaTestCase):

    def testAnd(self):

        searchingBooks = TermQuery(Term("subject", "search"))
        books2004 = NumericRangeQuery.newIntRange("pubmonth",
                                                  Integer(200401),
                                                  Integer(200412),
                                                  True, True)

        searchingBooks2004 = BooleanQuery()
        searchingBooks2004.add(searchingBooks, BooleanClause.Occur.MUST)
        searchingBooks2004.add(books2004, BooleanClause.Occur.MUST)

        searcher = IndexSearcher(self.directory, True)
        scoreDocs = searcher.search(searchingBooks2004, 50).scoreDocs

        self.assertHitsIncludeTitle(searcher, scoreDocs, "Lucene in Action")

    def testOr(self):

        methodologyBooks = TermQuery(Term("category",
                                          "/technology/computers/programming/methodology"))
        easternPhilosophyBooks = TermQuery(Term("category",
                                                "/philosophy/eastern"))

        enlightenmentBooks = BooleanQuery()
        enlightenmentBooks.add(methodologyBooks, BooleanClause.Occur.SHOULD)
        enlightenmentBooks.add(easternPhilosophyBooks, BooleanClause.Occur.SHOULD)

        searcher = IndexSearcher(self.directory, True)
        scoreDocs = searcher.search(enlightenmentBooks, 50).scoreDocs
        print "or =", enlightenmentBooks

        self.assertHitsIncludeTitle(searcher, scoreDocs,
                                    "Extreme Programming Explained")
        self.assertHitsIncludeTitle(searcher, scoreDocs,
                                    u"Tao Te Ching \u9053\u5FB7\u7D93")
