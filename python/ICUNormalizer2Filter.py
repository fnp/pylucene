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
#
#  Normalize token text with ICU's {@link com.ibm.icu.text.Normalizer2}
#
#  With this filter, you can normalize text in the following ways:
#   - NFKC Normalization, Case Folding, and removing Ignorables (the default)
#   - Using a standard Normalization mode (NFC, NFD, NFKC, NFKD)
#   - Based on rules from a custom normalization mapping.
#
#  If you use the defaults, this filter is a simple way to standardize
#  Unicode text in a language-independent way for search:
#   - The case folding that it does can be seen as a replacement for
#     LowerCaseFilter: For example, it handles cases such as the Greek
#     sigma, so that "Μάϊος" and "ΜΆΪΟΣ" will match correctly.
#   - The normalization will standardizes different forms of the same 
#     character in Unicode. For example, CJK full-width numbers will be
#     standardized to their ASCII forms.
#   - Ignorables such as Zero-Width Joiner and Variation Selectors are
#     removed. These are typically modifier characters that affect display.
#
# ====================================================================

from lucene import PythonTokenFilter, CharTermAttribute
from icu import Normalizer2, UNormalizationMode2, UNormalizationCheckResult


class ICUNormalizer2Filter(PythonTokenFilter):

    def __init__(self, input, normalizer=None):
        super(ICUNormalizer2Filter, self).__init__(input)

        self.input = input
        self.termAtt = self.addAttribute(CharTermAttribute.class_);

        if normalizer is None:
            normalizer = Normalizer2.getInstance(None, "nfkc_cf", UNormalizationMode2.COMPOSE)
        self.normalizer = normalizer

    def incrementToken(self):

        if self.input.incrementToken():
            text = self.termAtt.toString()

            if self.normalizer.quickCheck(text) != UNormalizationCheckResult.YES:
                self.termAtt.setEmpty()
                self.termAtt.append(self.normalizer.normalize(text))
                
            return True

        return False
