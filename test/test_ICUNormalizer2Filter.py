# -*- coding: utf-8 -*-
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
#  Port of java/org/apache/lucene/analysis/icu/ICUNormalizer2Filter.java
#  using IBM's C++ ICU wrapped by PyICU (http://pyicu.osafoundation.org)

try:
    from icu import Normalizer2, UNormalizationMode2
except ImportError, e:
    pass

from unittest import main
from BaseTokenStreamTestCase import BaseTokenStreamTestCase

from lucene import *


class TestICUNormalizer2Filter(BaseTokenStreamTestCase):

    def testDefaults(self):

        from lucene.ICUNormalizer2Filter import ICUNormalizer2Filter

        class analyzer(PythonAnalyzer):
            def tokenStream(_self, fieldName, reader):
                return ICUNormalizer2Filter(WhitespaceTokenizer(Version.LUCENE_CURRENT, reader))

        a = analyzer()

        # case folding
        self._assertAnalyzesTo(a, "This is a test",
                               [ "this", "is", "a", "test" ])

        # case folding
        self._assertAnalyzesTo(a, "Ruß", [ "russ" ])
    
        # case folding
        self._assertAnalyzesTo(a, u"ΜΆΪΟΣ", [ u"μάϊοσ" ])
        self._assertAnalyzesTo(a, u"Μάϊος", [ u"μάϊοσ" ])

        # supplementary case folding
        self._assertAnalyzesTo(a, u"𐐖", [ u"𐐾" ])
    
        # normalization
        self._assertAnalyzesTo(a, u"ﴳﴺﰧ", [ u"طمطمطم" ])

        # removal of default ignorables
        self._assertAnalyzesTo(a, u"क्‍ष", [ u"क्ष" ])
  
    def testAlternate(self):

        from lucene.ICUNormalizer2Filter import ICUNormalizer2Filter

        class analyzer(PythonAnalyzer):
            # specify nfc with decompose to get nfd
            def tokenStream(_self, fieldName, reader):
                return ICUNormalizer2Filter(WhitespaceTokenizer(Version.LUCENE_CURRENT, reader),
                                            Normalizer2.getInstance(None, "nfc", UNormalizationMode2.DECOMPOSE))

        a = analyzer()
        # decompose EAcute into E + combining Acute
        self._assertAnalyzesTo(a, u"\u00E9", [ u"\u0065\u0301" ])


if __name__ == "__main__":
    import sys, lucene
    try:
        import icu
    except ImportError:
        pass
    else:
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
