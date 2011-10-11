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
    SimpleFSDirectory, Document, Field, IndexSearcher, StandardAnalyzer, \
    MatchAllDocsQuery, Sort, SortField, DecimalFormat, System, File, \
    TopFieldCollector, QueryParser, Version, BooleanQuery, BooleanClause


class SortingExample(object):

    def __init__(self, directory):

        self.directory = directory

    def displayResults(self, query, sort):

        searcher = IndexSearcher(self.directory, True)

        fillFields = False
        computeMaxScore = False
        docsScoredInOrder = False
        computeScores = True

        collector = TopFieldCollector.create(sort, 20,
                                             fillFields,
                                             computeScores,
                                             computeMaxScore,
                                             docsScoredInOrder)

        searcher.search(query, None, collector)
        scoreDocs = collector.topDocs().scoreDocs

        print "\nResults for:", query, "sorted by", sort
        print "Title".rjust(30), "pubmonth".rjust(10), \
              "id".center(4), "score".center(15)

        scoreFormatter = DecimalFormat("0.######")
        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)
            title = doc["title"]
            if len(title) > 30:
                title = title[:30]
            print title.encode('ascii', 'replace').rjust(30), \
                  doc["pubmonth"].rjust(10), \
                  str(scoreDoc.doc).center(4), \
                  scoreFormatter.format(scoreDoc.score).ljust(12)
            print "  ", doc["category"]
            # print searcher.explain(query, scoreDoc.doc)

        searcher.close()

    def main(cls, argv):

        allBooks = MatchAllDocsQuery()
        parser = QueryParser(Version.LUCENE_CURRENT, "contents",
                             StandardAnalyzer(Version.LUCENE_CURRENT))
        query = BooleanQuery()
        query.add(allBooks, BooleanClause.Occur.SHOULD)
        query.add(parser.parse("java OR action"), BooleanClause.Occur.SHOULD)

        indexDir = System.getProperty("index.dir")
        directory = SimpleFSDirectory(File(indexDir))

        example = SortingExample(directory)

        example.displayResults(query, Sort.RELEVANCE)
        example.displayResults(query, Sort.INDEXORDER)
        example.displayResults(query,
                               Sort(SortField("category", SortField.STRING)))
        example.displayResults(query,
                               Sort(SortField("pubmonth", SortField.INT, True)))

        example.displayResults(query,
                               Sort([SortField("category", SortField.STRING),
                                     SortField.FIELD_SCORE,
                                     SortField("pubmonth", SortField.INT, True)]))

        example.displayResults(query,
                               Sort([SortField.FIELD_SCORE,
                                     SortField("category", SortField.STRING)]))
        directory.close()

    main = classmethod(main)
