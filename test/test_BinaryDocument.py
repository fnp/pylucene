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


class TestBinaryDocument(TestCase):

    binaryValStored = "this text will be stored as a byte array in the index"
    binaryValCompressed = "this text will be also stored and compressed as a byte array in the index"
  
    def testBinaryFieldInIndex(self):

        bytes = JArray('byte')(self.binaryValStored)
        binaryFldStored = Field("binaryStored", bytes, 
                                Field.Store.YES)
        stringFldStored = Field("stringStored", self.binaryValStored,
                                Field.Store.YES, Field.Index.NO,
                                Field.TermVector.NO)

        try:
            # binary fields with store off are not allowed
            Field("fail", bytes, Field.Store.NO)
            self.fail()
        except JavaError, e:
            self.assertEqual(e.getJavaException().getClass().getName(),
                             'java.lang.IllegalArgumentException')
    
        doc = Document()
        doc.add(binaryFldStored)
        doc.add(stringFldStored)

        # test for field count
        self.assertEqual(2, doc.fields.size())
    
        # add the doc to a ram index
        dir = RAMDirectory()
        writer = IndexWriter(dir, StandardAnalyzer(Version.LUCENE_CURRENT),
                             True, IndexWriter.MaxFieldLength.LIMITED)
        writer.addDocument(doc)
        writer.close()
    
        # open a reader and fetch the document
        reader = IndexReader.open(dir, False)
        docFromReader = reader.document(0)
        self.assert_(docFromReader is not None)
    
        # fetch the binary stored field and compare it's content with the
        # original one
        bytes = docFromReader.getBinaryValue("binaryStored")
        binaryFldStoredTest = bytes.string_
        self.assertEqual(binaryFldStoredTest, self.binaryValStored)
        
        # fetch the string field and compare it's content with the original
        # one
        stringFldStoredTest = docFromReader.get("stringStored")
        self.assertEqual(stringFldStoredTest, self.binaryValStored)
    
        # delete the document from index
        reader.deleteDocument(0)
        self.assertEqual(0, reader.numDocs())
    
        reader.close()
        dir.close()
  
    def testCompressionTools(self):

        bytes = JArray('byte')(self.binaryValCompressed)
        binaryFldCompressed = Field("binaryCompressed", CompressionTools.compress(bytes), Field.Store.YES)
        stringFldCompressed = Field("stringCompressed", CompressionTools.compressString(self.binaryValCompressed), Field.Store.YES)
    
        doc = Document()
        doc.add(binaryFldCompressed)
        doc.add(stringFldCompressed)
    
        # add the doc to a ram index
        dir = RAMDirectory()
        writer = IndexWriter(dir, StandardAnalyzer(Version.LUCENE_CURRENT),
                             True, IndexWriter.MaxFieldLength.LIMITED)
        writer.addDocument(doc)
        writer.close()
    
        # open a reader and fetch the document
        reader = IndexReader.open(dir, False)
        docFromReader = reader.document(0)
        self.assert_(docFromReader is not None)
    
        # fetch the binary compressed field and compare it's content with
        # the original one
        bytes = CompressionTools.decompress(docFromReader.getBinaryValue("binaryCompressed"))
        binaryFldCompressedTest = bytes.string_
        self.assertEqual(binaryFldCompressedTest, self.binaryValCompressed)
        self.assertEqual(CompressionTools.decompressString(docFromReader.getBinaryValue("stringCompressed")), self.binaryValCompressed)

        reader.close()
        dir.close()


if __name__ == '__main__':
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
