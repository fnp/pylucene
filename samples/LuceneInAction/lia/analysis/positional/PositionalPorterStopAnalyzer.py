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

import sys

from lucene import \
     LowerCaseTokenizer, PorterStemFilter, StopAnalyzer, StopFilter, \
     TokenStream, PythonAnalyzer

from lia.analysis.positional.PositionalStopFilter import PositionalStopFilter

python_ver = '%d.%d.%d' %(sys.version_info[0:3])
if python_ver < '2.4':
    from sets import Set as set


#
# An Analyzer extension
#

class PositionalPorterStopAnalyzer(PythonAnalyzer):

    def __init__(self, stopWords=None):

        super(PositionalPorterStopAnalyzer, self).__init__()

        if stopWords is None:
            self.stopWords = StopAnalyzer.ENGLISH_STOP_WORDS_SET
        else:
            self.stopWords = set(stopWords)

    def tokenStream(self, fieldName, reader):

        stopFilter = StopFilter(True, LowerCaseTokenizer(reader),
                                self.stopWords)
        stopFilter.setEnablePositionIncrements(True)

        return PorterStemFilter(stopFilter)
