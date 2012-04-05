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


# Test reusableTokenStream, using ReusableAnalyzerBase:
class MyDeletionPolicy(PythonIndexDeletionPolicy):

    onInitCalled = False
    onCommitCalled = False
    
    def onInit(self, commits):
      self.onInitCalled = True

    def onCommit(self, commits):
      self.onCommitCalled = True
    

class IndexDeletionPolicyTestCase(TestCase):

    def testIndexDeletionPolicy(self):

        dir = RAMDirectory()
        config = IndexWriterConfig(Version.LUCENE_CURRENT,
                                   WhitespaceAnalyzer())
        policy = MyDeletionPolicy()
        config.setIndexDeletionPolicy(policy)
        writer = IndexWriter(dir, config)
        # no commits exist in the index yet
        self.assertFalse(policy.onInitCalled)
        # we haven't called commit yet
        self.assertFalse(policy.onCommitCalled)
        doc = Document()
        writer.addDocument(doc)
        writer.commit()

        # now we called commit
        self.assertTrue(policy.onCommitCalled)

        # external IR sees 1 commit:
        self.assertEquals(1, IndexReader.listCommits(dir).size())

        # commit again:
        writer.addDocument(doc)
        writer.commit()

        # external IR sees 2 commits:
        self.assertEquals(2, IndexReader.listCommits(dir).size())

        writer.close()

        # open same index, make sure both commits survived:
        config = IndexWriterConfig(Version.LUCENE_CURRENT,
                                   WhitespaceAnalyzer())
        policy = MyDeletionPolicy()
        config.setIndexDeletionPolicy(policy)
        writer = IndexWriter(dir, config)
        self.assertTrue(policy.onInitCalled)
        self.assertFalse(policy.onCommitCalled)
        self.assertEquals(2, IndexReader.listCommits(dir).size())
        writer.close()

        self.assertEquals(2, IndexReader.listCommits(dir).size())

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
