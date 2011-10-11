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
#  Port of java/org/apache/lucene/analysis/icu/ICUFoldingFilter.java
#  using IBM's C++ ICU wrapped by PyICU (http://pyicu.osafoundation.org)

try:
    from icu import Normalizer2, UNormalizationMode2
except ImportError, e:
    pass

from unittest import main
from BaseTokenStreamTestCase import BaseTokenStreamTestCase

from lucene import *


class TestICUFoldingFilter(BaseTokenStreamTestCase):

    def testDefaults(self):

        from lucene.ICUFoldingFilter import ICUFoldingFilter

        class _analyzer(PythonAnalyzer):
            def tokenStream(_self, fieldName, reader):
                return ICUFoldingFilter(WhitespaceTokenizer(Version.LUCENE_CURRENT, reader))

        a = _analyzer()

        # case folding
        self._assertAnalyzesTo(a, "This is a test",
                               [ "this", "is", "a", "test" ])

        # case folding
        self._assertAnalyzesTo(a, u"Ruß", [ "russ" ])
    
        # case folding with accent removal
        self._assertAnalyzesTo(a, u"ΜΆΪΟΣ", [ u"μαιοσ" ])
        self._assertAnalyzesTo(a, u"Μάϊος", [ u"μαιοσ" ])

        # supplementary case folding
        self._assertAnalyzesTo(a, u"𐐖", [ u"𐐾" ])
    
        # normalization
        self._assertAnalyzesTo(a, u"ﴳﴺﰧ", [ u"طمطمطم" ])

        # removal of default ignorables
        self._assertAnalyzesTo(a, u"क्‍ष", [ u"कष" ])
    
        # removal of latin accents (composed)
        self._assertAnalyzesTo(a, u"résumé", [ "resume" ])
    
        # removal of latin accents (decomposed)
        self._assertAnalyzesTo(a, u"re\u0301sume\u0301", [ u"resume" ])
    
        # fold native digits
        self._assertAnalyzesTo(a, u"৭০৬", [ "706" ])
    
        # ascii-folding-filter type stuff
        self._assertAnalyzesTo(a, u"đis is cræzy", [ "dis", "is", "craezy" ])


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
