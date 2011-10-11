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
     WhitespaceAnalyzer, Document, Field, IndexWriter, Term, \
     QueryWrapperFilter, RAMDirectory, IndexSearcher, TermQuery


class SecurityFilterTest(TestCase):

    def setUp(self):

        self.directory = RAMDirectory()
        writer = IndexWriter(self.directory, WhitespaceAnalyzer(), True,
                             IndexWriter.MaxFieldLength.UNLIMITED)

        # Elwood
        document = Document()
        document.add(Field("owner", "elwood",
                           Field.Store.YES, Field.Index.NOT_ANALYZED))
        document.add(Field("keywords", "elwoods sensitive info",
                           Field.Store.YES, Field.Index.ANALYZED))
        writer.addDocument(document)

        # Jake
        document = Document()
        document.add(Field("owner", "jake",
                           Field.Store.YES, Field.Index.NOT_ANALYZED))
        document.add(Field("keywords", "jakes sensitive info",
                           Field.Store.YES, Field.Index.ANALYZED))
        writer.addDocument(document)

        writer.close()

    def testSecurityFilter(self):

        query = TermQuery(Term("keywords", "info"))

        searcher = IndexSearcher(self.directory, True)
        topDocs = searcher.search(query, 50)
        self.assertEqual(2, topDocs.totalHits, "Both documents match")

        jakeFilter = QueryWrapperFilter(TermQuery(Term("owner", "jake")))

        scoreDocs = searcher.search(query, jakeFilter, 50).scoreDocs
        self.assertEqual(1, len(scoreDocs))
        self.assertEqual("jakes sensitive info",
                         searcher.doc(scoreDocs[0].doc).get("keywords"),
                         "elwood is safe")
