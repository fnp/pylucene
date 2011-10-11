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
     LowerCaseFilter, StopFilter, Version, \
     StandardAnalyzer, StandardTokenizer, StandardFilter, PythonAnalyzer

from lia.analysis.synonym.SynonymFilter import SynonymFilter

#
# An Analyzer extension
#

class SynonymAnalyzer(PythonAnalyzer):

    def __init__(self, engine):

        super(SynonymAnalyzer, self).__init__()
        self.engine = engine

    def tokenStream(self, fieldName, reader):

        tokenStream = LowerCaseFilter(StandardFilter(StandardTokenizer(Version.LUCENE_CURRENT, reader)))
        tokenStream = StopFilter(True, tokenStream,
                                 StandardAnalyzer.STOP_WORDS_SET)
        
        return SynonymFilter(tokenStream, self.engine)
