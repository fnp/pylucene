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
     IndexSearcher, Term, TermQuery, MatchAllDocsQuery, \
     BooleanQuery, BooleanClause, CachingWrapperFilter, \
     TermRangeFilter, NumericRangeFilter, FieldCacheRangeFilter, \
     FieldCacheTermsFilter, QueryWrapperFilter, PrefixFilter
     

class FilterTest(LiaTestCase):

    def setUp(self):

        super(FilterTest, self).setUp()

        self.allBooks = MatchAllDocsQuery()
        self.searcher = IndexSearcher(self.directory, True)
        scoreDocs = self.searcher.search(self.allBooks, 50).scoreDocs
        self.numAllBooks = len(scoreDocs)

    def testTermRangeFilter(self):

        filter = TermRangeFilter("title2", "d", "j", True, True)
        scoreDocs = self.searcher.search(self.allBooks, filter, 50).scoreDocs
        self.assertEqual(3, len(scoreDocs))

    def testNumericDateFilter(self):

        filter = NumericRangeFilter.newIntRange("pubmonth",
                                                Integer(198805),
                                                Integer(198810),
                                                True, True)
        scoreDocs = self.searcher.search(self.allBooks, filter, 50).scoreDocs
        self.assertEqual(1, len(scoreDocs))

    def testFieldCacheRangeFilter(self):

        filter = FieldCacheRangeFilter.newStringRange("title2", "d", "j",
                                                      True, True)
        scoreDocs = self.searcher.search(self.allBooks, filter, 50).scoreDocs
        self.assertEqual(3, len(scoreDocs))

        filter = FieldCacheRangeFilter.newIntRange("pubmonth",
                                                   Integer(198805),
                                                   Integer(198810),
                                                   True, True)
        scoreDocs = self.searcher.search(self.allBooks, filter, 50).scoreDocs
        self.assertEqual(1, len(scoreDocs))

    def testFieldCacheTermsFilter(self):

        filter = FieldCacheTermsFilter("category",
                                       ["/health/alternative/chinese",
                                        "/technology/computers/ai",
                                        "/technology/computers/programming"])
        scoreDocs = self.searcher.search(self.allBooks, filter, 50).scoreDocs
        self.assertEqual(7, len(scoreDocs), "expected 7 hits")

    def testQueryWrapperFilter(self):

        categoryQuery = TermQuery(Term("category", "/philosophy/eastern"))
        categoryFilter = QueryWrapperFilter(categoryQuery)
        scoreDocs = self.searcher.search(self.allBooks, categoryFilter, 50).scoreDocs
        self.assertEqual(1, len(scoreDocs), "only tao te ching")

    def testSpanQueryFilter(self):
        
        categoryQuery = TermQuery(Term("category", "/philosophy/eastern"))
        categoryFilter = QueryWrapperFilter(categoryQuery)
        scoreDocs = self.searcher.search(self.allBooks, categoryFilter, 50).scoreDocs
        self.assertEqual(1, len(scoreDocs), "only tao te ching")

    def testFilterAlternative(self):

        categoryQuery = TermQuery(Term("category", "/philosophy/eastern"))

        constrainedQuery = BooleanQuery()
        constrainedQuery.add(self.allBooks, BooleanClause.Occur.MUST)
        constrainedQuery.add(categoryQuery, BooleanClause.Occur.MUST)

        scoreDocs = self.searcher.search(constrainedQuery, 50).scoreDocs
        self.assertEqual(1, len(scoreDocs), "only tao te ching")

    def testPrefixFilter(self):

        prefixFilter = PrefixFilter(Term("category", "/technology/computers"))
        scoreDocs = self.searcher.search(self.allBooks, prefixFilter, 50).scoreDocs
        self.assertEqual(8, len(scoreDocs),
                         "only /technology/computers/* books")

    def testCachingWrapper(self):

        filter = TermRangeFilter("title2", "d", "j", True, True)
        cachingFilter = CachingWrapperFilter(filter)
        scoreDocs = self.searcher.search(self.allBooks, cachingFilter, 50).scoreDocs
        self.assertEqual(3, len(scoreDocs))
