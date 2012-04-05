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


# Test reusableTokenStream, using ReusableAnalyzerBase:
class MyAnalyzer(PythonReusableAnalyzerBase):

    def initReader(self, reader):
        return reader

    def createComponents(self, field, reader):

        first = LowerCaseTokenizer(Version.LUCENE_CURRENT, reader)
        last = StopFilter(Version.LUCENE_CURRENT, first,
                          StopAnalyzer.ENGLISH_STOP_WORDS_SET)

        return ReusableAnalyzerBase.TokenStreamComponents(first, last)


class ReusableAnalyzerBaseTestCase(TestCase):

    def testReusable(self):

        analyzer = MyAnalyzer()

        for method in (analyzer.reusableTokenStream, analyzer.tokenStream):
            for x in xrange(2):
                reader = StringReader("This is a test of the english stop analyzer")
                stream = method("test", reader)

                termAtt = stream.getAttribute(TermAttribute.class_)
                count = 0
                while stream.incrementToken():
                    self.assert_(termAtt.term() not in StopAnalyzer.ENGLISH_STOP_WORDS_SET)
                    count += 1
                self.assertEquals(4, count)


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
