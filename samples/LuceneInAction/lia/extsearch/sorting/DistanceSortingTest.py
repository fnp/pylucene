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

from math import sqrt
from unittest import TestCase

from lucene import \
     WhitespaceAnalyzer, IndexSearcher, Term, TermQuery, RAMDirectory, \
     Document, Field, IndexWriter, Sort, SortField, FieldDoc, Double

from lia.extsearch.sorting.DistanceComparatorSource import \
     DistanceComparatorSource


class DistanceSortingTest(TestCase):

    def setUp(self):

        self.directory = RAMDirectory()
        writer = IndexWriter(self.directory, WhitespaceAnalyzer(), True,
                             IndexWriter.MaxFieldLength.UNLIMITED)

        self.addPoint(writer, "El Charro", "restaurant", 1, 2)
        self.addPoint(writer, "Cafe Poca Cosa", "restaurant", 5, 9)
        self.addPoint(writer, "Los Betos", "restaurant", 9, 6)
        self.addPoint(writer, "Nico's Taco Shop", "restaurant", 3, 8)

        writer.close()

        self.searcher = IndexSearcher(self.directory, True)
        self.query = TermQuery(Term("type", "restaurant"))

    def addPoint(self, writer, name, type, x, y):

        doc = Document()
        doc.add(Field("name", name, Field.Store.YES, Field.Index.NOT_ANALYZED))
        doc.add(Field("type", type, Field.Store.YES, Field.Index.NOT_ANALYZED))
        doc.add(Field("x", str(x), Field.Store.YES,
                      Field.Index.NOT_ANALYZED_NO_NORMS))
        doc.add(Field("y", str(y), Field.Store.YES,
                      Field.Index.NOT_ANALYZED_NO_NORMS));

        writer.addDocument(doc)

    def testNearestRestaurantToHome(self):

        sort = Sort(SortField("location", DistanceComparatorSource(0, 0)))

        scoreDocs = self.searcher.search(self.query, None, 50, sort).scoreDocs
        self.assertEqual("El Charro", self.searcher.doc(scoreDocs[0].doc).get("name"), "closest")
        self.assertEqual("Los Betos", self.searcher.doc(scoreDocs[3].doc).get("name"), "furthest")

    def testNeareastRestaurantToWork(self):

        sort = Sort(SortField("location", DistanceComparatorSource(10, 10)))

        docs = self.searcher.search(self.query, None, 3, sort)
        self.assertEqual(4, docs.totalHits)
        self.assertEqual(3, len(docs.scoreDocs))

        fieldDoc = FieldDoc.cast_(docs.scoreDocs[0])
        distance = Double.cast_(fieldDoc.fields[0]).doubleValue()

        self.assertEqual(sqrt(17), distance,
                         "(10,10) -> (9,6) = sqrt(17)")

        document = self.searcher.doc(fieldDoc.doc)
        self.assertEqual("Los Betos", document["name"])

        self.dumpDocs(sort, docs)

    def dumpDocs(self, sort, docs):

        print "Sorted by:", sort

        for scoreDoc in docs.scoreDocs:
            fieldDoc = FieldDoc.cast_(scoreDoc)
            distance = Double.cast_(fieldDoc.fields[0]).doubleValue()
            doc = self.searcher.doc(fieldDoc.doc)
            print "  %(name)s @ (%(location)s) ->" %doc, distance
