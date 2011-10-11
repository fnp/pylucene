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


class BooleanPrefixQueryTestCase(TestCase):
    """
    Unit tests ported from Java Lucene
    """

    def getCount(self, r,  q):

        if BooleanQuery.instance_(q):
            return len(BooleanQuery.cast_(q).getClauses())
        elif ConstantScoreQuery.instance_(q):
            iter = ConstantScoreQuery.cast_(q).getFilter().getDocIdSet(r).iterator()
            count = 0
            while iter.nextDoc() != DocIdSetIterator.NO_MORE_DOCS:
                count += 1

            return count
        else:
            self.fail("unexpected query " + q)

    def testMethod(self):

        directory = RAMDirectory()
        categories = ["food", "foodanddrink", "foodanddrinkandgoodtimes",
                      "food and drink"]

        try:
            writer = IndexWriter(directory, WhitespaceAnalyzer(), True,
                                 IndexWriter.MaxFieldLength.LIMITED)
            for category in categories:
                doc = Document()
                doc.add(Field("category", category, Field.Store.YES,
                              Field.Index.NOT_ANALYZED))
                writer.addDocument(doc)

            writer.close()
      
            reader = IndexReader.open(directory, True)
            query = PrefixQuery(Term("category", "foo"))
            rw1 = query.rewrite(reader)
      
            bq = BooleanQuery()
            bq.add(query, BooleanClause.Occur.MUST)
      
            rw2 = bq.rewrite(reader)
        except Exception, e:
            self.fail(e)

        self.assertEqual(self.getCount(reader, rw1), self.getCount(reader, rw2),
                         "Number of Clauses Mismatch")


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
