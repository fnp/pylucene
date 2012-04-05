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

from lucene import \
     Document, Term, IndexSearcher, TermQuery, \
     SimpleFSDirectory, RAMDirectory, File


class WordNetSynonymEngine(object):

    def __init__(self, indexDir):

        self.directory = RAMDirectory(SimpleFSDirectory(File(indexDir)))
        self.searcher = IndexSearcher(self.directory)

    def getSynonyms(self, word):

        synList = []
        topDocs = self.searcher.search(TermQuery(Term("word", word)), 50)
        
        for scoreDoc in topDocs.scoreDocs:
            doc = self.searcher.doc(scoreDoc.doc)
            for value in doc.getValues("syn"):
                synList.append(value)

        return synList
