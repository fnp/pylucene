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


class CachingWrapperFilterTestCase(TestCase):
    """
    Unit tests ported from Java Lucene
    """

    def testCachingWorks(self):

        dir = RAMDirectory()
        writer = IndexWriter(dir, StandardAnalyzer(Version.LUCENE_CURRENT),
                             True, IndexWriter.MaxFieldLength.LIMITED)
        writer.close()

        reader = IndexReader.open(dir, True)

        class mockFilter(PythonFilter):
            def __init__(self):
                super(mockFilter, self).__init__()
                self._wasCalled = False
            def getDocIdSet(self, reader):
                self._wasCalled = True;
                return DocIdBitSet(BitSet())
            def clear(self):
                self._wasCalled = False
            def wasCalled(self):
                return self._wasCalled

        filter = mockFilter()
        cacher = CachingWrapperFilter(filter)

        # first time, nested filter is called
        cacher.getDocIdSet(reader)
        self.assert_(filter.wasCalled(), "first time")

        # second time, nested filter should not be called
        filter.clear()
        cacher.getDocIdSet(reader)
        self.assert_(not filter.wasCalled(), "second time")

        reader.close()


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
