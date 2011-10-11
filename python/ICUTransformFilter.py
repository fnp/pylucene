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
#  Port of java/org/apache/lucene/analysis/icu/ICUTransformFilter.java
#  using IBM's C++ ICU wrapped by PyICU (http://pyicu.osafoundation.org)
#
#  A TokenFilter that transforms text with ICU.
#
#  ICU provides text-transformation functionality via its Transliteration API.
#  Although script conversion is its most common use, a Transliterator can
#  actually perform a more general class of tasks. In fact, Transliterator
#  defines a very general API which specifies only that a segment of the input
#  text is replaced by new text. The particulars of this conversion are
#  determined entirely by subclasses of Transliterator.
#
#  Some useful transformations for search are built-in:
#   - Conversion from Traditional to Simplified Chinese characters
#   - Conversion from Hiragana to Katakana
#   - Conversion from Fullwidth to Halfwidth forms.
#   - Script conversions, for example Serbian Cyrillic to Latin
#
#  Example usage: <blockquote>stream = new ICUTransformFilter(stream,
#  Transliterator.getInstance("Traditional-Simplified"));</blockquote>
#
#  For more details, see the ICU User Guide at:
#  http://userguide.icu-project.org/transforms/general
#
# ====================================================================

from lucene import PythonTokenFilter, CharTermAttribute
from icu import Transliterator, UTransPosition


class ICUTransformFilter(PythonTokenFilter):

    # Create a new ICUTransformFilter that transforms text on the given
    # stream.
    #  
    #  @param input {@link TokenStream} to filter.
    #  @param transform Transliterator to transform the text.

    def __init__(self, input, transform):

        super(ICUTransformFilter, self).__init__(input)

        # Reusable position object
        self.position = UTransPosition()

        # term attribute, will be updated with transformed text.
        self.termAtt = self.addAttribute(CharTermAttribute.class_)

        self.input = input
        self.transform = transform

    def incrementToken(self):

        if self.input.incrementToken():
            text = self.termAtt.toString()
            length = len(text)

            self.position.start = 0
            self.position.limit = length
            self.position.contextStart = 0
            self.position.contextLimit = length

            text = self.transform.filteredTransliterate(text, self.position,
                                                        False)
            self.termAtt.setEmpty()
            self.termAtt.append(text)
            
            return True

        return False
