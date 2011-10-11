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

from unittest import main
from BaseTestRangeFilter import BaseTestRangeFilter

from lucene import *

 #
 # A basic 'positive' Unit test class for the TermRangeFilter class.
 #
 # NOTE: at the moment, this class only tests for 'positive' results,
 # it does not verify the results to ensure there are no 'false positives',
 # nor does it adequately test 'negative' results.  It also does not test
 # that garbage in results in an Exception.
 #

class TestTermRangeFilter(BaseTestRangeFilter):

    def testRangeFilterId(self):

        index = self.signedIndex
        reader = IndexReader.open(index.index, True);
        search = IndexSearcher(reader)

        medId = ((self.maxId - self.minId) / 2)
        
        minIP = self.pad(self.minId)
        maxIP = self.pad(self.maxId)
        medIP = self.pad(medId)
    
        numDocs = reader.numDocs()
        
        self.assertEqual(numDocs, 1 + self.maxId - self.minId, "num of docs")
        
        q = TermQuery(Term("body","body"))

        # test id, bounded on both ends
        
        result = search.search(q, TermRangeFilter("id", minIP, maxIP,
                                                  True, True), 50)
        self.assertEqual(numDocs, result.totalHits, "find all")

        result = search.search(q, TermRangeFilter("id", minIP, maxIP,
                                                  True, False), 50)
        self.assertEqual(numDocs - 1, result.totalHits, "all but last")

        result = search.search(q, TermRangeFilter("id", minIP, maxIP,
                                                  False, True), 50)
        self.assertEqual(numDocs - 1, result.totalHits, "all but first")
        
        result = search.search(q, TermRangeFilter("id", minIP, maxIP,
                                                  False, False), 50)
        self.assertEqual(numDocs - 2, result.totalHits, "all but ends")
        
        result = search.search(q, TermRangeFilter("id", medIP, maxIP,
                                                  True, True), 50)
        self.assertEqual(1 + self.maxId - medId, result.totalHits, "med and up")
        
        result = search.search(q, TermRangeFilter("id", minIP, medIP,
                                                  True, True), 50)
        self.assertEqual(1 + medId - self.minId, result.totalHits, "up to med")

        # unbounded id

        result = search.search(q, TermRangeFilter("id", minIP, None,
                                                  True, False), 50)
        self.assertEqual(numDocs, result.totalHits, "min and up")
        
        result = search.search(q, TermRangeFilter("id", None, maxIP,
                                                  False, True), 50)
        self.assertEqual(numDocs, result.totalHits, "max and down")
        
        result = search.search(q, TermRangeFilter("id", minIP, None,
                                                  False, False), 50)
        self.assertEqual(numDocs - 1, result.totalHits, "not min, but up")
        
        result = search.search(q, TermRangeFilter("id", None, maxIP,
                                                  False, False), 50)
        self.assertEqual(numDocs - 1, result.totalHits, "not max, but down")
        
        result = search.search(q, TermRangeFilter("id",medIP, maxIP,
                                                  True, False), 50)
        self.assertEqual(self.maxId - medId, result.totalHits, "med and up, not max")
        
        result = search.search(q, TermRangeFilter("id", minIP, medIP,
                                                  False, True), 50)
        self.assertEqual(medId - self.minId, result.totalHits, "not min, up to med")

        # very small sets

        result = search.search(q, TermRangeFilter("id", minIP, minIP,
                                                  False, False), 50)
        self.assertEqual(0, result.totalHits, "min, min, False, False")
        
        result = search.search(q, TermRangeFilter("id", medIP, medIP,
                                                  False, False), 50)
        self.assertEqual(0, result.totalHits, "med, med, False, False")
        result = search.search(q, TermRangeFilter("id", maxIP, maxIP,
                                                  False, False), 50)
        self.assertEqual(0, result.totalHits, "max, max, False, False")
        
        result = search.search(q, TermRangeFilter("id", minIP, minIP,
                                                  True, True), 50)
        self.assertEqual(1, result.totalHits, "min, min, True, True")
        result = search.search(q, TermRangeFilter("id", None, minIP,
                                                  False, True), 50)
        self.assertEqual(1, result.totalHits, "nul, min, False, True")
        
        result = search.search(q, TermRangeFilter("id", maxIP, maxIP,
                                                  True, True), 50)
        self.assertEqual(1, result.totalHits, "max, max, True, True")
        result = search.search(q, TermRangeFilter("id", maxIP, None,
                                                  True, False), 50)
        self.assertEqual(1, result.totalHits, "max, nul, True, True")
        
        result = search.search(q, TermRangeFilter("id", medIP, medIP,
                                                  True, True), 50)
        self.assertEqual(1, result.totalHits, "med, med, True, True")
        
    def testRangeFilterIdCollating(self):

        index = self.signedIndex
        reader = IndexReader.open(index.index, True)
        search = IndexSearcher(reader)

        c = Collator.getInstance(Locale.ENGLISH)

        medId = ((self.maxId - self.minId) / 2)

        minIP = self.pad(self.minId)
        maxIP = self.pad(self.maxId)
        medIP = self.pad(medId)

        numDocs = reader.numDocs()

        self.assertEqual(numDocs, 1 + self.maxId - self.minId, "num of docs")

        q = TermQuery(Term("body", "body"))

        # test id, bounded on both ends
        numHits = search.search(q, TermRangeFilter("id", minIP, maxIP,
                                                   True, True, c), 1000).totalHits
        self.assertEqual(numDocs, numHits, "find all")

        numHits = search.search(q, TermRangeFilter("id", minIP, maxIP,
                                                   True, False, c), 1000).totalHits
        self.assertEqual(numDocs - 1, numHits, "all but last")

        numHits = search.search(q, TermRangeFilter("id", minIP, maxIP,
                                                   False, True, c), 1000).totalHits
        self.assertEqual(numDocs - 1, numHits, "all but first")

        numHits = search.search(q, TermRangeFilter("id", minIP, maxIP,
                                                   False, False, c), 1000).totalHits
        self.assertEqual(numDocs - 2, numHits, "all but ends")

        numHits = search.search(q, TermRangeFilter("id", medIP, maxIP,
                                                   True, True, c),  1000).totalHits
        self.assertEqual(1 + self.maxId - medId,  numHits, "med and up")

        numHits = search.search(q, TermRangeFilter("id", minIP, medIP,
                                                   True, True, c), 1000).totalHits
        self.assertEqual(1 + medId - self.minId, numHits, "up to med")

        # unbounded id

        numHits = search.search(q, TermRangeFilter("id", minIP, None,
                                                   True, False, c), 1000).totalHits
        self.assertEqual(numDocs, numHits, "min and up")

        numHits = search.search(q, TermRangeFilter("id", None, maxIP,
                                                   False, True, c), 1000).totalHits
        self.assertEqual(numDocs, numHits, "max and down")

        numHits = search.search(q, TermRangeFilter("id", minIP, None,
                                                   False, False, c), 1000).totalHits
        self.assertEqual(numDocs - 1, numHits, "not min, but up")

        numHits = search.search(q, TermRangeFilter("id", None, maxIP,
                                                   False, False, c), 1000).totalHits
        self.assertEqual(numDocs - 1, numHits, "not max, but down")

        numHits = search.search(q, TermRangeFilter("id", medIP, maxIP,
                                                   True, False, c), 1000).totalHits
        self.assertEqual(self.maxId - medId, numHits, "med and up, not max")

        numHits = search.search(q, TermRangeFilter("id", minIP, medIP,
                                                   False, True, c), 1000).totalHits
        self.assertEqual(medId - self.minId, numHits, "not min, up to med")

        # very small sets

        numHits = search.search(q, TermRangeFilter("id", minIP, minIP,
                                                   False, False, c), 1000).totalHits
        self.assertEqual(0, numHits, "min, min, F, F")
        numHits = search.search(q, TermRangeFilter("id", medIP, medIP,
                                                   False, False, c), 1000).totalHits
        self.assertEqual(0, numHits, "med, med, F, F")
        numHits = search.search(q, TermRangeFilter("id", maxIP, maxIP,
                                                   False, False, c), 1000).totalHits
        self.assertEqual(0, numHits, "max, max, F, F")

        numHits = search.search(q, TermRangeFilter("id", minIP, minIP,
                                                   True, True, c), 1000).totalHits
        self.assertEqual(1, numHits, "min, min, T, T")
        numHits = search.search(q, TermRangeFilter("id", None, minIP,
                                                   False, True, c), 1000).totalHits
        self.assertEqual(1, numHits, "nul, min, F, T")

        numHits = search.search(q, TermRangeFilter("id", maxIP, maxIP,
                                                   True, True, c), 1000).totalHits
        self.assertEqual(1, numHits, "max, max, T, T")
        numHits = search.search(q, TermRangeFilter("id", maxIP, None,
                                                   True, False, c), 1000).totalHits
        self.assertEqual(1, numHits, "max, nul, T, T")

        numHits = search.search(q, TermRangeFilter("id", medIP, medIP,
                                                   True, True, c), 1000).totalHits
        self.assertEqual(1, numHits, "med, med, T, T")

    def testRangeFilterRand(self):

        index = self.signedIndex
        reader = IndexReader.open(index.index, True)
        search = IndexSearcher(reader)

        minRP = self.pad(index.minR)
        maxRP = self.pad(index.maxR)

        numDocs = reader.numDocs()
        
        self.assertEqual(numDocs, 1 + self.maxId - self.minId, "num of docs")
        
        q = TermQuery(Term("body", "body"))

        # test extremes, bounded on both ends
        
        result = search.search(q, TermRangeFilter("rand", minRP, maxRP, 
                                                  True, True), 50)
        self.assertEqual(numDocs, result.totalHits, "find all")

        result = search.search(q, TermRangeFilter("rand", minRP, maxRP, 
                                                  True, False), 50)
        self.assertEqual(numDocs - 1, result.totalHits, "all but biggest")

        result = search.search(q, TermRangeFilter("rand", minRP, maxRP, 
                                                  False, True), 50)
        self.assertEqual(numDocs - 1, result.totalHits, "all but smallest")
        
        result = search.search(q, TermRangeFilter("rand", minRP, maxRP, 
                                                  False, False), 50)
        self.assertEqual(numDocs - 2, result.totalHits, "all but extremes")
    
        # unbounded

        result = search.search(q, TermRangeFilter("rand", minRP, None, 
                                                  True, False), 50)
        self.assertEqual(numDocs, result.totalHits, "smallest and up")

        result = search.search(q, TermRangeFilter("rand", None, maxRP, 
                                                  False, True), 50)
        self.assertEqual(numDocs, result.totalHits, "biggest and down")

        result = search.search(q, TermRangeFilter("rand", minRP, None, 
                                                  False, False), 50)
        self.assertEqual(numDocs - 1, result.totalHits, "not smallest, but up")
        
        result = search.search(q, TermRangeFilter("rand", None, maxRP, 
                                                  False, False), 50)
        self.assertEqual(numDocs - 1, result.totalHits, "not biggest, but down")
        
        # very small sets

        result = search.search(q, TermRangeFilter("rand", minRP, minRP, 
                                                  False, False), 50)
        self.assertEqual(0, result.totalHits, "min, min, False, False")

        result = search.search(q, TermRangeFilter("rand", maxRP, maxRP, 
                                                  False, False), 50)
        self.assertEqual(0, result.totalHits, "max, max, False, False")
                     
        result = search.search(q, TermRangeFilter("rand", minRP, minRP, 
                                                  True, True), 50)
        self.assertEqual(1, result.totalHits, "min, min, True, True")

        result = search.search(q, TermRangeFilter("rand", None, minRP, 
                                                  False, True), 50)
        self.assertEqual(1, result.totalHits, "nul, min, False, True")

        result = search.search(q, TermRangeFilter("rand", maxRP, maxRP, 
                                                  True, True), 50)
        self.assertEqual(1, result.totalHits, "max, max, True, True")

        result = search.search(q, TermRangeFilter("rand", maxRP, None, 
                                                  True, False), 50)
        self.assertEqual(1, result.totalHits, "max, nul, True, True")

    def testRangeFilterRandCollating(self):

        # using the unsigned index because collation seems to ignore hyphens
        index = self.unsignedIndex
        reader = IndexReader.open(index.index, True)
        search = IndexSearcher(reader)

        c = Collator.getInstance(Locale.ENGLISH)

        minRP = self.pad(index.minR)
        maxRP = self.pad(index.maxR)

        numDocs = reader.numDocs()

        self.assertEqual(numDocs, 1 + self.maxId - self.minId, "num of docs")

        q = TermQuery(Term("body", "body"))

        # test extremes, bounded on both ends

        numHits = search.search(q, TermRangeFilter("rand", minRP, maxRP,
                                                   True, True, c), 1000).totalHits
        self.assertEqual(numDocs, numHits, "find all")

        numHits = search.search(q, TermRangeFilter("rand", minRP, maxRP,
                                                   True, False, c), 1000).totalHits
        self.assertEqual(numDocs - 1, numHits, "all but biggest")

        numHits = search.search(q, TermRangeFilter("rand", minRP, maxRP,
                                                   False, True, c), 1000).totalHits
        self.assertEqual(numDocs - 1, numHits, "all but smallest")

        numHits = search.search(q, TermRangeFilter("rand", minRP, maxRP,
                                                   False, False, c), 1000).totalHits
        self.assertEqual(numDocs - 2, numHits, "all but extremes")

        # unbounded

        numHits = search.search(q, TermRangeFilter("rand", minRP, None,
                                                   True, False, c), 1000).totalHits
        self.assertEqual(numDocs, numHits, "smallest and up")

        numHits = search.search(q, TermRangeFilter("rand", None, maxRP,
                                                   False, True, c), 1000).totalHits
        self.assertEqual(numDocs, numHits, "biggest and down")

        numHits = search.search(q, TermRangeFilter("rand", minRP, None,
                                                   False, False, c), 1000).totalHits
        self.assertEqual(numDocs - 1, numHits, "not smallest, but up")

        numHits = search.search(q, TermRangeFilter("rand", None, maxRP,
                                                   False, False, c), 1000).totalHits
        self.assertEqual(numDocs - 1, numHits, "not biggest, but down")

        # very small sets

        numHits = search.search(q, TermRangeFilter("rand", minRP, minRP,
                                                   False, False, c), 1000).totalHits
        self.assertEqual(0, numHits, "min, min, F, F")

        numHits = search.search(q, TermRangeFilter("rand", maxRP, maxRP,
                                                   False, False, c), 1000).totalHits
        self.assertEqual(0, numHits, "max, max, F, F")

        numHits = search.search(q, TermRangeFilter("rand", minRP, minRP,
                                                   True, True, c), 1000).totalHits
        self.assertEqual(1, numHits, "min, min, T, T")

        numHits = search.search(q, TermRangeFilter("rand", None, minRP,
                                                   False, True, c), 1000).totalHits
        self.assertEqual(1, numHits, "nul, min, F, T")

        numHits = search.search(q, TermRangeFilter("rand", maxRP, maxRP,
                                                   True, True, c), 1000).totalHits
        self.assertEqual(1, numHits, "max, max, T, T")
        numHits = search.search(q, TermRangeFilter("rand", maxRP, None,
                                                   True, False, c), 1000).totalHits
        self.assertEqual(1, numHits, "max, nul, T, T")

    def testFarsi(self):
            
        # build an index
        farsiIndex = RAMDirectory()
        writer = IndexWriter(farsiIndex, SimpleAnalyzer(), True, 
                             IndexWriter.MaxFieldLength.LIMITED)
        doc = Document()
        doc.add(Field("content", u"\u0633\u0627\u0628", 
                      Field.Store.YES, Field.Index.NOT_ANALYZED))
        doc.add(Field("body", "body",
                      Field.Store.YES, Field.Index.NOT_ANALYZED))
        writer.addDocument(doc)
            
        writer.optimize()
        writer.close()

        reader = IndexReader.open(farsiIndex, True)
        search = IndexSearcher(reader)
        q = TermQuery(Term("body", "body"))

        # Neither Java 1.4.2 nor 1.5.0 has Farsi Locale collation available in
        # RuleBasedCollator.  However, the Arabic Locale seems to order the
        # Farsi characters properly.
        collator = Collator.getInstance(Locale("ar"))
        
        # Unicode order would include U+0633 in [ U+062F - U+0698 ], but Farsi
        # orders the U+0698 character before the U+0633 character, so the
        # single index Term below should NOT be returned by a
        # TermRangeFilter with a Farsi Collator (or an Arabic one for the
        # case when Farsi is not supported).
        numHits = search.search(q, TermRangeFilter("content", u"\u062F", u"\u0698", True, True, collator), 1000).totalHits
        self.assertEqual(0, numHits, "The index Term should not be included.")

        numHits = search.search(q, TermRangeFilter("content", u"\u0633", u"\u0638", True, True, collator), 1000).totalHits
        self.assertEqual(1, numHits, "The index Term should be included.")
        search.close()

    def testDanish(self):
            
        # build an index
        danishIndex = RAMDirectory()
        writer = IndexWriter(danishIndex, SimpleAnalyzer(), True,
                             IndexWriter.MaxFieldLength.LIMITED)

        # Danish collation orders the words below in the given order
        # (example taken from TestSort.testInternationalSort() ).
        words = [u"H\u00D8T", u"H\u00C5T", "MAND"]
        for word in words:
            doc = Document()
            doc.add(Field("content", word, Field.Store.YES,
                          Field.Index.NOT_ANALYZED))
            doc.add(Field("body", "body", Field.Store.YES,
                          Field.Index.NOT_ANALYZED))
            writer.addDocument(doc)

        writer.optimize()
        writer.close()

        reader = IndexReader.open(danishIndex, True)
        search = IndexSearcher(reader)
        q = TermQuery(Term("body", "body"))

        collator = Collator.getInstance(Locale("da", "dk"))
        query = TermRangeQuery("content", "H\u00D8T", "MAND", False, False,
                               collator)

        # Unicode order would not include "H\u00C5T" in [ "H\u00D8T", "MAND" ],
        # but Danish collation does.
        numHits = search.search(q, TermRangeFilter("content", u"H\u00D8T", "MAND", False, False, collator), 1000).totalHits
        self.assertEqual(1, numHits, "The index Term should be included.")

        numHits = search.search(q, TermRangeFilter("content", u"H\u00C5T", "MAND", False, False, collator), 1000).totalHits
        self.assertEqual(0, numHits, "The index Term should not be included.")
        search.close()


if __name__ == "__main__":
    import sys, lucene
    lucene.initVM()
    if '-loop' in sys.argv:
        sys.argv.remove('-loop')
        while True:
            try:
                main(defaultTest='TestTermRangeFilter')
            except:
                pass
    else:
        main(defaultTest='TestTermRangeFilter')
