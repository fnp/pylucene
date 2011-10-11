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


class TestBooleanQuery(TestCase):
    """
    Unit tests ported from Java Lucene
    """

    def testEquality(self):

        bq1 = BooleanQuery()
        bq1.add(TermQuery(Term("field", "value1")), BooleanClause.Occur.SHOULD)
        bq1.add(TermQuery(Term("field", "value2")), BooleanClause.Occur.SHOULD)

        nested1 = BooleanQuery()
        nested1.add(TermQuery(Term("field", "nestedvalue1")), BooleanClause.Occur.SHOULD)
        nested1.add(TermQuery(Term("field", "nestedvalue2")), BooleanClause.Occur.SHOULD)
        bq1.add(nested1, BooleanClause.Occur.SHOULD)

        bq2 = BooleanQuery()
        bq2.add(TermQuery(Term("field", "value1")), BooleanClause.Occur.SHOULD)
        bq2.add(TermQuery(Term("field", "value2")), BooleanClause.Occur.SHOULD)

        nested2 = BooleanQuery()
        nested2.add(TermQuery(Term("field", "nestedvalue1")), BooleanClause.Occur.SHOULD)
        nested2.add(TermQuery(Term("field", "nestedvalue2")), BooleanClause.Occur.SHOULD)
        bq2.add(nested2, BooleanClause.Occur.SHOULD)
        
        self.assert_(bq1.equals(bq2))


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
