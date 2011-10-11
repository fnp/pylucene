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

import os

from unittest import TestCase

from lucene import VERSION, \
     IndexWriter, IndexReader, SimpleAnalyzer, SimpleFSDirectory, System, File


class LockTest(TestCase):

    def setUp(self):

        indexDir = os.path.join(System.getProperty("java.io.tmpdir", "tmp"),
                                "index")
        self.rmdir(indexDir)
        self.dir = SimpleFSDirectory(File(indexDir))

    def rmdir(self, dir):

        for dir, dirnames, filenames in os.walk(dir):
            for filename in filenames:
                os.remove(os.path.join(dir, filename))
            for dirname in dirnames:
                os.rmdir(os.path.join(dir, dirname))

    def testWriteLock(self):

        writer1 = IndexWriter(self.dir, SimpleAnalyzer(),
                              IndexWriter.MaxFieldLength.UNLIMITED)
        writer2 = None

        try:
            try:
                writer2 = IndexWriter(self.dir, SimpleAnalyzer(),
                                      IndexWriter.MaxFieldLength.UNLIMITED)
                self.fail("We should never reach this point")
            except:
                pass
        finally:
            writer1.close()
            self.assert_(writer2 is None)
