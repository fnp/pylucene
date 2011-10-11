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

from lia.common.LiaTestCase import LiaTestCase

from lucene import \
     WhitespaceAnalyzer, StandardAnalyzer, Term, QueryParser, Locale, \
     BooleanQuery, FuzzyQuery, IndexSearcher, TermRangeQuery, TermQuery, \
     BooleanClause, Version


class QueryParserTest(LiaTestCase):

    def setUp(self):

        super(QueryParserTest, self).setUp()
        self.analyzer = WhitespaceAnalyzer()
        self.searcher = IndexSearcher(self.directory, True)

    def testToString(self):

        query = BooleanQuery()
        query.add(FuzzyQuery(Term("field", "kountry")),
                  BooleanClause.Occur.MUST)
        query.add(TermQuery(Term("title", "western")),
                  BooleanClause.Occur.SHOULD)

        self.assertEqual("+kountry~0.5 title:western",
                         query.toString("field"), "both kinds")

    def testPrefixQuery(self):

        parser = QueryParser(Version.LUCENE_CURRENT, "category",
                             StandardAnalyzer(Version.LUCENE_CURRENT))
        parser.setLowercaseExpandedTerms(False)

        print parser.parse("/Computers/technology*").toString("category")

    def testGrouping(self):

        query = QueryParser(Version.LUCENE_CURRENT, "subject",
                            self.analyzer).parse("(agile OR extreme) AND methodology")
        scoreDocs = self.searcher.search(query, 50).scoreDocs

        self.assertHitsIncludeTitle(self.searcher, scoreDocs,
                                    "Extreme Programming Explained")
        self.assertHitsIncludeTitle(self.searcher, scoreDocs,
                                    "The Pragmatic Programmer")

    def testTermRangeQuery(self):

        query = QueryParser(Version.LUCENE_CURRENT, "subject",
                            self.analyzer).parse("title2:[K TO N]")
        self.assert_(TermRangeQuery.instance_(query))

        scoreDocs = self.searcher.search(query, 10).scoreDocs
        self.assertHitsIncludeTitle(self.searcher, scoreDocs, "Mindstorms")

        query = QueryParser(Version.LUCENE_CURRENT, "subject",
                            self.analyzer).parse("title2:{K TO Mindstorms}")
        scoreDocs = self.searcher.search(query, 10).scoreDocs
        self.assertHitsIncludeTitle(self.searcher, scoreDocs, "Mindstorms",
                                    True)

    def testDateRangeQuery(self):

        # locale diff between jre and gcj 1/1/04 -> 01/01/04
        # expression = "modified:[1/1/04 TO 12/31/04]"
        
        expression = "modified:[01/01/04 TO 12/31/04]"
        parser = QueryParser(Version.LUCENE_CURRENT, "subject", self.analyzer)
        parser.setLocale(Locale.US)
        query = parser.parse(expression)
        print expression, "parsed to", query

        topDocs = self.searcher.search(query, 50)
        self.assert_(topDocs.totalHits > 0)

    def testSlop(self):

        q = QueryParser(Version.LUCENE_CURRENT, "field",
                        self.analyzer).parse('"exact phrase"')
        self.assertEqual("\"exact phrase\"", q.toString("field"),
                         "zero slop")

        qp = QueryParser(Version.LUCENE_CURRENT, "field", self.analyzer)
        qp.setPhraseSlop(5)
        q = qp.parse('"sloppy phrase"')
        self.assertEqual("\"sloppy phrase\"~5", q.toString("field"),
                         "sloppy, implicitly")

    def testPhraseQuery(self):

        analyzer = StandardAnalyzer(Version.LUCENE_24)
        q = QueryParser(Version.LUCENE_24, "field",
                        analyzer).parse('"This is Some Phrase*"')
        self.assertEqual("\"some phrase\"", q.toString("field"), "analyzed")

        q = QueryParser(Version.LUCENE_CURRENT, "field",
                        self.analyzer).parse('"term"')
        self.assert_(TermQuery.instance_(q), "reduced to TermQuery")

    def testLowercasing(self):

        q = QueryParser(Version.LUCENE_CURRENT, "field",
                        self.analyzer).parse("PrefixQuery*")
        self.assertEqual("prefixquery*", q.toString("field"), "lowercased")

        qp = QueryParser(Version.LUCENE_CURRENT, "field", self.analyzer)
        qp.setLowercaseExpandedTerms(False)
        q = qp.parse("PrefixQuery*")
        self.assertEqual("PrefixQuery*", q.toString("field"), "not lowercased")

    def testWildcard(self):

        try:
            QueryParser(Version.LUCENE_CURRENT, "field",
                        self.analyzer).parse("*xyz")
            self.fail("Leading wildcard character should not be allowed")
        except:
            self.assert_(True)

    def testBoost(self):

         q = QueryParser(Version.LUCENE_CURRENT, "field",
                         self.analyzer).parse("term^2")
         self.assertEqual("term^2.0", q.toString("field"))

    def testParseException(self):

        try:
            QueryParser(Version.LUCENE_CURRENT, "contents",
                        self.analyzer).parse("^&#")
        except:
            # expression is invalid, as expected
            self.assert_(True)
        else:
            self.fail("ParseException expected, but not thrown")
