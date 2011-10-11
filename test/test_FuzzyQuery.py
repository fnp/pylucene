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


class FuzzyQueryTestCase(TestCase):
    """
    Unit tests ported from Java Lucene
    """

    def _addDoc(self, text, writer):

        doc = Document()
        doc.add(Field("field", text,
                      Field.Store.YES, Field.Index.ANALYZED))
        writer.addDocument(doc)

    def testDefaultFuzziness(self):

        directory = RAMDirectory()
        writer = IndexWriter(directory, WhitespaceAnalyzer(), True,
                             IndexWriter.MaxFieldLength.LIMITED)
        self._addDoc("aaaaa", writer)
        self._addDoc("aaaab", writer)
        self._addDoc("aaabb", writer)
        self._addDoc("aabbb", writer)
        self._addDoc("abbbb", writer)
        self._addDoc("bbbbb", writer)
        self._addDoc("ddddd", writer)
        writer.optimize()
        writer.close()

        searcher = IndexSearcher(directory, True)

        query = FuzzyQuery(Term("field", "aaaaa"))
        topDocs = searcher.search(query, 50)
        self.assertEqual(3, topDocs.totalHits)

        # not similar enough:
        query = FuzzyQuery(Term("field", "xxxxx"))
        topDocs = searcher.search(query, 50)
        self.assertEqual(0, topDocs.totalHits)
        # edit distance to "aaaaa" = 3
        query = FuzzyQuery(Term("field", "aaccc"))
        topDocs = searcher.search(query, 50)
        self.assertEqual(0, topDocs.totalHits)

        # query identical to a word in the index:
        query = FuzzyQuery(Term("field", "aaaaa"))
        scoreDocs = searcher.search(query, 50).scoreDocs
        self.assertEqual(3, len(scoreDocs))
        self.assertEqual(searcher.doc(scoreDocs[0].doc).get("field"), "aaaaa")
        # default allows for up to two edits:
        self.assertEqual(searcher.doc(scoreDocs[1].doc).get("field"), "aaaab")
        self.assertEqual(searcher.doc(scoreDocs[2].doc).get("field"), "aaabb")

        # query similar to a word in the index:
        query = FuzzyQuery(Term("field", "aaaac"))
        scoreDocs = searcher.search(query, 50).scoreDocs
        self.assertEqual(3, len(scoreDocs))
        self.assertEqual(searcher.doc(scoreDocs[0].doc).get("field"), "aaaaa")
        self.assertEqual(searcher.doc(scoreDocs[1].doc).get("field"), "aaaab")
        self.assertEqual(searcher.doc(scoreDocs[2].doc).get("field"), "aaabb")

        query = FuzzyQuery(Term("field", "ddddX"))
        scoreDocs = searcher.search(query, 50).scoreDocs
        self.assertEqual(1, len(scoreDocs))
        self.assertEqual(searcher.doc(scoreDocs[0].doc).get("field"), "ddddd")

        # different field = no match:
        query = FuzzyQuery(Term("anotherfield", "ddddX"))
        topDocs = searcher.search(query, 50)
        self.assertEqual(0, topDocs.totalHits)

        searcher.close()
        directory.close()

    def testDefaultFuzzinessLong(self):

        directory = RAMDirectory()
        writer = IndexWriter(directory, WhitespaceAnalyzer(), True,
                             IndexWriter.MaxFieldLength.LIMITED)
        self._addDoc("aaaaaaa", writer)
        self._addDoc("segment", writer)
        writer.optimize()
        writer.close()
        searcher = IndexSearcher(directory, True)

        # not similar enough:
        query = FuzzyQuery(Term("field", "xxxxx"))
        topDocs = searcher.search(query, 50)
        self.assertEqual(0, topDocs.totalHits)
        # edit distance to "aaaaaaa" = 3, this matches because
        # the string is longer than
        # in testDefaultFuzziness so a bigger difference is allowed:
        query = FuzzyQuery(Term("field", "aaaaccc"))
        scoreDocs = searcher.search(query, 50).scoreDocs
        self.assertEqual(1, len(scoreDocs))
        self.assertEqual(searcher.doc(scoreDocs[0].doc).get("field"), "aaaaaaa")

        # no match, more than half of the characters is wrong:
        query = FuzzyQuery(Term("field", "aaacccc"))
        topDocs = searcher.search(query, 50)
        self.assertEqual(0, topDocs.totalHits)

        # "student" and "stellent" are indeed similar to "segment" by default:
        query = FuzzyQuery(Term("field", "student"))
        topDocs = searcher.search(query, 50)
        self.assertEqual(1, topDocs.totalHits)
        query = FuzzyQuery(Term("field", "stellent"))
        topDocs = searcher.search(query, 50)
        self.assertEqual(1, topDocs.totalHits)

        searcher.close()
        directory.close()


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
