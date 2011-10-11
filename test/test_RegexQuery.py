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


class TestRegexQuery(TestCase):

    FN = "field"

    def setUp(self):

        directory = RAMDirectory()

        writer = IndexWriter(directory, SimpleAnalyzer(), True,
                             IndexWriter.MaxFieldLength.LIMITED)
        doc = Document()
        doc.add(Field(self.FN, "the quick brown fox jumps over the lazy dog", Field.Store.NO, Field.Index.ANALYZED))
        writer.addDocument(doc)
        writer.optimize()
        writer.close()
        self.searcher = IndexSearcher(directory, True)

    def tearDown(self):

        self.searcher.close()

    def newTerm(self, value):
  
        return Term(self.FN, value)

    def regexQueryNrHits(self, regex):

        query = RegexQuery(self.newTerm(regex))

        return self.searcher.search(query, 50).totalHits

    def spanRegexQueryNrHits(self, regex1, regex2, slop, ordered):

        srq1 = SpanRegexQuery(self.newTerm(regex1))
        srq2 = SpanRegexQuery(self.newTerm(regex2))
        query = SpanNearQuery([srq1, srq2], slop, ordered)

        return self.searcher.search(query, 50).totalHits

    def testRegex1(self):

        self.assertEqual(1, self.regexQueryNrHits("^q.[aeiou]c.*$"))

    def testRegex2(self):

        self.assertEqual(0, self.regexQueryNrHits("^.[aeiou]c.*$"))

    def testRegex3(self):

        self.assertEqual(0, self.regexQueryNrHits("^q.[aeiou]c$"))

    def testSpanRegex1(self):

        self.assertEqual(1, self.spanRegexQueryNrHits("^q.[aeiou]c.*$",
                                                      "dog", 6, True))

    def testSpanRegex2(self):

        self.assertEqual(0, self.spanRegexQueryNrHits("^q.[aeiou]c.*$",
                                                      "dog", 5, True))


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
