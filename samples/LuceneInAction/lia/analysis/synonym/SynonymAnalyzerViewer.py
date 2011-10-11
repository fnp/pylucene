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


from lia.analysis.AnalyzerUtils import AnalyzerUtils
from lia.analysis.synonym.WordNetSynonymEngine import WordNetSynonymEngine
from lia.analysis.synonym.SynonymAnalyzer import SynonymAnalyzer


class SynonymAnalyzerViewer(object):

    def main(cls, argv):

        engine = WordNetSynonymEngine(argv[1])

        text = "The quick brown fox jumps over the lazy dogs"
        AnalyzerUtils.displayTokensWithPositions(SynonymAnalyzer(engine), text)

        text = "\"Oh, we get both kinds - country AND western!\" - B.B."
        AnalyzerUtils.displayTokensWithPositions(SynonymAnalyzer(engine), text)

    main = classmethod(main)
