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
from lucene import StopAnalyzer

from lia.analysis.AnalyzerUtils import AnalyzerUtils
from lia.analysis.stopanalyzer.StopAnalyzerFlawed import StopAnalyzerFlawed
from lia.analysis.stopanalyzer.StopAnalyzer2 import StopAnalyzer2


class StopAnalyzerAlternativeTest(TestCase):

    def testStopAnalyzer2(self):

        AnalyzerUtils.assertAnalyzesTo(StopAnalyzer2(),
                                       "The quick brown...",
                                       ["quick", "brown"])

    def testStopAnalyzerFlawed(self):

        AnalyzerUtils.assertAnalyzesTo(StopAnalyzerFlawed(),
                                       "The quick brown...",
                                       ["the", "quick", "brown"])


    #
    # Illustrates that "the" is not removed, although it is lowercased
    #

    def main(cls):

        AnalyzerUtils.displayTokens(StopAnalyzerFlawed(),
                                    "The quick brown...")

    main = classmethod(main)
