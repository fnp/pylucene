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
    QueryParser, StandardAnalyzer, PerFieldAnalyzerWrapper, \
    WhitespaceAnalyzer, Version


class AnalysisParalysisTest(LiaTestCase):

    def testAnalyzer(self):

        analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
        queryString = "category:/philosophy/eastern"

        parser = QueryParser(Version.LUCENE_CURRENT, "contents", analyzer)
        parser.setAutoGeneratePhraseQueries(True)
        query = parser.parse(queryString)

        self.assertEqual("category:\"philosophy eastern\"",
                         query.toString("contents"), "path got split, yikes!")

        perFieldAnalyzer = PerFieldAnalyzerWrapper(analyzer)
        perFieldAnalyzer.addAnalyzer("category", WhitespaceAnalyzer())
        query = QueryParser(Version.LUCENE_CURRENT,
                            "contents", perFieldAnalyzer).parse(queryString)

        self.assertEqual("category:/philosophy/eastern",
                         query.toString("contents"),
                         "leave category field alone")
