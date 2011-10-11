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

from lucene import PythonTokenFilter

#
# A TokenFilter extension
#

class PositionalStopFilter(PythonTokenFilter):

    def __init__(self, tokenStream, stopWords):

        super(PositionalStopFilter, self).__init__(tokenStream)

        self.input = tokenStream
        self.stopWords = stopWords

    def next(self):

        increment = 0

        for token in self.input:
            if not token.termText() in self.stopWords:
                token.setPositionIncrement(token.getPositionIncrement() +
                                           increment)
                return token

            increment += 1

        return None
