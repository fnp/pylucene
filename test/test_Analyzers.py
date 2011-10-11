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

from unittest import main
from BaseTokenStreamTestCase import BaseTokenStreamTestCase
from lucene import *


class AnalyzersTestCase(BaseTokenStreamTestCase):
    """
    Unit tests ported from Java Lucene
    """

    def testSimple(self):

        a = SimpleAnalyzer()
        self._assertAnalyzesTo(a, "foo bar FOO BAR", 
                               [ "foo", "bar", "foo", "bar" ])
        self._assertAnalyzesTo(a, "foo      bar .  FOO <> BAR", 
                               [ "foo", "bar", "foo", "bar" ])
        self._assertAnalyzesTo(a, "foo.bar.FOO.BAR", 
                               [ "foo", "bar", "foo", "bar" ])
        self._assertAnalyzesTo(a, "U.S.A.", 
                               [ "u", "s", "a" ])
        self._assertAnalyzesTo(a, "C++", 
                               [ "c" ])
        self._assertAnalyzesTo(a, "B2B", 
                               [ "b", "b" ])
        self._assertAnalyzesTo(a, "2B", 
                               [ "b" ])
        self._assertAnalyzesTo(a, "\"QUOTED\" word", 
                               [ "quoted", "word" ])


    def testNull(self):

        a = WhitespaceAnalyzer()
        self._assertAnalyzesTo(a, "foo bar FOO BAR", 
                               [ "foo", "bar", "FOO", "BAR" ])
        self._assertAnalyzesTo(a, "foo      bar .  FOO <> BAR", 
                               [ "foo", "bar", ".", "FOO", "<>", "BAR" ])
        self._assertAnalyzesTo(a, "foo.bar.FOO.BAR", 
                               [ "foo.bar.FOO.BAR" ])
        self._assertAnalyzesTo(a, "U.S.A.", 
                               [ "U.S.A." ])
        self._assertAnalyzesTo(a, "C++", 
                               [ "C++" ])
        self._assertAnalyzesTo(a, "B2B", 
                               [ "B2B" ])
        self._assertAnalyzesTo(a, "2B", 
                               [ "2B" ])
        self._assertAnalyzesTo(a, "\"QUOTED\" word", 
                               [ "\"QUOTED\"", "word" ])

    def testStop(self):

        a = StopAnalyzer(Version.LUCENE_CURRENT)
        self._assertAnalyzesTo(a, "foo bar FOO BAR", 
                               [ "foo", "bar", "foo", "bar" ])
        self._assertAnalyzesTo(a, "foo a bar such FOO THESE BAR", 
                               [ "foo", "bar", "foo", "bar" ])

    def _verifyPayload(self, ts):

        payloadAtt = ts.getAttribute(PayloadAttribute.class_)
        b = 0
        while True:
            b += 1
            if not ts.incrementToken():
                break
            self.assertEqual(b, payloadAtt.getPayload().toByteArray()[0])

    # Make sure old style next() calls result in a new copy of payloads
    def testPayloadCopy(self):

        s = "how now brown cow"
        ts = WhitespaceTokenizer(StringReader(s))
        ts = PayloadSetter(ts)
        self._verifyPayload(ts)

        ts = WhitespaceTokenizer(StringReader(s))
        ts = PayloadSetter(ts)
        self._verifyPayload(ts)


class PayloadSetter(PythonTokenFilter):

    def __init__(self, input):
        super(PayloadSetter, self).__init__(input)

        self.input = input
        self.payloadAtt = self.addAttribute(PayloadAttribute.class_)
        self.data = JArray('byte')(1)
        self.p = Payload(self.data, 0, 1)

    def incrementToken(self):

        if not self.input.incrementToken():
            return False

        self.payloadAtt.setPayload(self.p)
        self.data[0] += 1;

        return True


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
