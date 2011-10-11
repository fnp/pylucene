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


class PhraseQueryTestCase(TestCase):
    """
    Unit tests ported from Java Lucene
    """

    def setUp(self):

        self.directory = RAMDirectory()
        writer = IndexWriter(self.directory, WhitespaceAnalyzer(), True,
                             IndexWriter.MaxFieldLength.LIMITED)
    
        doc = Document()
        doc.add(Field("field", "one two three four five",
                      Field.Store.YES, Field.Index.ANALYZED))
        writer.addDocument(doc)
    
        writer.optimize()
        writer.close()

        self.searcher = IndexSearcher(self.directory, True)
        self.query = PhraseQuery()

    def tearDown(self):

        self.searcher.close()
        self.directory.close()

    def testNotCloseEnough(self):

        self.query.setSlop(2)
        self.query.add(Term("field", "one"))
        self.query.add(Term("field", "five"))
        topDocs = self.searcher.search(self.query, 50)
        self.assertEqual(0, topDocs.totalHits)

    def testBarelyCloseEnough(self):

        self.query.setSlop(3)
        self.query.add(Term("field", "one"))
        self.query.add(Term("field", "five"))
        topDocs = self.searcher.search(self.query, 50)
        self.assertEqual(1, topDocs.totalHits)

    def testExact(self):
        """
        Ensures slop of 0 works for exact matches, but not reversed
        """

        # slop is zero by default
        self.query.add(Term("field", "four"))
        self.query.add(Term("field", "five"))
        topDocs = self.searcher.search(self.query, 50)
        self.assertEqual(1, topDocs.totalHits, "exact match")

        self.query = PhraseQuery()
        self.query.add(Term("field", "two"))
        self.query.add(Term("field", "one"))
        topDocs = self.searcher.search(self.query, 50)
        self.assertEqual(0, topDocs.totalHits, "reverse not exact")

    def testSlop1(self):

        # Ensures slop of 1 works with terms in order.
        self.query.setSlop(1)
        self.query.add(Term("field", "one"))
        self.query.add(Term("field", "two"))
        topDocs = self.searcher.search(self.query, 50)
        self.assertEqual(1, topDocs.totalHits, "in order")

        # Ensures slop of 1 does not work for phrases out of order
        # must be at least 2.
        self.query = PhraseQuery()
        self.query.setSlop(1)
        self.query.add(Term("field", "two"))
        self.query.add(Term("field", "one"))
        topDocs = self.searcher.search(self.query, 50)
        self.assertEqual(0, topDocs.totalHits, "reversed, slop not 2 or more")

    def testOrderDoesntMatter(self):
        """
        As long as slop is at least 2, terms can be reversed
        """

        self.query.setSlop(2) # must be at least two for reverse order match
        self.query.add(Term("field", "two"))
        self.query.add(Term("field", "one"))
        topDocs = self.searcher.search(self.query, 50)
        self.assertEqual(1, topDocs.totalHits, "just sloppy enough")

        self.query = PhraseQuery()
        self.query.setSlop(2)
        self.query.add(Term("field", "three"))
        self.query.add(Term("field", "one"))
        topDocs = self.searcher.search(self.query, 50)
        self.assertEqual(0, topDocs.totalHits, "not sloppy enough")

    def testMulipleTerms(self):
        """
        slop is the total number of positional moves allowed
        to line up a phrase
        """
        
        self.query.setSlop(2)
        self.query.add(Term("field", "one"))
        self.query.add(Term("field", "three"))
        self.query.add(Term("field", "five"))
        topDocs = self.searcher.search(self.query, 50)
        self.assertEqual(1, topDocs.totalHits, "two total moves")

        self.query = PhraseQuery()
        self.query.setSlop(5) # it takes six moves to match this phrase
        self.query.add(Term("field", "five"))
        self.query.add(Term("field", "three"))
        self.query.add(Term("field", "one"))
        topDocs = self.searcher.search(self.query, 50)
        self.assertEqual(0, topDocs.totalHits, "slop of 5 not close enough")

        self.query.setSlop(6)
        topDocs = self.searcher.search(self.query, 50)
        self.assertEqual(1, topDocs.totalHits, "slop of 6 just right")

    def testPhraseQueryWithStopAnalyzer(self):

        directory = RAMDirectory()
        stopAnalyzer = StopAnalyzer(Version.LUCENE_24)
        writer = IndexWriter(directory, stopAnalyzer, True,
                             IndexWriter.MaxFieldLength.LIMITED)
        doc = Document()
        doc.add(Field("field", "the stop words are here",
                      Field.Store.YES, Field.Index.ANALYZED))
        writer.addDocument(doc)
        writer.close()

        searcher = IndexSearcher(directory, True)

        # valid exact phrase query
        query = PhraseQuery()
        query.add(Term("field","stop"))
        query.add(Term("field","words"))
        topDocs = searcher.search(query, 50)
        self.assertEqual(1, topDocs.totalHits)

        # currently StopAnalyzer does not leave "holes", so this matches.
        query = PhraseQuery()
        query.add(Term("field", "words"))
        query.add(Term("field", "here"))
        topDocs = searcher.search(query, 50)
        self.assertEqual(1, topDocs.totalHits)

        searcher.close()
  
    def testPhraseQueryInConjunctionScorer(self):

        directory = RAMDirectory()
        writer = IndexWriter(directory, WhitespaceAnalyzer(), True,
                             IndexWriter.MaxFieldLength.LIMITED)
    
        doc = Document()
        doc.add(Field("source", "marketing info",
                      Field.Store.YES, Field.Index.ANALYZED,
                      Field.TermVector.YES))
        writer.addDocument(doc)
    
        doc = Document()
        doc.add(Field("contents", "foobar",
                      Field.Store.YES, Field.Index.ANALYZED,
                      Field.TermVector.YES))
        doc.add(Field("source", "marketing info",
                      Field.Store.YES, Field.Index.ANALYZED,
                      Field.TermVector.YES))
        writer.addDocument(doc)
    
        writer.optimize()
        writer.close()
    
        searcher = IndexSearcher(directory, True)
    
        phraseQuery = PhraseQuery()
        phraseQuery.add(Term("source", "marketing"))
        phraseQuery.add(Term("source", "info"))
        topDocs = searcher.search(phraseQuery, 50)
        self.assertEqual(2, topDocs.totalHits)
    
        termQuery = TermQuery(Term("contents","foobar"))
        booleanQuery = BooleanQuery()
        booleanQuery.add(termQuery, BooleanClause.Occur.MUST)
        booleanQuery.add(phraseQuery, BooleanClause.Occur.MUST)
        topDocs = searcher.search(booleanQuery, 50)
        self.assertEqual(1, topDocs.totalHits)
    
        searcher.close()
    
        writer = IndexWriter(directory, WhitespaceAnalyzer(), True,
                             IndexWriter.MaxFieldLength.LIMITED)
        doc = Document()
        doc.add(Field("contents", "map entry woo",
                      Field.Store.YES, Field.Index.ANALYZED,
                      Field.TermVector.YES))
        writer.addDocument(doc)

        doc = Document()
        doc.add(Field("contents", "woo map entry",
                      Field.Store.YES, Field.Index.ANALYZED,
                      Field.TermVector.YES))
        writer.addDocument(doc)

        doc = Document()
        doc.add(Field("contents", "map foobarword entry woo",
                      Field.Store.YES, Field.Index.ANALYZED,
                      Field.TermVector.YES))
        writer.addDocument(doc)

        writer.optimize()
        writer.close()
    
        searcher = IndexSearcher(directory, True)
    
        termQuery = TermQuery(Term("contents", "woo"))
        phraseQuery = PhraseQuery()
        phraseQuery.add(Term("contents", "map"))
        phraseQuery.add(Term("contents", "entry"))
    
        topDocs = searcher.search(termQuery, 50)
        self.assertEqual(3, topDocs.totalHits)
        topDocs = searcher.search(phraseQuery, 50)
        self.assertEqual(2, topDocs.totalHits)
    
        booleanQuery = BooleanQuery()
        booleanQuery.add(termQuery, BooleanClause.Occur.MUST)
        booleanQuery.add(phraseQuery, BooleanClause.Occur.MUST)
        topDocs = searcher.search(booleanQuery, 50)
        self.assertEqual(2, topDocs.totalHits)
    
        booleanQuery = BooleanQuery()
        booleanQuery.add(phraseQuery, BooleanClause.Occur.MUST)
        booleanQuery.add(termQuery, BooleanClause.Occur.MUST)
        topDocs = searcher.search(booleanQuery, 50)
        self.assertEqual(2, topDocs.totalHits)
    
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
