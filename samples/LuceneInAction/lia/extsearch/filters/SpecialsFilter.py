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

from lucene import \
    IndexReader, Term, BitSet, PythonFilter, JArray, OpenBitSet

#
# A Filter extension, with a TermDocs wrapper working around the lack of
# support for returning values in array arguments.
#
class SpecialsFilter(PythonFilter):

    def __init__(self, accessor):
        
        super(SpecialsFilter, self).__init__()
        self.accessor = accessor

    def getDocIdSet(self, reader):

        bits = OpenBitSet(long(reader.maxDoc()))
        isbns = self.accessor.isbns()

        docs = JArray(int)(1)
        freqs = JArray(int)(1)

        for isbn in isbns:
            if isbn is not None:
                termDocs = reader.termDocs(Term("isbn", isbn))
                count = termDocs.read(docs, freqs)
                if count == 1:
                    bits.set(long(docs[0]))

        return bits

    def __str__():

        return "SpecialsFilter"
