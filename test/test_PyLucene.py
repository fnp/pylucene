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

import os, shutil

from unittest import TestCase, main
from lucene import *


class Test_PyLuceneBase(object):

    def getAnalyzer(self):
        return StandardAnalyzer(Version.LUCENE_CURRENT)

    def openStore(self):
        raise NotImplemented

    def closeStore(self, store, *args):
        pass

    def getWriter(self, store, analyzer, create=False):
        writer = IndexWriter(store, analyzer, create,
                             IndexWriter.MaxFieldLength.LIMITED)
        #writer.setUseCompoundFile(False)
        return writer

    def getReader(self, store, analyzer):
        pass

    def test_indexDocument(self):

        store = self.openStore()
        writer = None
        try:
            analyzer = self.getAnalyzer()
            writer = self.getWriter(store, analyzer, True)

            doc = Document()
            doc.add(Field("title", "value of testing",
                          Field.Store.YES, Field.Index.ANALYZED))
            doc.add(Field("docid", str(1),
                          Field.Store.NO, Field.Index.NOT_ANALYZED))
            doc.add(Field("owner", "unittester",
                          Field.Store.YES, Field.Index.NOT_ANALYZED))
            doc.add(Field("search_name", "wisdom",
                          Field.Store.YES, Field.Index.NO))
            doc.add(Field("meta_words", "rabbits are beautiful",
                          Field.Store.NO, Field.Index.ANALYZED))
        
            writer.addDocument(doc)
        finally:
            self.closeStore(store, writer)

    def test_indexDocumentWithText(self):

        store = self.openStore()
        writer = None
        try:
            analyzer = self.getAnalyzer()
            writer = self.getWriter(store, analyzer, True)
        
            doc = Document()
            doc.add(Field("title", "value of testing",
                          Field.Store.YES, Field.Index.ANALYZED))
            doc.add(Field("docid", str(1),
                          Field.Store.NO, Field.Index.NOT_ANALYZED))
            doc.add(Field("owner", "unittester",
                          Field.Store.YES, Field.Index.NOT_ANALYZED))
            doc.add(Field("search_name", "wisdom",
                          Field.Store.YES, Field.Index.NO))
            doc.add(Field("meta_words", "rabbits are beautiful",
                          Field.Store.NO, Field.Index.ANALYZED))

            body_text = "hello world" * 20
            body_reader = StringReader(body_text)
            doc.add(Field("content", body_reader))

            writer.addDocument(doc)
        finally:
            self.closeStore(store, writer)

    def test_indexDocumentWithUnicodeText(self):

        store = self.openStore()
        writer = None
        try:
            analyzer = self.getAnalyzer()
            writer = self.getWriter(store, analyzer, True)
        
            doc = Document()
            doc.add(Field("title", "value of testing",
                          Field.Store.YES, Field.Index.ANALYZED))
            doc.add(Field("docid", str(1),
                          Field.Store.NO, Field.Index.NOT_ANALYZED))
            doc.add(Field("owner", "unittester",
                          Field.Store.YES, Field.Index.NOT_ANALYZED))
            doc.add(Field("search_name", "wisdom",
                          Field.Store.YES, Field.Index.NO))
            doc.add(Field("meta_words", "rabbits are beautiful",
                          Field.Store.NO, Field.Index.ANALYZED))

            # using a unicode body cause problems, which seems very odd
            # since the python type is the same regardless affter doing
            # the encode
            body_text = u"hello world"*20
            body_reader = StringReader(body_text)
            doc.add(Field("content", body_reader))

            writer.addDocument(doc)
        finally:
            self.closeStore(store, writer)

    def test_searchDocuments(self):

        self.test_indexDocument()

        store = self.openStore()
        searcher = None
        try:
            searcher = IndexSearcher(store, True)
            query = QueryParser(Version.LUCENE_CURRENT, "title",
                                self.getAnalyzer()).parse("value")
            topDocs = searcher.search(query, 50)
            self.assertEqual(topDocs.totalHits, 1)
        finally:
            self.closeStore(store, searcher)

    def test_searchDocumentsWithMultiField(self):
        """
        Tests searching with MultiFieldQueryParser
        """

        self.test_indexDocument()
        store = self.openStore()
        searcher = None
        try:
            searcher = IndexSearcher(store, True)
            SHOULD = BooleanClause.Occur.SHOULD
            query = MultiFieldQueryParser.parse(Version.LUCENE_CURRENT,
                                                "value", ["title", "docid"],
                                                [SHOULD, SHOULD],
                                                self.getAnalyzer())
            topDocs = searcher.search(query, 50)
            self.assertEquals(1, topDocs.totalHits)
        finally:
            self.closeStore(store, searcher)
        
    def test_removeDocument(self):

        self.test_indexDocument()

        store = self.openStore()
        searcher = None
        reader = None

        try:
            searcher = IndexSearcher(store, True)
            query = TermQuery(Term("docid", str(1)))
            topDocs = searcher.search(query, 50)
            self.assertEqual(topDocs.totalHits, 1)
            # be careful with ids they are ephemeral
            docid = topDocs.scoreDocs[0].doc
        
            reader = IndexReader.open(store, False)
            reader.deleteDocument(docid)
        finally:
            self.closeStore(store, searcher, reader)

        store = self.openStore()
        searcher = None
        try:
            searcher = IndexSearcher(store, True)
            query = TermQuery(Term("docid", str(1)))
            topDocs = searcher.search(query, 50)
            self.assertEqual(topDocs.totalHits, 0)
        finally:
            self.closeStore(store, searcher)
        
    def test_removeDocuments(self):

        self.test_indexDocument()

        store = self.openStore()
        reader = None
        try:
            reader = IndexReader.open(store, False)
            reader.deleteDocuments(Term('docid', str(1)))
        finally:
            self.closeStore(store, reader)
        
        store = self.openStore()
        searcher = None
        try:
            searcher = IndexSearcher(store, True)
            query = QueryParser(Version.LUCENE_CURRENT, "title",
                                self.getAnalyzer()).parse("value")
            topDocs = searcher.search(query, 50)
            self.assertEqual(topDocs.totalHits, 0)
        finally:
            self.closeStore(store, searcher)
        
    def test_FieldEnumeration(self):

        self.test_indexDocument()

        store = self.openStore()
        writer = None
        try:
            analyzer = self.getAnalyzer()
        
            writer = self.getWriter(store, analyzer, False)
            doc = Document()
            doc.add(Field("title", "value of testing",
                          Field.Store.YES, Field.Index.ANALYZED))
            doc.add(Field("docid", str(2),
                          Field.Store.NO, Field.Index.NOT_ANALYZED))
            doc.add(Field("owner", "unittester",
                          Field.Store.YES, Field.Index.NOT_ANALYZED))
            doc.add(Field("search_name", "wisdom",
                          Field.Store.YES, Field.Index.NO))
            doc.add(Field("meta_words", "rabbits are beautiful",
                          Field.Store.NO, Field.Index.ANALYZED))
                                   
            writer.addDocument(doc)
        
            doc = Document()
            doc.add(Field("owner", "unittester",
                          Field.Store.NO, Field.Index.NOT_ANALYZED))
            doc.add(Field("search_name", "wisdom",
                          Field.Store.YES, Field.Index.NO))
            doc.add(Field("meta_words", "rabbits are beautiful",
                          Field.Store.NO, Field.Index.ANALYZED))
            writer.addDocument(doc)        
        finally:
            self.closeStore(store, writer)
        
        store = self.openStore()
        reader = None
        try:
            reader = IndexReader.open(store, True)
            term_enum = reader.terms(Term("docid", ''))
            docids = []

            while term_enum.term().field() == 'docid':
                docids.append(term_enum.term().text())
                term_enum.next()
            self.assertEqual(len(docids), 2)
        finally:
            self.closeStore(store, reader)

    def test_getFieldNames(self):

        self.test_indexDocument()

        store = self.openStore()
        reader = None
        try:
            reader = IndexReader.open(store, True)
            fieldNames = reader.getFieldNames(IndexReader.FieldOption.ALL)
            for fieldName in fieldNames:
                self.assert_(fieldName in ['owner', 'search_name', 'meta_words',
                                           'docid', 'title'])
        
            fieldNames = reader.getFieldNames(IndexReader.FieldOption.INDEXED)
            for fieldName in fieldNames:
                self.assert_(fieldName in ['owner', 'meta_words',
                                           'docid', 'title'])

            fieldNames = reader.getFieldNames(IndexReader.FieldOption.INDEXED_NO_TERMVECTOR)
            for fieldName in fieldNames:
                self.assert_(fieldName in ['owner', 'meta_words',
                                           'docid', 'title'])
        finally:
            store = self.closeStore(store, reader)

        
class Test_PyLuceneWithFSStore(TestCase, Test_PyLuceneBase):

    STORE_DIR = "testrepo"

    def setUp(self):

        if not os.path.exists(self.STORE_DIR):
            os.mkdir(self.STORE_DIR)

    def tearDown(self):

        if os.path.exists(self.STORE_DIR):
            shutil.rmtree(self.STORE_DIR)

    def openStore(self):

        return SimpleFSDirectory(File(self.STORE_DIR))

    def closeStore(self, store, *args):
        
        for arg in args:
            if arg is not None:
                arg.close()

        store.close()


class Test_PyLuceneWithMMapStore(Test_PyLuceneWithFSStore):

    def openStore(self):

        return MMapDirectory(File(self.STORE_DIR))



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
