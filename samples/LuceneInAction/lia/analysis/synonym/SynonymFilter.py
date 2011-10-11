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

from lucene import Token, PythonTokenFilter, TermAttribute
from lia.analysis.AnalyzerUtils import AnalyzerUtils

#
# A TokenFilter extension
#

class SynonymFilter(PythonTokenFilter):
    TOKEN_TYPE_SYNONYM = "SYNONYM"

    def __init__(self, inStream, engine):
        super(SynonymFilter, self).__init__(inStream)

        self.synonymStack = []
        self.termAttr = self.addAttribute(TermAttribute.class_)
        self.save = inStream.cloneAttributes()
        self.engine = engine
        self.inStream = inStream

    def incrementToken(self):

        if len(self.synonymStack) > 0:
            syn = self.synonymStack.pop()
            self.restoreState(syn)
            return True

        if not self.inStream.incrementToken():
            return False

        self.addAliasesToStack()

        return True

    def addAliasesToStack(self):

        synonyms = self.engine.getSynonyms(self.termAttr.term())
        if synonyms is None:
            return

        current = self.captureState()

        for synonym in synonyms:
            self.save.restoreState(current)
            AnalyzerUtils.setTerm(self.save, synonym)
            AnalyzerUtils.setType(self.save, self.TOKEN_TYPE_SYNONYM)
            AnalyzerUtils.setPositionIncrement(self.save, 0)
            self.synonymStack.append(self.save.captureState())
