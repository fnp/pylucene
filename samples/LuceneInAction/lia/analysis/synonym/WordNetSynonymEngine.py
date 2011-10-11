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
     Document, Term, IndexSearcher, TermQuery, FSDirectory, RAMDirectory, Hit


class WordNetSynonymEngine(object):

    def __init__(self, indexDir):

        self.directory = RAMDirectory(indexDir)
        self.searcher = IndexSearcher(self.directory)

    def getSynonyms(self, word):

        synList = []

        for hit in self.searcher.search(TermQuery(Term("word", word))):
            doc = Hit.cast_(hit).getDocument()
            for value in doc.getValues("syn"):
                synList.append(value)

        return synList
