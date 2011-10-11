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
     WhitespaceAnalyzer, Document, Field, IndexReader, IndexWriter


class T9er(object):

    keys = [         "2abc", "3def",
            "4ghi",  "5jkl", "6mno",
            "7pqrs", "8tuv", "9wxyz"]

    keyMap = {}

    def main(cls, argv):
        
        if len(argv) != 3:
            print "Usage: T9er <WordNet index dir> <t9 index>"
            return
        
        for key in cls.keys:
            c = key[0]
            k = key[1:]
            for kc in k:
                cls.keyMap[kc] = c
                print kc, "=", c

        indexDir = argv[1]
        t9dir = argv[2]

        reader = IndexReader.open(indexDir)

        numDocs = reader.maxDoc()
        print "Processing", numDocs, "words"

        writer = IndexWriter(t9dir, WhitespaceAnalyzer(), True)

        for id in xrange(reader.maxDoc()):
            origDoc = reader.document(id)
            word = origDoc.get("word")
            if word is None or len(word) == 0:
                continue

            newDoc = Document()
            newDoc.add(Field("word", word,
                             Field.Store.YES, Field.Index.UN_TOKENIZED))
            newDoc.add(Field("t9", cls.t9(word),
                             Field.Store.YES, Field.Index.UN_TOKENIZED))
            newDoc.add(Field("length", str(len(word)),
                             Field.Store.NO, Field.Index.UN_TOKENIZED))
            writer.addDocument(newDoc)
            if id % 100 == 0:
                print "Document", id

        writer.optimize()
        writer.close()

        reader.close()

    def t9(cls, word):

        return ''.join([cls.keyMap[c] for c in word])

    main = classmethod(main)
    t9 = classmethod(t9)
