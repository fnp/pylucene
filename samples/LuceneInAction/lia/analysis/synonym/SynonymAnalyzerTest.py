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
     StandardAnalyzer, RAMDirectory, IndexWriter, Term, Document, Field, \
     IndexSearcher, TermQuery, PhraseQuery, QueryParser, StringReader, \
     TermAttribute, PositionIncrementAttribute, Version

from lia.analysis.AnalyzerUtils import AnalyzerUtils
from lia.analysis.synonym.SynonymAnalyzer import SynonymAnalyzer
from lia.analysis.synonym.MockSynonymEngine import MockSynonymEngine


class SynonymAnalyzerTest(TestCase):

    synonymAnalyzer = SynonymAnalyzer(MockSynonymEngine())

    def setUp(self):

        self.directory = RAMDirectory()
        writer = IndexWriter(self.directory, self.synonymAnalyzer, True,
                             IndexWriter.MaxFieldLength.UNLIMITED)

        doc = Document()
        doc.add(Field("content",
                      "The quick brown fox jumps over the lazy dogs",
                      Field.Store.YES, Field.Index.ANALYZED))
        writer.addDocument(doc)
        writer.close()

        self.searcher = IndexSearcher(self.directory, True)

    def tearDown(self):

        self.searcher.close()

    def testJumps(self):

        stream = self.synonymAnalyzer.tokenStream("contents",
                                                  StringReader("jumps"))
        term = stream.addAttribute(TermAttribute.class_)
        posIncr = stream.addAttribute(PositionIncrementAttribute.class_)

        i = 0
        expected = ["jumps", "hops", "leaps"]
        while stream.incrementToken():
            self.assertEqual(expected[i], term.term())
            if i == 0:
                expectedPos = 1
            else:
                expectedPos = 0

            self.assertEqual(expectedPos, posIncr.getPositionIncrement())
            i += 1

        self.assertEqual(3, i)

    def testSearchByAPI(self):

        tq = TermQuery(Term("content", "hops"))
        topDocs = self.searcher.search(tq, 50)
        self.assertEqual(1, topDocs.totalHits)

        pq = PhraseQuery()
        pq.add(Term("content", "fox"))
        pq.add(Term("content", "hops"))
        topDocs = self.searcher.search(pq, 50)
        self.assertEquals(1, topDocs.totalHits)

    def testWithQueryParser(self):

        query = QueryParser(Version.LUCENE_CURRENT, "content",
                            self.synonymAnalyzer).parse('"fox jumps"')
        topDocs = self.searcher.search(query, 50)
        # in Lucene 1.9, position increments are no longer ignored
        self.assertEqual(1, topDocs.totalHits, "!!!! what?!")

        query = QueryParser(Version.LUCENE_CURRENT, "content",
                            StandardAnalyzer(Version.LUCENE_CURRENT)).parse('"fox jumps"')
        topDocs = self.searcher.search(query, 50)
        self.assertEqual(1, topDocs.totalHits, "*whew*")

    def main(cls):

        query = QueryParser(Version.LUCENE_CURRENT, "content",
                            cls.synonymAnalyzer).parse('"fox jumps"')
        print "\"fox jumps\" parses to ", query.toString("content")

        print "From AnalyzerUtils.tokensFromAnalysis: "
        AnalyzerUtils.displayTokens(cls.synonymAnalyzer, "\"fox jumps\"")
        print ''
        
    main = classmethod(main)
