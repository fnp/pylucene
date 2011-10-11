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
     WhitespaceAnalyzer, IndexSearcher, RAMDirectory, \
     Document, Field, IndexWriter, TermQuery, SpanNearQuery

from lia.extsearch.queryparser.NumberUtils import NumberUtils
from lia.extsearch.queryparser.CustomQueryParser import \
    MultiFieldCustomQueryParser, CustomQueryParser


class AdvancedQueryParserTest(TestCase):

    def setUp(self):

        self.analyzer = WhitespaceAnalyzer()
        self.directory = RAMDirectory()

        writer = IndexWriter(self.directory, self.analyzer, True, 
                             IndexWriter.MaxFieldLength.LIMITED)

        for i in xrange(1, 501):
            doc = Document()
            doc.add(Field("id", NumberUtils.pad(i),
                          Field.Store.YES, Field.Index.NOT_ANALYZED))
            writer.addDocument(doc)

        writer.close()

    def testCustomQueryParser(self):

        parser = CustomQueryParser("field", self.analyzer)

        try:
            parser.parse("a?t")
            self.fail("Wildcard queries should not be allowed")
        except:
            # expected
            self.assert_(True)

        try:
            parser.parse("xunit~")
            self.fail("Fuzzy queries should not be allowed")
        except:
            # expected
            self.assert_(True)

    def testCustomMultiFieldQueryParser(self):

        parser = MultiFieldCustomQueryParser(["field"], self.analyzer)

        try:
            parser.parse("a?t")
            self.fail("Wildcard queries should not be allowed")
        except:
            # expected
            self.assert_(True)

        try:
            parser.parse("xunit~")
            self.fail("Fuzzy queries should not be allowed")
        except:
            # expected
            self.assert_(True)

    def testIdRangeQuery(self):

        parser = CustomQueryParser("field", self.analyzer)

        query = parser.parse("id:[37 TO 346]")
        self.assertEqual("id:[0000000037 TO 0000000346]",
                         query.toString("field"), "padded")

        searcher = IndexSearcher(self.directory, True)
        scoreDocs = searcher.search(query, 1000).scoreDocs
        self.assertEqual(310, len(scoreDocs))

        print parser.parse("special:[term TO *]")
        print parser.parse("special:[* TO term]")

    def testPhraseQuery(self):

        parser = CustomQueryParser("field", self.analyzer)

        query = parser.parse("singleTerm")
        self.assert_(TermQuery.instance_(query), "TermQuery")

        query = parser.parse("\"a phrase\"")
        self.assert_(SpanNearQuery.instance_(query), "SpanNearQuery")
