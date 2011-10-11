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

from unittest import TestCase, main
from lucene import *


class PerFieldAnalyzerTestCase(TestCase):
    """
    Unit tests ported from Java Lucene
    """

    def testPerField(self):

        text = "Qwerty"
        analyzer = PerFieldAnalyzerWrapper(WhitespaceAnalyzer())
        analyzer.addAnalyzer("special", SimpleAnalyzer())

        tokenStream = analyzer.tokenStream("field", StringReader(text))
        termAtt = tokenStream.getAttribute(TermAttribute.class_)

        self.assert_(tokenStream.incrementToken())
        self.assertEqual("Qwerty", termAtt.term(),
                         "WhitespaceAnalyzer does not lowercase")

        tokenStream = analyzer.tokenStream("special", StringReader(text))
        termAtt = tokenStream.getAttribute(TermAttribute.class_)
        self.assert_(tokenStream.incrementToken())
        self.assertEqual("qwerty", termAtt.term(),
                         "SimpleAnalyzer lowercases")


if __name__ == "__main__":
    import sys, lucene
    lucene.initVM()
    if '-loop' in sys.argv:
        sys.argv.remove('-loop')
        while True:
            try:
                main()
            except:
                pass
    else:
         main()
