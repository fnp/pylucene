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
from lucene import StopAnalyzer, Version
from lia.analysis.AnalyzerUtils import AnalyzerUtils


class StopAnalyzerTest(TestCase):

    def setUp(self):

        self.stopAnalyzer = StopAnalyzer(Version.LUCENE_CURRENT)

    def testHoles(self):
        
        expected = ["one", "enough"]

        AnalyzerUtils.assertAnalyzesTo(self.stopAnalyzer, "one is not enough",
                                       expected)
        AnalyzerUtils.assertAnalyzesTo(self.stopAnalyzer, "one is enough",
                                       expected)
        AnalyzerUtils.assertAnalyzesTo(self.stopAnalyzer, "one enough",
                                       expected)
        AnalyzerUtils.assertAnalyzesTo(self.stopAnalyzer, "one but not enough",
                                       expected)
