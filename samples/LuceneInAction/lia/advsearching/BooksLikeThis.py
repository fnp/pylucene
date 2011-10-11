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
     Document, IndexReader, Term, BooleanQuery, IndexSearcher, TermQuery, \
     SimpleFSDirectory, File, System, BooleanClause


class BooksLikeThis(object):

    def main(cls, argv):

        indexDir = System.getProperty("index.dir")
        directory = SimpleFSDirectory(File(indexDir))

        reader = IndexReader.open(directory, True)
        blt = BooksLikeThis(reader)

        for id in xrange(reader.maxDoc()):
            if reader.isDeleted(id):
                continue
            doc = reader.document(id)
            print ''
            print doc.get("title").encode('utf-8')

            docs = blt.docsLike(id, doc, 10)
            if not docs:
                print "  None like this"
            else:
                for doc in docs:
                    print " ->", doc.get("title").encode('utf-8')

    def __init__(self, reader):

        self.reader = reader
        self.searcher = IndexSearcher(reader)

    def docsLike(self, id, doc, max):

        authors = doc.getValues("author")
        authorQuery = BooleanQuery()
        for author in authors:
            authorQuery.add(TermQuery(Term("author", author)),
                            BooleanClause.Occur.SHOULD)
        authorQuery.setBoost(2.0)

        vector = self.reader.getTermFreqVector(id, "subject")

        subjectQuery = BooleanQuery()
        for term in vector.getTerms():
            tq = TermQuery(Term("subject", term))
            subjectQuery.add(tq, BooleanClause.Occur.SHOULD)

        likeThisQuery = BooleanQuery()
        likeThisQuery.add(authorQuery, BooleanClause.Occur.SHOULD)
        likeThisQuery.add(subjectQuery, BooleanClause.Occur.SHOULD)

        # exclude myself
        likeThisQuery.add(TermQuery(Term("isbn", doc.get("isbn"))),
                          BooleanClause.Occur.MUST_NOT)

        print "  Query:", likeThisQuery.toString("contents")
        scoreDocs = self.searcher.search(likeThisQuery, 50).scoreDocs

        docs = []
        for scoreDoc in scoreDocs:
            doc = self.searcher.doc(scoreDoc.doc)
            if len(docs) < max:
                docs.append(doc)
            else:
                break

        return docs

    main = classmethod(main)
