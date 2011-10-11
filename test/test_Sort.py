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

import math

from itertools import izip
from random import randint
from unittest import TestCase, main
from lucene import *

NUM_STRINGS = 6000



class SortTestCase(TestCase):
    """
    Unit tests for sorting code, ported from Java Lucene
    """

    def __init__(self, *args, **kwds):

        super(SortTestCase, self).__init__(*args, **kwds)

        self.data = [
    #      tracer  contents         int            float           string   custom   i18n               long                  double,                short,                byte,           custom parser encoding'
        [   "A",   "x a",           "5",           "4f",           "c",    "A-3",   u"p\u00EAche",      "10",                  "-4.0",                "3",                  "126",          "J"  ],
        [   "B",   "y a",           "5",           "3.4028235E38", "i",    "B-10",  "HAT",             "1000000000",          "40.0",                "24",                 "1",            "I"  ],
        [   "C",   "x a b c",       "2147483647",  "1.0",          "j",    "A-2",   u"p\u00E9ch\u00E9", "99999999",            "40.00002343",         "125",                "15",           "H"  ],
        [   "D",   "y a b c",       "-1",          "0.0f",         "a",     "C-0",   "HUT",             str(Long.MAX_VALUE),  str(Double.MIN_VALUE), str(Short.MIN_VALUE), str(Byte.MIN_VALUE), "G"  ],
        [   "E",   "x a b c d",     "5",           "2f",           "h",     "B-8",   "peach",           str(Long.MIN_VALUE),  str(Double.MAX_VALUE), str(Short.MAX_VALUE), str(Byte.MAX_VALUE), "F"  ],
        [   "F",   "y a b c d",     "2",           "3.14159f",     "g",     "B-1",   u"H\u00C5T",        "-44",                "343.034435444",       "-3",                 "0",            "E"  ],
        [   "G",   "x a b c d",     "3",           "-1.0",         "f",     "C-100", "sin",             "323254543543",       "4.043544",            "5",                  "100",          "D"  ],
        [   "H",   "y a b c d",     "0",           "1.4E-45",      "e",     "C-88",  u"H\u00D8T",        "1023423423005",      "4.043545",            "10",                 "-50",          "C"  ],
        [   "I",   "x a b c d e f", "-2147483648", "1.0e+0",       "d",     "A-10",  u"s\u00EDn",        "332422459999",       "4.043546",            "-340",               "51",           "B"  ],
        [   "J",   "y a b c d e f", "4",           ".5",           "b",     "C-7",   "HOT",             "34334543543",        "4.0000220343",        "300",                "2",            "A"  ],
        [   "W",   "g",             "1",           None,           None,    None,    None,              None,                 None,                  None,                 None,           None  ],
        [   "X",   "g",             "1",           "0.1",          None,    None,    None,              None,                 None,                  None,                 None,           None  ],
        [   "Y",   "g",             "1",           "0.2",          None,    None,    None,              None,                 None,                  None,                 None,           None  ],
        [   "Z",   "f g",           None,          None,           None,    None,    None,              None,                 None,                  None,                 None,           None  ],
        ]

    def _getIndex(self, even, odd):

        indexStore = RAMDirectory()
        writer = IndexWriter(indexStore, SimpleAnalyzer(), True,
                             IndexWriter.MaxFieldLength.LIMITED)
        writer.setMaxBufferedDocs(2)
        writer.setMergeFactor(1000)

        for i in xrange(len(self.data)):
            if (i % 2 == 0 and even) or (i % 2 == 1 and odd):
                doc = Document()
                doc.add(Field("tracer", self.data[i][0], Field.Store.YES,
                              Field.Index.NO))
                doc.add(Field("contents", self.data[i][1], Field.Store.NO,
                              Field.Index.ANALYZED))
                if self.data[i][2] is not None:
                    doc.add(Field("int", self.data[i][2], Field.Store.NO,
                                  Field.Index.NOT_ANALYZED))
                if self.data[i][3] is not None:
                    doc.add(Field("float", self.data[i][3], Field.Store.NO,
                                  Field.Index.NOT_ANALYZED))
                if self.data[i][4] is not None:
                    doc.add(Field("string", self.data[i][4], Field.Store.NO,
                                  Field.Index.NOT_ANALYZED))
                if self.data[i][5] is not None:
                    doc.add(Field("custom", self.data[i][5], Field.Store.NO,
                                  Field.Index.NOT_ANALYZED))
                if self.data[i][6] is not None:
                    doc.add(Field("i18n", self.data[i][6], Field.Store.NO,
                                  Field.Index.NOT_ANALYZED))
                if self.data[i][7] is not None:
                    doc.add(Field("long", self.data[i][7], Field.Store.NO,
                                  Field.Index.NOT_ANALYZED))
                if self.data[i][8] is not None:
                    doc.add(Field("double", self.data[i][8], Field.Store.NO,
                                  Field.Index.NOT_ANALYZED))
                if self.data[i][9] is not None:
                    doc.add(Field("short", self.data[i][9], Field.Store.NO,
                                  Field.Index.NOT_ANALYZED))
                if self.data[i][10] is not None:
                    doc.add(Field("byte", self.data[i][10], Field.Store.NO,
                                  Field.Index.NOT_ANALYZED))
                if self.data[i][11] is not None:
                    doc.add(Field("parser", self.data[i][11], Field.Store.NO,
                                  Field.Index.NOT_ANALYZED))
                doc.setBoost(2.0)  # produce some scores above 1.0
                writer.addDocument(doc)
        # writer.optimize()
        writer.close()
        s = IndexSearcher(indexStore, True)
        s.setDefaultFieldSortScoring(True, True)

        return s

    def _getFullIndex(self):
        return self._getIndex(True, True)

    def getFullStrings(self):

        indexStore = RAMDirectory()
        writer = IndexWriter(indexStore, SimpleAnalyzer(), True,
                             IndexWriter.MaxFieldLength.LIMITED)
        writer.setMaxBufferedDocs(4)
        writer.setMergeFactor(97)
        
        for i in xrange(NUM_STRINGS):
            doc = Document()
            num = self.getRandomCharString(self.getRandomNumber(2, 8), 48, 52)
            doc.add(Field("tracer", num, Field.Store.YES, Field.Index.NO))
            # doc.add(Field("contents", str(i), Field.Store.NO,
            #         Field.Index.ANALYZED))
            doc.add(Field("string", num, Field.Store.NO,
                          Field.Index.NOT_ANALYZED))
            num2 = self.getRandomCharString(self.getRandomNumber(1, 4), 48, 50)
            doc.add(Field("string2", num2, Field.Store.NO,
                          Field.Index.NOT_ANALYZED))
            doc.add(Field("tracer2", num2, Field.Store.YES, Field.Index.NO))
            doc.setBoost(2.0)  # produce some scores above 1.0
            writer.setMaxBufferedDocs(self.getRandomNumber(2, 12))
            writer.addDocument(doc)
      
        # writer.optimize()
        # print writer.getSegmentCount()
        writer.close()

        return IndexSearcher(indexStore, True)
  
    def getRandomNumberString(self, num, low, high):

        return ''.join([self.getRandomNumber(low, high) for i in xrange(num)])
  
    def getRandomCharString(self, num):

        return self.getRandomCharString(num, 48, 122)
  
    def getRandomCharString(self, num,  start, end):
        
        return ''.join([chr(self.getRandomNumber(start, end))
                        for i in xrange(num)])
  
    def getRandomNumber(self, low, high):
  
        return randint(low, high)

    def _getXIndex(self):
        return self._getIndex(True, False)

    def _getYIndex(self):
        return self._getIndex(False, True)

    def _getEmptyIndex(self):
        return self._getIndex(False, False)

    def setUp(self):

        self.full = self._getFullIndex()
        self.searchX = self._getXIndex()
        self.searchY = self._getYIndex()
        self.queryX = TermQuery(Term("contents", "x"))
        self.queryY = TermQuery(Term("contents", "y"))
        self.queryA = TermQuery(Term("contents", "a"))
        self.queryE = TermQuery(Term("contents", "e"))
        self.queryF = TermQuery(Term("contents", "f"))
        self.queryG = TermQuery(Term("contents", "g"))

    def testBuiltInSorts(self):
        """
        test the sorts by score and document number
        """

        sort = Sort()
        self._assertMatches(self.full, self.queryX, sort, "ACEGI")
        self._assertMatches(self.full, self.queryY, sort, "BDFHJ")

        sort.setSort(SortField.FIELD_DOC)
        self._assertMatches(self.full, self.queryX, sort, "ACEGI")
        self._assertMatches(self.full, self.queryY, sort, "BDFHJ")

    def testTypedSort(self):
        """
        test sorts where the type of field is specified
        """

        sort = Sort()

        sort.setSort([SortField("int", SortField.INT),
                      SortField.FIELD_DOC])
        self._assertMatches(self.full, self.queryX, sort, "IGAEC")
        self._assertMatches(self.full, self.queryY, sort, "DHFJB")

        sort.setSort([SortField("float", SortField.FLOAT),
                      SortField.FIELD_DOC])
        self._assertMatches(self.full, self.queryX, sort, "GCIEA")
        self._assertMatches(self.full, self.queryY, sort, "DHJFB")

        sort.setSort([SortField("long", SortField.LONG),
                      SortField.FIELD_DOC])
        self._assertMatches(self.full, self.queryX, sort, "EACGI")
        self._assertMatches(self.full, self.queryY, sort, "FBJHD")

        sort.setSort([SortField("double", SortField.DOUBLE),
                      SortField.FIELD_DOC])
        self._assertMatches(self.full, self.queryX, sort, "AGICE")
        self._assertMatches(self.full, self.queryY, sort, "DJHBF")

        sort.setSort([SortField("byte", SortField.BYTE),
                      SortField.FIELD_DOC])
        self._assertMatches(self.full, self.queryX, sort, "CIGAE")
        self._assertMatches(self.full, self.queryY, sort, "DHFBJ")

        sort.setSort([SortField("short", SortField.SHORT),
                      SortField.FIELD_DOC])
        self._assertMatches(self.full, self.queryX, sort, "IAGCE")
        self._assertMatches(self.full, self.queryY, sort, "DFHBJ")

        sort.setSort([SortField("string", SortField.STRING),
                      SortField.FIELD_DOC])
        self._assertMatches(self.full, self.queryX, sort, "AIGEC")
        self._assertMatches(self.full, self.queryY, sort, "DJHFB")
  
    def testStringSort(self):
        """
        Test String sorting: small queue to many matches, multi field sort,
        reverse sort
        """

        sort = Sort()
        searcher = self.getFullStrings()

        sort.setSort([SortField("string", SortField.STRING),
                      SortField("string2", SortField.STRING, True),
                      SortField.FIELD_DOC])

        result = searcher.search(MatchAllDocsQuery(), None, 500, sort).scoreDocs

        buff = []
        last = None
        lastSub = None
        lastDocId = 0
        fail = False

        for scoreDoc in result:
            doc2 = searcher.doc(scoreDoc.doc)
            v = doc2.getValues("tracer")
            v2 = doc2.getValues("tracer2")
            for _v, _v2 in izip(v, v2):
                if last is not None:
                    _cmp = cmp(_v, last)
                    if _cmp < 0: # ensure first field is in order
                        fail = True
                        print "fail:", _v, "<", last

                    if _cmp == 0: # ensure second field is in reverse order
                        _cmp = cmp(_v2, lastSub)
                        if _cmp > 0:
                            fail = True
                            print "rev field fail:", _v2, ">", lastSub
                        elif _cmp == 0: # ensure docid is in order
                            if scoreDoc.doc < lastDocId:
                                fail = True
                                print "doc fail:", scoreDoc.doc, ">", lastDocId

                last = _v
                lastSub = _v2
                lastDocId = scoreDoc.doc
                buff.append(_v + "(" + _v2 + ")(" + str(scoreDoc.doc) + ") ")

        if fail:
            print "topn field1(field2)(docID):", ''.join(buff)

        self.assert_(not fail, "Found sort results out of order")
  
    def testCustomFieldParserSort(self):
        """
        test sorts where the type of field is specified and a custom field
        parser is used, that uses a simple char encoding. The sorted string
        contains a character beginning from 'A' that is mapped to a numeric
        value using some "funny" algorithm to be different for each data
        type.
        """

        # since tests explicitly use different parsers on the same field name
        # we explicitly check/purge the FieldCache between each assertMatch
        fc = FieldCache.DEFAULT
        
        class intParser(PythonIntParser):
            def parseInt(_self, val):
                return (ord(val[0]) - ord('A')) * 123456

        class floatParser(PythonFloatParser):
            def parseFloat(_self, val):
                return math.sqrt(ord(val[0]))

        class longParser(PythonLongParser):
            def parseLong(_self, val):
                return (ord(val[0]) - ord('A')) * 1234567890L

        class doubleParser(PythonDoubleParser):
            def parseDouble(_self, val):
                return math.pow(ord(val[0]), ord(val[0]) - ord('A'))

        class byteParser(PythonByteParser):
            def parseByte(_self, val):
                return chr(ord(val[0]) - ord('A'))

        class shortParser(PythonShortParser):
            def parseShort(_self, val):
                return ord(val[0]) - ord('A')

        sort = Sort()
        sort.setSort([SortField("parser", intParser()),
                      SortField.FIELD_DOC])
        self._assertMatches(self.full, self.queryA, sort, "JIHGFEDCBA")
        self._assertSaneFieldCaches(self.getName() + " IntParser")
        fc.purgeAllCaches()

        sort.setSort([SortField("parser", floatParser()),
                      SortField.FIELD_DOC])
        self._assertMatches(self.full, self.queryA, sort, "JIHGFEDCBA")
        self._assertSaneFieldCaches(self.getName() + " FloatParser")
        fc.purgeAllCaches()

        sort.setSort([SortField("parser", longParser()),
                           SortField.FIELD_DOC])
        self._assertMatches(self.full, self.queryA, sort, "JIHGFEDCBA")
        self._assertSaneFieldCaches(self.getName() + " LongParser")
        fc.purgeAllCaches()

        sort.setSort([SortField("parser", doubleParser()),
                      SortField.FIELD_DOC])
        self._assertMatches(self.full, self.queryA, sort, "JIHGFEDCBA")
        self._assertSaneFieldCaches(self.getName() + " DoubleParser")
        fc.purgeAllCaches()

        sort.setSort([SortField("parser", byteParser()),
                      SortField.FIELD_DOC])
        self._assertMatches(self.full, self.queryA, sort, "JIHGFEDCBA")
        self._assertSaneFieldCaches(self.getName() + " ByteParser")
        fc.purgeAllCaches()

        sort.setSort([SortField("parser", shortParser()),
                      SortField.FIELD_DOC])
        self._assertMatches(self.full, self.queryA, sort, "JIHGFEDCBA")
        self._assertSaneFieldCaches(self.getName() + " ShortParser")
        fc.purgeAllCaches()

    def testEmptyIndex(self):
        """
        test sorts when there's nothing in the index
        """

        sort = Sort()
        empty = self._getEmptyIndex()

        self._assertMatches(empty, self.queryX, sort, "")

        sort.setSort(SortField.FIELD_DOC)
        self._assertMatches(empty, self.queryX, sort, "")

        sort.setSort([SortField("int", SortField.INT), SortField.FIELD_DOC])
        self._assertMatches(empty, self.queryX, sort, "")

        sort.setSort([SortField("string", SortField.STRING, True),
                      SortField.FIELD_DOC])
        self._assertMatches(empty, self.queryX, sort, "")

        sort.setSort([SortField("float", SortField.FLOAT),
                      SortField("string", SortField.STRING)])
        self._assertMatches(empty, self.queryX, sort, "")


    def testNewCustomFieldParserSort(self):
        """
        Test sorting w/ custom FieldComparator
        """
        sort = Sort()

        sort.setSort([SortField("parser", MyFieldComparatorSource())])
        self._assertMatches(self.full, self.queryA, sort, "JIHGFEDCBA")

    def testReverseSort(self):
        """
        test sorts in reverse
        """
        sort = Sort()

        sort.setSort([SortField(None, SortField.SCORE, True),
                      SortField.FIELD_DOC])
        self._assertMatches(self.full, self.queryX, sort, "IEGCA")
        self._assertMatches(self.full, self.queryY, sort, "JFHDB")

        sort.setSort(SortField(None, SortField.DOC, True))
        self._assertMatches(self.full, self.queryX, sort, "IGECA")
        self._assertMatches(self.full, self.queryY, sort, "JHFDB")

        sort.setSort(SortField("int", SortField.INT, True))
        self._assertMatches(self.full, self.queryX, sort, "CAEGI")
        self._assertMatches(self.full, self.queryY, sort, "BJFHD")

        sort.setSort(SortField("float", SortField.FLOAT, True))
        self._assertMatches(self.full, self.queryX, sort, "AECIG")
        self._assertMatches(self.full, self.queryY, sort, "BFJHD")

        sort.setSort(SortField("string", SortField.STRING, True))
        self._assertMatches(self.full, self.queryX, sort, "CEGIA")
        self._assertMatches(self.full, self.queryY, sort, "BFHJD")

    def testEmptyFieldSort(self):
        """
        test sorting when the sort field is empty(undefined) for some of the
        documents
        """
        sort = Sort()

        sort.setSort(SortField("string", SortField.STRING))
        self._assertMatches(self.full, self.queryF, sort, "ZJI")

        sort.setSort(SortField("string", SortField.STRING, True))
        self._assertMatches(self.full, self.queryF, sort, "IJZ")
    
        sort.setSort(SortField("i18n", Locale.ENGLISH))
        self._assertMatches(self.full, self.queryF, sort, "ZJI")
    
        sort.setSort(SortField("i18n", Locale.ENGLISH, True))
        self._assertMatches(self.full, self.queryF, sort, "IJZ")

        sort.setSort(SortField("int", SortField.INT))
        self._assertMatches(self.full, self.queryF, sort, "IZJ")

        sort.setSort(SortField("int", SortField.INT, True))
        self._assertMatches(self.full, self.queryF, sort, "JZI")

        sort.setSort(SortField("float", SortField.FLOAT))
        self._assertMatches(self.full, self.queryF, sort, "ZJI")

        # using a nonexisting field as first sort key shouldn't make a
        # difference:
        sort.setSort([SortField("nosuchfield", SortField.STRING),
                      SortField("float", SortField.FLOAT)])
        self._assertMatches(self.full, self.queryF, sort, "ZJI")

        sort.setSort(SortField("float", SortField.FLOAT, True))
        self._assertMatches(self.full, self.queryF, sort, "IJZ")

        # When a field is None for both documents, the next SortField should
        # be used. 
        # Works for
        sort.setSort([SortField("int", SortField.INT),
                      SortField("string", SortField.STRING),
                      SortField("float", SortField.FLOAT)])
        self._assertMatches(self.full, self.queryG, sort, "ZWXY")

        # Reverse the last criterium to make sure the test didn't pass by
        # chance 
        sort.setSort([SortField("int", SortField.INT),
                      SortField("string", SortField.STRING),
                      SortField("float", SortField.FLOAT, True)])
        self._assertMatches(self.full, self.queryG, sort, "ZYXW")

        # Do the same for a MultiSearcher
        multiSearcher = MultiSearcher([self.full])

        sort.setSort([SortField("int", SortField.INT),
                      SortField("string", SortField.STRING),
                      SortField("float", SortField.FLOAT)])
        self._assertMatches(multiSearcher, self.queryG, sort, "ZWXY")

        sort.setSort([SortField("int", SortField.INT),
                      SortField("string", SortField.STRING),
                      SortField("float", SortField.FLOAT, True)])
        self._assertMatches(multiSearcher, self.queryG, sort, "ZYXW")

        # Don't close the multiSearcher. it would close the full searcher too!
        # Do the same for a ParallelMultiSearcher
        parallelSearcher = ParallelMultiSearcher([self.full])

        sort.setSort([SortField("int", SortField.INT),
                      SortField("string", SortField.STRING),
                      SortField("float", SortField.FLOAT)])
        self._assertMatches(parallelSearcher, self.queryG, sort, "ZWXY")

        sort.setSort([SortField("int", SortField.INT),
                      SortField("string", SortField.STRING),
                      SortField("float", SortField.FLOAT, True)])
        self._assertMatches(parallelSearcher, self.queryG, sort, "ZYXW")

        # Don't close the parallelSearcher. it would close the full searcher
        # too!

    def testSortCombos(self):
        """
        test sorts using a series of fields
        """
        sort = Sort()

        sort.setSort([SortField("int", SortField.INT),
                      SortField("float", SortField.FLOAT)])
        self._assertMatches(self.full, self.queryX, sort, "IGEAC")

        sort.setSort([SortField("int", SortField.INT, True),
                      SortField(None, SortField.DOC, True)])
        self._assertMatches(self.full, self.queryX, sort, "CEAGI")

        sort.setSort([SortField("float", SortField.FLOAT),
                      SortField("string", SortField.STRING)])
        self._assertMatches(self.full, self.queryX, sort, "GICEA")

    def testLocaleSort(self):
        """
        test using a Locale for sorting strings
        """
        sort = Sort()

        sort.setSort([SortField("string", Locale.US)])
        self._assertMatches(self.full, self.queryX, sort, "AIGEC")
        self._assertMatches(self.full, self.queryY, sort, "DJHFB")

        sort.setSort([SortField("string", Locale.US, True)])
        self._assertMatches(self.full, self.queryX, sort, "CEGIA")
        self._assertMatches(self.full, self.queryY, sort, "BFHJD")

    def testInternationalSort(self):
        """
        test using various international locales with accented characters
        (which sort differently depending on locale)
        """
        sort = Sort()

        sort.setSort(SortField("i18n", Locale.US))
        self._assertMatches(self.full, self.queryY, sort, "BFJDH")

        sort.setSort(SortField("i18n", Locale("sv", "se")))
        self._assertMatches(self.full, self.queryY, sort, "BJDFH")

        sort.setSort(SortField("i18n", Locale("da", "dk")))
        self._assertMatches(self.full, self.queryY, sort, "BJDHF")

        sort.setSort(SortField("i18n", Locale.US))
        self._assertMatches(self.full, self.queryX, sort, "ECAGI")

        sort.setSort(SortField("i18n", Locale.FRANCE))
        self._assertMatches(self.full, self.queryX, sort, "EACGI")

    def testInternationalMultiSearcherSort(self):
        """
        Test the MultiSearcher's ability to preserve locale-sensitive ordering
        by wrapping it around a single searcher
        """
        sort = Sort()

        multiSearcher = MultiSearcher([self.full])
        sort.setSort(SortField("i18n", Locale("sv", "se")))
        self._assertMatches(multiSearcher, self.queryY, sort, "BJDFH")
    
        sort.setSort(SortField("i18n", Locale.US))
        self._assertMatches(multiSearcher, self.queryY, sort, "BFJDH")
    
        sort.setSort(SortField("i18n", Locale("da", "dk")))
        self._assertMatches(multiSearcher, self.queryY, sort, "BJDHF")
    
    def testMultiSort(self):
        """
        test a variety of sorts using more than one searcher
        """
        
        searcher = MultiSearcher([self.searchX, self.searchY])
        self.runMultiSorts(searcher, False)

    def testParallelMultiSort(self):
        """
        test a variety of sorts using a parallel multisearcher
        """

        searcher = ParallelMultiSearcher([self.searchX, self.searchY])
        self.runMultiSorts(searcher, False)

    def testNormalizedScores(self):
        """
        test that the relevancy scores are the same even if
        hits are sorted
        """

        # capture relevancy scores
        scoresX = self.getScores(self.full.search(self.queryX, None,
                                                  1000).scoreDocs, self.full)
        scoresY = self.getScores(self.full.search(self.queryY, None,
                                                  1000).scoreDocs, self.full)
        scoresA = self.getScores(self.full.search(self.queryA, None,
                                                  1000).scoreDocs, self.full)

        # we'll test searching locally, remote and multi
        multi = MultiSearcher([self.searchX, self.searchY])

        # change sorting and make sure relevancy stays the same

        sort = Sort()
        self._assertSameValues(scoresX, self.getScores(self.full.search(self.queryX, None, 1000, sort).scoreDocs, self.full))
        self._assertSameValues(scoresX, self.getScores(multi.search(self.queryX, None, 1000, sort).scoreDocs, multi))
        self._assertSameValues(scoresY, self.getScores(self.full.search(self.queryY, None, 1000, sort).scoreDocs, self.full))
        self._assertSameValues(scoresY, self.getScores(multi.search(self.queryY, None, 1000, sort).scoreDocs, multi))
        self._assertSameValues(scoresA, self.getScores(self.full.search(self.queryA, None, 1000, sort).scoreDocs, self.full))
        self._assertSameValues(scoresA, self.getScores(multi.search(self.queryA, None, 1000, sort).scoreDocs, multi))

        sort.setSort(SortField.FIELD_DOC)
        self._assertSameValues(scoresX, self.getScores(self.full.search(self.queryX, None, 1000, sort).scoreDocs, self.full))
        self._assertSameValues(scoresX, self.getScores(multi.search(self.queryX, None, 1000, sort).scoreDocs, multi))
        self._assertSameValues(scoresY, self.getScores(self.full.search(self.queryY, None, 1000, sort).scoreDocs, self.full))
        self._assertSameValues(scoresY, self.getScores(multi.search(self.queryY, None, 1000, sort).scoreDocs, multi))
        self._assertSameValues(scoresA, self.getScores(self.full.search(self.queryA, None, 1000, sort).scoreDocs, self.full))
        self._assertSameValues(scoresA, self.getScores(multi.search(self.queryA, None, 1000, sort).scoreDocs, multi))

        sort.setSort(SortField("int", SortField.INT))
        self._assertSameValues(scoresX, self.getScores(self.full.search(self.queryX, None, 1000, sort).scoreDocs, self.full))
        self._assertSameValues(scoresX, self.getScores(multi.search(self.queryX, None, 1000, sort).scoreDocs, multi))
        self._assertSameValues(scoresY, self.getScores(self.full.search(self.queryY, None, 1000, sort).scoreDocs, self.full))
        self._assertSameValues(scoresY, self.getScores(multi.search(self.queryY, None, 1000, sort).scoreDocs, multi))
        self._assertSameValues(scoresA, self.getScores(self.full.search(self.queryA, None, 1000, sort).scoreDocs, self.full))
        self._assertSameValues(scoresA, self.getScores(multi.search(self.queryA, None, 1000, sort).scoreDocs, multi))

        sort.setSort(SortField("float", SortField.FLOAT))
        self._assertSameValues(scoresX, self.getScores(self.full.search(self.queryX, None, 1000, sort).scoreDocs, self.full))
        self._assertSameValues(scoresX, self.getScores(multi.search(self.queryX, None, 1000, sort).scoreDocs, multi))
        self._assertSameValues(scoresY, self.getScores(self.full.search(self.queryY, None, 1000, sort).scoreDocs, self.full))
        self._assertSameValues(scoresY, self.getScores(multi.search(self.queryY, None, 1000, sort).scoreDocs, multi))
        self._assertSameValues(scoresA, self.getScores(self.full.search(self.queryA, None, 1000, sort).scoreDocs, self.full))
        self._assertSameValues(scoresA, self.getScores(multi.search(self.queryA, None, 1000, sort).scoreDocs, multi))

        sort.setSort(SortField("string", SortField.STRING))
        self._assertSameValues(scoresX, self.getScores(self.full.search(self.queryX, None, 1000, sort).scoreDocs, self.full))
        self._assertSameValues(scoresX, self.getScores(multi.search(self.queryX, None, 1000, sort).scoreDocs, multi))
        self._assertSameValues(scoresY, self.getScores(self.full.search(self.queryY, None, 1000, sort).scoreDocs, self.full))
        self._assertSameValues(scoresY, self.getScores(multi.search(self.queryY, None, 1000, sort).scoreDocs, multi))
        self._assertSameValues(scoresA, self.getScores(self.full.search(self.queryA, None, 1000, sort).scoreDocs, self.full))
        self._assertSameValues(scoresA, self.getScores(multi.search(self.queryA, None, 1000, sort).scoreDocs, multi))

        sort.setSort([SortField("int", SortField.INT),
                      SortField("float", SortField.FLOAT)])
        self._assertSameValues(scoresX, self.getScores(self.full.search(self.queryX, None, 1000, sort).scoreDocs, self.full))
        self._assertSameValues(scoresX, self.getScores(multi.search(self.queryX, None, 1000, sort).scoreDocs, multi))
        self._assertSameValues(scoresY, self.getScores(self.full.search(self.queryY, None, 1000, sort).scoreDocs, self.full))
        self._assertSameValues(scoresY, self.getScores(multi.search(self.queryY, None, 1000, sort).scoreDocs, multi))
        self._assertSameValues(scoresA, self.getScores(self.full.search(self.queryA, None, 1000, sort).scoreDocs, self.full))
        self._assertSameValues(scoresA, self.getScores(multi.search(self.queryA, None, 1000, sort).scoreDocs, multi))

        sort.setSort([SortField("int", SortField.INT, True),
                      SortField(None, SortField.DOC, True)])
        self._assertSameValues(scoresX, self.getScores(self.full.search(self.queryX, None, 1000, sort).scoreDocs, self.full))
        self._assertSameValues(scoresX, self.getScores(multi.search(self.queryX, None, 1000, sort).scoreDocs, multi))
        self._assertSameValues(scoresY, self.getScores(self.full.search(self.queryY, None, 1000, sort).scoreDocs, self.full))
        self._assertSameValues(scoresY, self.getScores(multi.search(self.queryY, None, 1000, sort).scoreDocs, multi))
        self._assertSameValues(scoresA, self.getScores(self.full.search(self.queryA, None, 1000, sort).scoreDocs, self.full))
        self._assertSameValues(scoresA, self.getScores(multi.search(self.queryA, None, 1000, sort).scoreDocs, multi))

        sort.setSort([SortField("float", SortField.FLOAT),
                      SortField("string", SortField.STRING)])
        self._assertSameValues(scoresX, self.getScores(self.full.search(self.queryX, None, 1000, sort).scoreDocs, self.full))
        self._assertSameValues(scoresX, self.getScores(multi.search(self.queryX, None, 1000, sort).scoreDocs, multi))
        self._assertSameValues(scoresY, self.getScores(self.full.search(self.queryY, None, 1000, sort).scoreDocs, self.full))
        self._assertSameValues(scoresY, self.getScores(multi.search(self.queryY, None, 1000, sort).scoreDocs, multi))
        self._assertSameValues(scoresA, self.getScores(self.full.search(self.queryA, None, 1000, sort).scoreDocs, self.full))
        self._assertSameValues(scoresA, self.getScores(multi.search(self.queryA, None, 1000, sort).scoreDocs, multi))

    def testTopDocsScores(self):
        """
        There was previously a bug in FieldSortedHitQueue.maxscore when only
        a single doc was added.  That is what the following tests for.
        """
        
        sort = Sort()
        nDocs = 10

        # try to pick a query that will result in an unnormalized
        # score greater than 1 to test for correct normalization
        docs1 = self.full.search(self.queryE, None, nDocs, sort)

        # a filter that only allows through the first hit
        class filter(PythonFilter):
            def getDocIdSet(_self, reader):
                bs = BitSet(reader.maxDoc())
                bs.set(0, reader.maxDoc())
                bs.set(docs1.scoreDocs[0].doc)
                return DocIdBitSet(bs)

        filt = filter()

        docs2 = self.full.search(self.queryE, filt, nDocs, sort)
        self.assertEqual(docs1.scoreDocs[0].score,
                         docs2.scoreDocs[0].score,
                         1e-6)
  
    def testSortWithoutFillFields(self):
        """
        There was previously a bug in TopFieldCollector when fillFields was
        set to False - the same doc and score was set in ScoreDoc[]
        array. This test asserts that if fillFields is False, the documents
        are set properly. It does not use Searcher's default search
        methods(with Sort) since all set fillFields to True.
        """

        sorts = [Sort(SortField.FIELD_DOC), Sort()]
        for sort in sorts:
            q = MatchAllDocsQuery()
            tdc = TopFieldCollector.create(sort, 10, False,
                                           False, False, True)
            self.full.search(q, tdc)
      
            sds = tdc.topDocs().scoreDocs
            for i in xrange(1, len(sds)):
                self.assert_(sds[i].doc != sds[i - 1].doc)

    def testSortWithoutScoreTracking(self):
        """
        Two Sort criteria to instantiate the multi/single comparators.
        """

        sorts = [Sort(SortField.FIELD_DOC), Sort()]
        for sort in sorts:
            q = MatchAllDocsQuery()
            tdc = TopFieldCollector.create(sort, 10, True, False,
                                           False, True)
      
            self.full.search(q, tdc)
      
            tds = tdc.topDocs()
            sds = tds.scoreDocs
            for sd in sds:
                self.assert_(Float.isNaN_(sd.score))

            self.assert_(Float.isNaN_(tds.getMaxScore()))

    def testSortWithScoreNoMaxScoreTracking(self):
        """
        Two Sort criteria to instantiate the multi/single comparators.
        """
        
        sorts = [Sort(SortField.FIELD_DOC), Sort()]
        for sort in sorts:
            q = MatchAllDocsQuery()
            tdc = TopFieldCollector.create(sort, 10, True, True,
                                           False, True)
      
            self.full.search(q, tdc)
      
            tds = tdc.topDocs()
            sds = tds.scoreDocs
            for sd in sds:
                self.assert_(not Float.isNaN_(sd.score))

            self.assert_(Float.isNaN_(tds.getMaxScore()))
  
    def testSortWithScoreAndMaxScoreTracking(self):
        """
        Two Sort criteria to instantiate the multi/single comparators.
        """
        
        sorts = [Sort(SortField.FIELD_DOC), Sort()]
        for sort in sorts:
            q = MatchAllDocsQuery()
            tdc = TopFieldCollector.create(sort, 10, True, True,
                                           True, True)
      
            self.full.search(q, tdc)
      
            tds = tdc.topDocs()
            sds = tds.scoreDocs
            for sd in sds:
                self.assert_(not Float.isNaN_(sd.score))

            self.assert_(not Float.isNaN_(tds.getMaxScore()))

    def testOutOfOrderDocsScoringSort(self):
        """
        Two Sort criteria to instantiate the multi/single comparators.
        """

        sorts = [Sort(SortField.FIELD_DOC), Sort()]

        tfcOptions = [[False, False, False],
                      [False, False, True],
                      [False, True, False],
                      [False, True, True],
                      [True, False, False],
                      [True, False, True],
                      [True, True, False],
                      [True, True, True]]

        actualTFCClasses = [
            "OutOfOrderOneComparatorNonScoringCollector", 
            "OutOfOrderOneComparatorScoringMaxScoreCollector", 
            "OutOfOrderOneComparatorScoringNoMaxScoreCollector", 
            "OutOfOrderOneComparatorScoringMaxScoreCollector", 
            "OutOfOrderOneComparatorNonScoringCollector", 
            "OutOfOrderOneComparatorScoringMaxScoreCollector", 
            "OutOfOrderOneComparatorScoringNoMaxScoreCollector", 
            "OutOfOrderOneComparatorScoringMaxScoreCollector" 
        ]
    
        bq = BooleanQuery()

        # Add a Query with SHOULD, since bw.scorer() returns BooleanScorer2
        # which delegates to BS if there are no mandatory clauses.
        bq.add(MatchAllDocsQuery(), BooleanClause.Occur.SHOULD)

        # Set minNrShouldMatch to 1 so that BQ will not optimize rewrite to
        # return the clause instead of BQ.
        bq.setMinimumNumberShouldMatch(1)

        for sort in sorts:
            for tfcOption, actualTFCClass in izip(tfcOptions,
                                                  actualTFCClasses):
                tdc = TopFieldCollector.create(sort, 10, tfcOption[0],
                                               tfcOption[1], tfcOption[2],
                                               False)

                self.assert_(tdc.getClass().getName().endswith("$" + actualTFCClass))
          
                self.full.search(bq, tdc)
          
                tds = tdc.topDocs()
                sds = tds.scoreDocs  
                self.assertEqual(10, len(sds))
  
    def testSortWithScoreAndMaxScoreTrackingNoResults(self):
        """
        Two Sort criteria to instantiate the multi/single comparators.
        """

        sorts = [Sort(SortField.FIELD_DOC), Sort()]
        for sort in sorts:
            tdc = TopFieldCollector.create(sort, 10, True, True, True, True)
            tds = tdc.topDocs()
            self.assertEqual(0, tds.totalHits)
            self.assert_(Float.isNaN_(tds.getMaxScore()))
  
    def runMultiSorts(self, multi, isFull):
        """
        runs a variety of sorts useful for multisearchers
        """
        sort = Sort()

        sort.setSort(SortField.FIELD_DOC)
        expected = isFull and "ABCDEFGHIJ" or "ACEGIBDFHJ"
        self._assertMatches(multi, self.queryA, sort, expected)

        sort.setSort(SortField("int", SortField.INT))
        expected = isFull and "IDHFGJABEC" or "IDHFGJAEBC"
        self._assertMatches(multi, self.queryA, sort, expected)

        sort.setSort([SortField("int", SortField.INT), SortField.FIELD_DOC])
        expected = isFull and "IDHFGJABEC" or "IDHFGJAEBC"
        self._assertMatches(multi, self.queryA, sort, expected)

        sort.setSort(SortField("int", SortField.INT))
        expected = isFull and "IDHFGJABEC" or "IDHFGJAEBC"
        self._assertMatches(multi, self.queryA, sort, expected)

        sort.setSort([SortField("float", SortField.FLOAT), SortField.FIELD_DOC])
        self._assertMatches(multi, self.queryA, sort, "GDHJCIEFAB")

        sort.setSort(SortField("float", SortField.FLOAT))
        self._assertMatches(multi, self.queryA, sort, "GDHJCIEFAB")

        sort.setSort(SortField("string", SortField.STRING))
        self._assertMatches(multi, self.queryA, sort, "DJAIHGFEBC")

        sort.setSort(SortField("int", SortField.INT, True))
        expected = isFull and "CABEJGFHDI" or "CAEBJGFHDI"
        self._assertMatches(multi, self.queryA, sort, expected)

        sort.setSort(SortField("float", SortField.FLOAT, True))
        self._assertMatches(multi, self.queryA, sort, "BAFECIJHDG")

        sort.setSort(SortField("string", SortField.STRING, True))
        self._assertMatches(multi, self.queryA, sort, "CBEFGHIAJD")

        sort.setSort([SortField("int", SortField.INT),
                      SortField("float", SortField.FLOAT)])
        self._assertMatches(multi, self.queryA, sort, "IDHFGJEABC")

        sort.setSort([SortField("float", SortField.FLOAT),
                      SortField("string", SortField.STRING)])
        self._assertMatches(multi, self.queryA, sort, "GDHJICEFAB")

        sort.setSort(SortField("int", SortField.INT))
        self._assertMatches(multi, self.queryF, sort, "IZJ")

        sort.setSort(SortField("int", SortField.INT, True))
        self._assertMatches(multi, self.queryF, sort, "JZI")

        sort.setSort(SortField("float", SortField.FLOAT))
        self._assertMatches(multi, self.queryF, sort, "ZJI")

        sort.setSort(SortField("string", SortField.STRING))
        self._assertMatches(multi, self.queryF, sort, "ZJI")

        sort.setSort(SortField("string", SortField.STRING, True))
        self._assertMatches(multi, self.queryF, sort, "IJZ")

        # up to this point, all of the searches should have "sane" 
        # FieldCache behavior, and should have reused hte cache in several
        # cases 
        self._assertSaneFieldCaches(self.getName() + " various")
        
        # next we'll check Locale based(String[]) for 'string', so purge first
        FieldCache.DEFAULT.purgeAllCaches()

        sort.setSort([SortField("string", Locale.US)])
        self._assertMatches(multi, self.queryA, sort, "DJAIHGFEBC")

        sort.setSort([SortField("string", Locale.US, True)])
        self._assertMatches(multi, self.queryA, sort, "CBEFGHIAJD")

        sort.setSort([SortField("string", Locale.UK)])
        self._assertMatches(multi, self.queryA, sort, "DJAIHGFEBC")

        self._assertSaneFieldCaches(self.getName() + " Locale.US + Locale.UK")
        FieldCache.DEFAULT.purgeAllCaches()

    def _assertMatches(self, searcher, query, sort, expectedResult):
        """
        make sure the documents returned by the search match the expected
        list
        """

        # ScoreDoc[] result = searcher.search(query, None, 1000, sort).scoreDocs
        hits = searcher.search(query, None, len(expectedResult) or 1, sort)
        sds = hits.scoreDocs

        self.assertEqual(hits.totalHits, len(expectedResult))
        buff = []
        for sd in sds:
            doc = searcher.doc(sd.doc)
            v = doc.getValues("tracer")
            for _v in v:
                buff.append(_v)

        self.assertEqual(expectedResult, ''.join(buff))

    def getScores(self, hits, searcher):

        scoreMap = {}
        for hit in hits:
            doc = searcher.doc(hit.doc)
            v = doc.getValues("tracer")
            self.assertEqual(len(v), 1)
            scoreMap[v[0]] = hit.score

        return scoreMap

    def _assertSameValues(self, m1, m2):
        """
        make sure all the values in the maps match
        """

        self.assertEquals(len(m1), len(m2))
        for key in m1.iterkeys():
            self.assertEquals(m1[key], m2[key], 1e-6)

    def getName(self):

        return type(self).__name__

    def _assertSaneFieldCaches(self, msg):

        entries = FieldCache.DEFAULT.getCacheEntries()

        insanity = FieldCacheSanityChecker.checkSanity(entries)
        self.assertEqual(0, len(insanity),
                         msg + ": Insane FieldCache usage(s) found")


