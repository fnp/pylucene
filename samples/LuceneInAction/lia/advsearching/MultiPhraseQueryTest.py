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
     WhitespaceAnalyzer, Document, Field, IndexWriter, Term, BooleanQuery, \
     IndexSearcher, MultiPhraseQuery, PhraseQuery, RAMDirectory, BooleanClause


class MultiPhraseQueryTest(TestCase):

    def setUp(self):

        directory = RAMDirectory()
        writer = IndexWriter(directory, WhitespaceAnalyzer(), True,
                             IndexWriter.MaxFieldLength.UNLIMITED)

        doc1 = Document()
        doc1.add(Field("field", "the quick brown fox jumped over the lazy dog",
                       Field.Store.YES, Field.Index.ANALYZED))
        writer.addDocument(doc1)

        doc2 = Document()
        doc2.add(Field("field", "the fast fox hopped over the hound",
                       Field.Store.YES, Field.Index.ANALYZED))
        writer.addDocument(doc2)
        writer.close()

        self.searcher = IndexSearcher(directory, True)

    def testBasic(self):
        
        query = MultiPhraseQuery()
        query.add([Term("field", "quick"),
                   Term("field", "fast")])
        query.add(Term("field", "fox"))
        print query

        topDocs = self.searcher.search(query, 10)
        self.assertEqual(1, topDocs.totalHits, "fast fox match")

        query.setSlop(1);
        topDocs = self.searcher.search(query, 10)
        self.assertEqual(2, topDocs.totalHits, "both match");

    def testAgainstOR(self):

        quickFox = PhraseQuery()
        quickFox.setSlop(1)
        quickFox.add(Term("field", "quick"))
        quickFox.add(Term("field", "fox"))

        fastFox = PhraseQuery()
        fastFox.add(Term("field", "fast"))
        fastFox.add(Term("field", "fox"))

        query = BooleanQuery()
        query.add(quickFox, BooleanClause.Occur.SHOULD)
        query.add(fastFox, BooleanClause.Occur.SHOULD)
        topDocs = self.searcher.search(query, 10)
        self.assertEqual(2, topDocs.totalHits)

    def debug(self, hits):

        for i, doc in hits:
            print "%s: %s" %(hits.score(i), doc['field'])
