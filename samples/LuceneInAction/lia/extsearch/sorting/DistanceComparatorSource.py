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

from math import sqrt
from lucene import SortField, Term, IndexReader, FieldCache, \
    PythonFieldComparatorSource, PythonFieldComparator, Double

#
# A FieldComparatorSource implementation
#

class DistanceComparatorSource(PythonFieldComparatorSource):

    def __init__(self, x, y):
        super(DistanceComparatorSource, self).__init__()

        self.x = x
        self.y = y

    def newComparator(self, fieldName, numHits, sortPos, reversed):

        class DistanceScoreDocLookupComparator(PythonFieldComparator):

            def __init__(_self, fieldName, numHits):
                super(DistanceScoreDocLookupComparator, _self).__init__()
                _self.values = [0.0] * numHits
                _self.fieldName = fieldName

            def setNextReader(_self, reader, docBase):
      
                _self.xDoc = FieldCache.DEFAULT.getInts(reader, "x")
                _self.yDoc = FieldCache.DEFAULT.getInts(reader, "y")

            def _getDistance(_self, doc):

                deltax = _self.xDoc[doc] - self.x
                deltay = _self.yDoc[doc] - self.y

                return sqrt(deltax * deltax + deltay * deltay)

            def compare(_self, slot1, slot2):

                if _self.values[slot1] < _self.values[slot2]:
                    return -1
                if _self.values[slot1] > _self.values[slot2]:
                    return 1

                return 0

            def setBottom(_self, slot):

                _self._bottom = _self.values[slot]

            def compareBottom(_self, doc):

                docDistance = _self._getDistance(doc)
                if _self._bottom < docDistance:
                    return -1
                if _self._bottom > docDistance:
                     return 1

                return 0

            def copy(_self, slot, doc):

                _self.values[slot] = _self._getDistance(doc)

            def value(_self, slot):

                return Double(_self.values[slot])

            def sortType(_self):
                return SortField.CUSTOM

        return DistanceScoreDocLookupComparator(fieldName, numHits)

    def __str__(self):

        return "Distance from (" + self.x + "," + self.y + ")"
