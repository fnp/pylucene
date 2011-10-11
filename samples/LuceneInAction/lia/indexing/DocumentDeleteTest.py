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

from lucene import IndexWriter, IndexReader
from lia.indexing.BaseIndexingTestCase import BaseIndexingTestCase


class DocumentDeleteTest(BaseIndexingTestCase):

    def testDeleteBeforeIndexMerge(self):

        reader = IndexReader.open(self.dir, False)
        self.assertEqual(2, reader.maxDoc())
        self.assertEqual(2, reader.numDocs())
        reader.deleteDocument(1)

        self.assert_(reader.isDeleted(1))
        self.assert_(reader.hasDeletions())
        self.assertEqual(2, reader.maxDoc())
        self.assertEqual(1, reader.numDocs())

        reader.close()

        reader = IndexReader.open(self.dir, True)

        self.assertEqual(2, reader.maxDoc())
        self.assertEqual(1, reader.numDocs())

        reader.close()

    def testDeleteAfterIndexMerge(self):

        reader = IndexReader.open(self.dir, False)
        self.assertEqual(2, reader.maxDoc())
        self.assertEqual(2, reader.numDocs())
        reader.deleteDocument(1)
        reader.close()

        writer = IndexWriter(self.dir, self.getAnalyzer(), False,
                             IndexWriter.MaxFieldLength.UNLIMITED)
        writer.optimize()
        writer.close()

        reader = IndexReader.open(self.dir, True)

        self.assert_(not reader.isDeleted(1))
        self.assert_(not reader.hasDeletions())
        self.assertEqual(1, reader.maxDoc())
        self.assertEqual(1, reader.numDocs())

        reader.close()
