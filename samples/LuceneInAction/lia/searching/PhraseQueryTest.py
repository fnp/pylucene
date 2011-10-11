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

from unittest import TestCase

from lucene import \
     WhitespaceAnalyzer, Document, Field, IndexWriter, Term, \
     IndexSearcher, PhraseQuery, RAMDirectory


class PhraseQueryTest(TestCase):

    def setUp(self):

        # set up sample document
        directory = RAMDirectory()
        writer = IndexWriter(directory, WhitespaceAnalyzer(), True,
                             IndexWriter.MaxFieldLength.UNLIMITED)
        doc = Document()
        doc.add(Field("field", "the quick brown fox jumped over the lazy dog",
                       Field.Store.YES, Field.Index.ANALYZED))
        writer.addDocument(doc)
        writer.close()

        self.searcher = IndexSearcher(directory)

    def matched(self, phrase, slop):

        query = PhraseQuery()
        query.setSlop(slop)

        for word in phrase:
            query.add(Term("field", word))

        topDocs = self.searcher.search(query, 50)

        return topDocs.totalHits > 0

    def testSlopComparison(self):

        phrase = ["quick", "fox"]

        self.assert_(not self.matched(phrase, 0), "exact phrase not found")
        self.assert_(self.matched(phrase, 1), "close enough")

    def testReverse(self):

        phrase = ["fox", "quick"]

        self.assert_(not self.matched(phrase, 2), "hop flop")
        self.assert_(self.matched(phrase, 3), "hop hop slop")

    def testMultiple(self):

        self.assert_(not self.matched(["quick", "jumped", "lazy"], 3),
                     "not close enough")

        self.assert_(self.matched(["quick", "jumped", "lazy"], 4),
                     "just enough")

        self.assert_(not self.matched(["lazy", "jumped", "quick"], 7),
                     "almost but not quite")

        self.assert_(self.matched(["lazy", "jumped", "quick"], 8),
                     "bingo")
