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

import sys, unittest
from lucene import *


# Originally intended to demonstrate a memory leak.  See
# http://lists.osafoundation.org/pipermail/pylucene-dev/2008-October/002937.html
# and followup

class QueryRewriteTest(unittest.TestCase):

    def setUp(self):

        store = RAMDirectory()
        writer = IndexWriter(store, StandardAnalyzer(Version.LUCENE_CURRENT),
                             True, IndexWriter.MaxFieldLength.LIMITED)
        writer.close()
        self.reader = IndexSearcher(store, True).getIndexReader()
        self.term = Term('all', 'foo')
        
    def testQuery(self):

        base_query = TermQuery(self.term)
        new_query = base_query.rewrite(self.reader)

        self.assertEquals(base_query, new_query)
    

if __name__ == "__main__":
    env = initVM()
    if '-loop' in sys.argv:
        sys.argv.remove('-loop')
        while True:
            try:
                unittest.main()
            except:
                pass
    else:
        unittest.main()
