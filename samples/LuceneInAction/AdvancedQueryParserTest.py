
import os, sys, unittest, lucene
lucene.initVM()

sys.path.append(os.path.dirname(os.path.abspath(sys.argv[0])))

import lia.extsearch.queryparser.AdvancedQueryParserTest
unittest.main(lia.extsearch.queryparser.AdvancedQueryParserTest)
