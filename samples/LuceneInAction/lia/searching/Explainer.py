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

from lucene import \
     SimpleAnalyzer, Document, QueryParser, Explanation, \
     IndexSearcher, SimpleFSDirectory, File, Version


class Explainer(object):

    def main(cls, argv):

        if len(argv) != 3:
            print "Usage: Explainer <index dir> <query>"

        else:
            indexDir = argv[1]
            queryExpression = argv[2]

            directory = SimpleFSDirectory(File(indexDir))
            query = QueryParser(Version.LUCENE_CURRENT, "contents",
                                SimpleAnalyzer()).parse(queryExpression)

            print "Query:", queryExpression

            searcher = IndexSearcher(directory)
            scoreDocs = searcher.search(query, 50).scoreDocs

            for scoreDoc in scoreDocs:
                doc = searcher.doc(scoreDoc.doc)
                explanation = searcher.explain(query, scoreDoc.doc)
                print "----------"
                print doc["title"].encode('utf-8')
                print explanation

    main = classmethod(main)


if __name__ == "__main__":
    import sys
    Explainer.main(sys.argv)
