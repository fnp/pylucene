
import os, sys, unittest, lucene
lucene.initVM()

sys.path.append(os.path.dirname(os.path.abspath(sys.argv[0])))

from lia.analysis.synonym.SynonymAnalyzerTest import SynonymAnalyzerTest
SynonymAnalyzerTest.main()

import lia.analysis.synonym.SynonymAnalyzerTest
unittest.main(lia.analysis.synonym.SynonymAnalyzerTest)
