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

from lucene import Term, IndexSearcher, TermRangeQuery


class TermRangeQueryTest(LiaTestCase):

    def testTermRangeQuery(self):

        searcher = IndexSearcher(self.directory, True)
        query = TermRangeQuery("title2", "d", "j", True, True)

        topDocs = searcher.search(query, 100)
        self.assertEqual(3, topDocs.totalHits)
        searcher.close()
