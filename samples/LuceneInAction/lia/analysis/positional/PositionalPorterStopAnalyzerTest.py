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
     IndexWriter, Term, RAMDirectory, Document, Field, \
     IndexSearcher, QueryParser, Version

from lia.analysis.AnalyzerUtils import AnalyzerUtils
from lia.analysis.positional.PositionalPorterStopAnalyzer import \
     PositionalPorterStopAnalyzer


class PositionalPorterStopAnalyzerTest(TestCase):

    porterAnalyzer = PositionalPorterStopAnalyzer()
    
    def setUp(self):

        self.directory = RAMDirectory()
        writer = IndexWriter(self.directory, self.porterAnalyzer, True,
                             IndexWriter.MaxFieldLength.UNLIMITED)

        doc = Document()
        doc.add(Field("contents",
                      "The quick brown fox jumps over the lazy dogs",
                       Field.Store.YES, Field.Index.ANALYZED))
        writer.addDocument(doc)
        writer.close()

    def testStems(self):
        
        searcher = IndexSearcher(self.directory)
        query = QueryParser(Version.LUCENE_CURRENT, "contents",
                            self.porterAnalyzer).parse("laziness")
        topDocs = searcher.search(query, 50)

        self.assertEqual(1, topDocs.totalHits, "lazi")

        query = QueryParser(Version.LUCENE_CURRENT, "contents",
                            self.porterAnalyzer).parse('"fox jumped"')
        topDocs = searcher.search(query, 50)

        self.assertEqual(1, topDocs.totalHits, "jump jumps jumped jumping")

    def testExactPhrase(self):

        searcher = IndexSearcher(self.directory, True)
        query = QueryParser(Version.LUCENE_24, "contents",
                            self.porterAnalyzer).parse('"over the lazy"')
        topDocs = searcher.search(query, 50)

        self.assertEqual(0, topDocs.totalHits, "exact match not found!")

    def testWithSlop(self):

        searcher = IndexSearcher(self.directory, True)

        parser = QueryParser(Version.LUCENE_CURRENT, "contents",
                             self.porterAnalyzer)
        parser.setPhraseSlop(1)

        query = parser.parse('"over the lazy"')
        topDocs = searcher.search(query, 50)

        self.assertEqual(1, topDocs.totalHits, "hole accounted for")

    def main(cls):

        text = "The quick brown fox jumps over the lazy dogs"
        AnalyzerUtils.displayTokensWithPositions(cls.porterAnalyzer, text)
        print ''
        
    main = classmethod(main)
