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

from unittest import TestCase
from lucene import SnowballAnalyzer, StringReader, Version
from lia.analysis.AnalyzerUtils import AnalyzerUtils


class SnowballTest(TestCase):

    def testEnglish(self):

        analyzer = SnowballAnalyzer(Version.LUCENE_CURRENT, "English")
        AnalyzerUtils.assertAnalyzesTo(analyzer, "stemming algorithms",
                                       ["stem", "algorithm"])

    def testSpanish(self):

        analyzer = SnowballAnalyzer(Version.LUCENE_CURRENT, "Spanish")
        AnalyzerUtils.assertAnalyzesTo(analyzer, "algoritmos", ["algoritm"])
