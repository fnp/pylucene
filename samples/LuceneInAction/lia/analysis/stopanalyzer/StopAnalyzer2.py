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

from lucene import \
     LetterTokenizer, LowerCaseFilter, StopAnalyzer, StopFilter

#
# An Analyzer extension
#

class StopAnalyzer2(object):

    def __init__(self, stopWords=None):

        if stopWords is None:
            self.stopWords = StopAnalyzer.ENGLISH_STOP_WORDS_SET
        else:
            self.stopWords = stopWords

    def tokenStream(self, fieldName, reader):

        return StopFilter(True, LowerCaseFilter(LetterTokenizer(reader)),
                          self.stopWords)