class MyFieldComparator(PythonFieldComparator):

    def __init__(self, numHits):
        super(MyFieldComparator, self).__init__()
        self.slotValues = [0] * numHits

    def copy(self, slot, doc):
        self.slotValues[slot] = self.docValues[doc]

    def compare(self, slot1, slot2):
        return self.slotValues[slot1] - self.slotValues[slot2]

    def compareBottom(self, doc):
        return self.bottomValue - self.docValues[doc]

    def setBottom(self, bottom):
        self.bottomValue = self.slotValues[bottom]

    def setNextReader(self, reader, docBase):
        
        class intParser(PythonIntParser):
            def parseInt(_self, val):
                return (ord(val[0]) - ord('A')) * 123456
                
        self.docValues = FieldCache.DEFAULT.getInts(reader, "parser",
                                                    intParser())

    def value(self, slot):
        return Integer(self.slotValues[slot])


class MyFieldComparatorSource(PythonFieldComparatorSource):

    def newComparator(self, fieldname, numHits, sortPos, reversed):
        return MyFieldComparator(numHits)



if __name__ == "__main__":
    import sys, lucene
    env = lucene.initVM()
    if '-loop' in sys.argv:
        sys.argv.remove('-loop')
        while True:
            try:
                main()
            except:
                pass
#            refs = sorted(env._dumpRefs(classes=True).items(),
#                          key=lambda x: x[1], reverse=True)
#            print refs[0:4]
    else:
        main()
