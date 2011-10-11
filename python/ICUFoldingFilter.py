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
#
#  A TokenFilter that applies search term folding to Unicode text,
#  applying foldings from UTR#30 Character Foldings.
#
#  This filter applies the following foldings from the report to unicode text:
#
#  Accent removal
#  Case folding
#  Canonical duplicates folding
#  Dashes folding
#  Diacritic removal (including stroke, hook, descender)
#  Greek letterforms folding
#  Han Radical folding
#  Hebrew Alternates folding
#  Jamo folding
#  Letterforms folding
#  Math symbol folding
#  Multigraph Expansions: All
#  Native digit folding
#  No-break folding
#  Overline folding
#  Positional forms folding
#  Small forms folding
#  Space folding
#  Spacing Accents folding
#  Subscript folding
#  Superscript folding
#  Suzhou Numeral folding
#  Symbol folding
#  Underline folding
#  Vertical forms folding
#  Width folding
#
#  Additionally, Default Ignorables are removed, and text is normalized to NFKC.
#  All foldings, case folding, and normalization mappings are applied
#  recursively to ensure a fully folded and normalized result.
#
# ====================================================================

import os, lucene

from lucene.ICUNormalizer2Filter import ICUNormalizer2Filter
from icu import ResourceBundle, Normalizer2, UNormalizationMode2

utr30 = os.path.join(lucene.__dir__, 'resources',
                     'org', 'apache', 'lucene', 'analysis', 'icu',
                     'utr30.dat')
ResourceBundle.setAppData("utr30", utr30)


class ICUFoldingFilter(ICUNormalizer2Filter):

    def __init__(self, input):

        normalizer = Normalizer2.getInstance("utr30", "utr30",
                                             UNormalizationMode2.COMPOSE)
        super(ICUFoldingFilter, self).__init__(input, normalizer)
