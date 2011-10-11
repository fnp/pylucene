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

import unittest
from lucene import *

class Test_Bug1842(unittest.TestCase):

    def setUp(self):

        self.analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
        self.d1 = RAMDirectory()
        
        w1 = IndexWriter(self.d1, self.analyzer, True,
                         IndexWriter.MaxFieldLength.LIMITED)
        doc1 = Document()
        doc1.add(Field("all", "blah blah blah Gesundheit",
                       Field.Store.NO, Field.Index.ANALYZED,
                       Field.TermVector.YES))
        doc1.add(Field('id', '1',
                       Field.Store.YES, Field.Index.NOT_ANALYZED))
        w1.addDocument(doc1)
        w1.optimize()
        w1.close()

    def tearDown(self):
        pass

    def test_bug1842(self):

        reader = IndexReader.open(self.d1, True)
        searcher = IndexSearcher(self.d1, True)
        q = TermQuery(Term("id", '1'))
        topDocs = searcher.search(q, 50)
        freqvec = reader.getTermFreqVector(topDocs.scoreDocs[0].doc, "all")
        terms = list(freqvec.getTerms())
        terms.sort()
        self.assert_(terms == ['blah', 'gesundheit'])

        freqs = freqvec.getTermFrequencies()
        self.assert_(freqs == [3, 1])

if __name__ == '__main__':
    import lucene
    lucene.initVM()
    unittest.main()
