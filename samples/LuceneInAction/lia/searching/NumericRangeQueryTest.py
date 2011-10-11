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

from lucene import Integer, \
    IndexSearcher, NumericRangeQuery

from lia.common.LiaTestCase import LiaTestCase


class NumericRangeQueryTest(LiaTestCase):

    def testInclusive(self):

        searcher = IndexSearcher(self.directory, True)
        # pub date of TTC was October 1988
        query = NumericRangeQuery.newIntRange("pubmonth",
                                              Integer(198805),
                                              Integer(198810),
                                              True, True)

        topDocs = searcher.search(query, 100)
        self.assertEqual(1, topDocs.totalHits)
        searcher.close()

    def testExclusive(self):

        searcher = IndexSearcher(self.directory, True)
        # pub date of TTC was October 1988
        query = NumericRangeQuery.newIntRange("pubmonth",
                                              Integer(198805),
                                              Integer(198810),
                                              False, False)
        topDocs = searcher.search(query, 100)
        self.assertEqual(0, topDocs.totalHits)
        searcher.close()
