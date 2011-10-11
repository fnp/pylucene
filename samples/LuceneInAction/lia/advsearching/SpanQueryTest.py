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
from cStringIO import StringIO

from lucene import \
     WhitespaceAnalyzer, Document, Field, IndexReader, IndexWriter, Term, \
     IndexSearcher, PhraseQuery, SpanFirstQuery, SpanNearQuery, SpanNotQuery, \
     SpanOrQuery, SpanTermQuery, RAMDirectory, TermAttribute, StringReader

from lia.analysis.AnalyzerUtils import AnalyzerUtils


class SpanQueryTest(TestCase):

    def setUp(self):

        self.directory = RAMDirectory()
        self.analyzer = WhitespaceAnalyzer()

        writer = IndexWriter(self.directory, self.analyzer, True,
                             IndexWriter.MaxFieldLength.UNLIMITED)

        doc = Document()
        doc.add(Field("f", "the quick brown fox jumps over the lazy dog",
                      Field.Store.YES, Field.Index.ANALYZED))
        writer.addDocument(doc)

        doc = Document()
        doc.add(Field("f", "the quick red fox jumps over the sleepy cat",
                      Field.Store.YES, Field.Index.ANALYZED))
        writer.addDocument(doc)

        writer.close()

        self.searcher = IndexSearcher(self.directory, True)
        self.reader = IndexReader.open(self.directory, True)

        self.quick = SpanTermQuery(Term("f", "quick"))
        self.brown = SpanTermQuery(Term("f", "brown"))
        self.red = SpanTermQuery(Term("f", "red"))
        self.fox = SpanTermQuery(Term("f", "fox"))
        self.lazy = SpanTermQuery(Term("f", "lazy"))
        self.sleepy = SpanTermQuery(Term("f", "sleepy"))
        self.dog = SpanTermQuery(Term("f", "dog"))
        self.cat = SpanTermQuery(Term("f", "cat"))

    def assertOnlyBrownFox(self, query):

        topDocs = self.searcher.search(query, 50)
        self.assertEqual(1, topDocs.totalHits)
        self.assertEqual(0, topDocs.scoreDocs[0].doc, "wrong doc")

    def assertBothFoxes(self, query):

        topDocs = self.searcher.search(query, 50)
        self.assertEqual(2, topDocs.totalHits)

    def assertNoMatches(self, query):

        topDocs = self.searcher.search(query, 50)
        self.assertEquals(0, topDocs.totalHits)

    def testSpanTermQuery(self):

        self.assertOnlyBrownFox(self.brown)
        self.dumpSpans(self.brown)

    def testSpanFirstQuery(self):

        sfq = SpanFirstQuery(self.brown, 2)
        self.assertNoMatches(sfq)

        self.dumpSpans(sfq)

        sfq = SpanFirstQuery(self.brown, 3)
        self.dumpSpans(sfq)
        self.assertOnlyBrownFox(sfq)

    def testSpanNearQuery(self):

        quick_brown_dog = [self.quick, self.brown, self.dog]
        snq = SpanNearQuery(quick_brown_dog, 0, True)
        self.assertNoMatches(snq)
        self.dumpSpans(snq)

        snq = SpanNearQuery(quick_brown_dog, 4, True)
        self.assertNoMatches(snq)
        self.dumpSpans(snq)

        snq = SpanNearQuery(quick_brown_dog, 5, True)
        self.assertOnlyBrownFox(snq)
        self.dumpSpans(snq)

        # interesting - even a sloppy phrase query would require
        # more slop to match
        snq = SpanNearQuery([self.lazy, self.fox], 3, False)
        self.assertOnlyBrownFox(snq)
        self.dumpSpans(snq)

        pq = PhraseQuery()
        pq.add(Term("f", "lazy"))
        pq.add(Term("f", "fox"))
        pq.setSlop(4)
        self.assertNoMatches(pq)

        pq.setSlop(5)
        self.assertOnlyBrownFox(pq)

    def testSpanNotQuery(self):

        quick_fox = SpanNearQuery([self.quick, self.fox], 1, True)
        self.assertBothFoxes(quick_fox)
        self.dumpSpans(quick_fox)

        quick_fox_dog = SpanNotQuery(quick_fox, self.dog)
        self.assertBothFoxes(quick_fox_dog)
        self.dumpSpans(quick_fox_dog)

        no_quick_red_fox = SpanNotQuery(quick_fox, self.red)
        self.assertOnlyBrownFox(no_quick_red_fox)
        self.dumpSpans(no_quick_red_fox)

    def testSpanOrQuery(self):

        quick_fox = SpanNearQuery([self.quick, self.fox], 1, True)
        lazy_dog = SpanNearQuery([self.lazy, self.dog], 0, True)
        sleepy_cat = SpanNearQuery([self.sleepy, self.cat], 0, True)
        qf_near_ld = SpanNearQuery([quick_fox, lazy_dog], 3, True)

        self.assertOnlyBrownFox(qf_near_ld)
        self.dumpSpans(qf_near_ld)

        qf_near_sc = SpanNearQuery([quick_fox, sleepy_cat], 3, True)
        self.dumpSpans(qf_near_sc)

        orQ = SpanOrQuery([qf_near_ld, qf_near_sc])
        self.assertBothFoxes(orQ)
        self.dumpSpans(orQ)

    def testPlay(self):

        orQ = SpanOrQuery([self.quick, self.fox])
        self.dumpSpans(orQ)

        quick_fox = SpanNearQuery([self.quick, self.fox], 1, True)
        sfq = SpanFirstQuery(quick_fox, 4)
        self.dumpSpans(sfq)

        self.dumpSpans(SpanTermQuery(Term("f", "the")))

        quick_brown = SpanNearQuery([self.quick, self.brown], 0, False)
        self.dumpSpans(quick_brown)

    def dumpSpans(self, query):

        spans = query.getSpans(self.reader)
        print "%s:" % query
        numSpans = 0

        scoreDocs = self.searcher.search(query, 50).scoreDocs
        scores = [0, 0]
        for scoreDoc in scoreDocs:
            scores[scoreDoc.doc] = scoreDoc.score

        while spans.next():
            numSpans += 1

            id = spans.doc()
            doc = self.reader.document(id)

            # for simplicity - assume tokens are in sequential,
            # positions, starting from 0
            stream = self.analyzer.tokenStream("contents",
                                               StringReader(doc.get("f")))
            term = stream.addAttribute(TermAttribute.class_)
      
            buffer = StringIO()
            buffer.write("   ")

            i = 0
            while stream.incrementToken():
                if i == spans.start():
                    buffer.write("<")

                buffer.write(term.term())
                if i + 1 == spans.end():
                    buffer.write(">")

                buffer.write(" ")
                i += 1
      
            buffer.write("(")
            buffer.write(str(scores[id]))
            buffer.write(") ")

            print buffer.getvalue()
            # print self.searcher.explain(query, id)

        if numSpans == 0:
            print "   No spans"

        print ''
