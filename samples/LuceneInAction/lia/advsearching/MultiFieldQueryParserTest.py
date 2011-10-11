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
    SimpleAnalyzer, MultiFieldQueryParser, IndexSearcher, BooleanClause, \
    Version


class MultiFieldQueryParserTest(LiaTestCase):

    def testDefaultOperator(self):

        SHOULD = BooleanClause.Occur.SHOULD
        query = MultiFieldQueryParser.parse(Version.LUCENE_CURRENT,
                                            "development", ["title", "subject"],
                                            [SHOULD, SHOULD],
                                            SimpleAnalyzer())

        searcher = IndexSearcher(self.directory, True)
        scoreDocs = searcher.search(query, 50).scoreDocs

        self.assertHitsIncludeTitle(searcher, scoreDocs,
                                    "Java Development with Ant")

        # has "development" in the subject field
        self.assertHitsIncludeTitle(searcher, scoreDocs,
                                    "Extreme Programming Explained")

    def testSpecifiedOperator(self):
        
        MUST = BooleanClause.Occur.MUST
        query = MultiFieldQueryParser.parse(Version.LUCENE_CURRENT,
                                            "development", ["title", "subject"],
                                            [MUST, MUST],
                                            SimpleAnalyzer())

        searcher = IndexSearcher(self.directory, True)
        scoreDocs = searcher.search(query, 50).scoreDocs

        self.assertHitsIncludeTitle(searcher, scoreDocs,
                                    "Java Development with Ant")
        self.assertEqual(1, len(scoreDocs), "one and only one")
