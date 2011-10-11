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

import time, threading
from unittest import TestCase, main
from lucene import *


class PyLuceneThreadTestCase(TestCase):
    """
    Test using threads in PyLucene with python threads
    """

    def setUp(self):

        self.classLoader = Thread.currentThread().getContextClassLoader()

        self.directory = RAMDirectory()
        writer = IndexWriter(self.directory,
                             StandardAnalyzer(Version.LUCENE_CURRENT), True,
                             IndexWriter.MaxFieldLength.LIMITED)

        doc1 = Document()
        doc2 = Document()
        doc3 = Document()
        doc4 = Document()
        doc1.add(Field("field", "one",
                       Field.Store.YES, Field.Index.ANALYZED))
        doc2.add(Field("field", "two",
                       Field.Store.YES, Field.Index.ANALYZED))
        doc3.add(Field("field", "three",
                       Field.Store.YES, Field.Index.ANALYZED))
        doc4.add(Field("field", "one",
                       Field.Store.YES, Field.Index.ANALYZED))

        writer.addDocument(doc1)
        writer.addDocument(doc2)
        writer.addDocument(doc3)
        writer.addDocument(doc4)
        writer.optimize()
        writer.close()

        self.testData = [('one',2), ('two',1), ('three', 1), ('five', 0)] * 500
        self.lock = threading.Lock()
        self.totalQueries = 0


    def tearDown(self):

        self.directory.close()


    def testWithMainThread(self):
        """ warm up test for runSearch in main thread """

        self.runSearch(2000, True)


    def testWithPyLuceneThread(self):
        """ Run 5 threads with 2000 queries each """

        threads = []
        for i in xrange(5):
            threads.append(threading.Thread(target=self.runSearch,
                                            args=(2000,)))

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        # we survived!

        # and all queries have ran successfully
        self.assertEqual(10000, self.totalQueries)


    def runSearch(self, runCount, mainThread=False):
        """ search for runCount number of times """

        # problem: if there are any assertion errors in the child
        #   thread, the calling thread is not notified and may still
        #   consider the test case pass. We are using self.totalQueries
        #   to double check that work has actually been done.

        if not mainThread:
            getVMEnv().attachCurrentThread()
        time.sleep(0.5)

        searcher = IndexSearcher(self.directory, True)
        try:
            self.query = PhraseQuery()
            for word, count in self.testData[0:runCount]:
                query = TermQuery(Term("field", word))
                topDocs = searcher.search(query, 50)
                self.assertEqual(topDocs.totalHits, count)

                self.lock.acquire()
                self.totalQueries += 1
                self.lock.release()
        finally:
            searcher.close()


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
