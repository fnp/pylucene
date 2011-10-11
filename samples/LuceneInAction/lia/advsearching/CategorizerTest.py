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

from math import pi, sqrt, acos
from lia.common.LiaTestCase import LiaTestCase

from lucene import Document, IndexReader 


class CategorizerTest(LiaTestCase):

    def setUp(self):

        super(CategorizerTest, self).setUp()
        self.categoryMap = {}

        self.buildCategoryVectors()
        self.dumpCategoryVectors()

    def testCategorization(self):
        
        self.assertEqual("/technology/computers/programming/methodology",
                         self.getCategory("extreme agile methodology"))
        self.assertEqual("/education/pedagogy",
                         self.getCategory("montessori education philosophy"))

    def dumpCategoryVectors(self):

        for category, vectorMap in self.categoryMap.iteritems():
            print "Category", category
            for term, freq in vectorMap.iteritems():
                print "   ", term, "=", freq

    def buildCategoryVectors(self):

        reader = IndexReader.open(self.directory, True)

        for id in xrange(reader.maxDoc()):
            doc = reader.document(id)
            category = doc.get("category")
            vectorMap = self.categoryMap.get(category, None)
            if vectorMap is None:
                vectorMap = self.categoryMap[category] = {}

            termFreqVector = reader.getTermFreqVector(id, "subject")
            self.addTermFreqToMap(vectorMap, termFreqVector)

    def addTermFreqToMap(self, vectorMap, termFreqVector):

        terms = termFreqVector.getTerms()
        freqs = termFreqVector.getTermFrequencies()

        i = 0
        for term in terms:
            if term in vectorMap:
                vectorMap[term] += freqs[i]
            else:
                vectorMap[term] = freqs[i]
            i += 1

    def getCategory(self, subject):

        words = subject.split(' ')

        bestAngle = 2 * pi
        bestCategory = None

        for category, vectorMap in self.categoryMap.iteritems():
            angle = self.computeAngle(words, category, vectorMap)
            if angle != 'nan' and angle < bestAngle:
                bestAngle = angle
                bestCategory = category

        return bestCategory

    def computeAngle(self, words, category, vectorMap):

        # assume words are unique and only occur once

        dotProduct = 0
        sumOfSquares = 0

        for word in words:
            categoryWordFreq = 0

            if word in vectorMap:
                categoryWordFreq = vectorMap[word]

            # optimized because we assume frequency in words is 1
            dotProduct += categoryWordFreq
            sumOfSquares += categoryWordFreq ** 2

        if sumOfSquares == 0:
            return 'nan'

        if sumOfSquares == len(words):
            # avoid precision issues for special case
            # sqrt x * sqrt x = x
            denominator = sumOfSquares 
        else:
            denominator = sqrt(sumOfSquares) * sqrt(len(words))

        return acos(dotProduct / denominator)
