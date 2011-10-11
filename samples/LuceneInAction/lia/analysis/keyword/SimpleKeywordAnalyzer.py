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

#
# CharTokenizer limits token width to 255 characters, though.
# This implementation assumes keywords are 255 in length or less.
#

from lucene import PythonAnalyzer, PythonCharTokenizer


class SimpleKeywordAnalyzer(PythonAnalyzer):

    def tokenStream(self, fieldName, reader):

        class charTokenizer(PythonCharTokenizer):
            def __init__(self, reader):
                super(charTokenizer, self).__init__(reader)
            def isTokenChar(self, c):
                return True
            def normalize(self, c):
                return c
        
        return charTokenizer(reader)
