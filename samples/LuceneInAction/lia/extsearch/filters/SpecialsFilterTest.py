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
from lia.extsearch.filters.TestSpecialsAccessor import TestSpecialsAccessor
from lia.extsearch.filters.SpecialsFilter import SpecialsFilter

from lucene import \
     WildcardQuery, FilteredQuery, TermQuery, BooleanQuery, TermRangeQuery, \
     IndexSearcher, Term, BooleanClause, MatchAllDocsQuery


class SpecialsFilterTest(LiaTestCase):

    def setUp(self):

        super(SpecialsFilterTest, self).setUp()

        self.allBooks = MatchAllDocsQuery()
        self.searcher = IndexSearcher(self.directory, True)

    def testCustomFilter(self):

        isbns = ["0060812451", "0465026567"]
        accessor = TestSpecialsAccessor(isbns)
        
        filter = SpecialsFilter(accessor)
        topDocs = self.searcher.search(self.allBooks, filter, 50)
        self.assertEquals(len(isbns), topDocs.totalHits, "the specials")

    def testFilteredQuery(self):
        
        isbns = ["0854402624"]  # Steiner

        accessor = TestSpecialsAccessor(isbns)
        filter = SpecialsFilter(accessor)

        educationBooks = WildcardQuery(Term("category", "*education*"))
        edBooksOnSpecial = FilteredQuery(educationBooks, filter)

        logoBooks = TermQuery(Term("subject", "logo"))

        logoOrEdBooks = BooleanQuery()
        logoOrEdBooks.add(logoBooks, BooleanClause.Occur.SHOULD)
        logoOrEdBooks.add(edBooksOnSpecial, BooleanClause.Occur.SHOULD)

        topDocs = self.searcher.search(logoOrEdBooks, 50)
        print logoOrEdBooks
        self.assertEqual(2, topDocs.totalHits, "Papert and Steiner")
