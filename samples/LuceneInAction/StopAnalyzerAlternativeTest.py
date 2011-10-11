
import os, sys, unittest, lucene
lucene.initVM()

sys.path.append(os.path.dirname(os.path.abspath(sys.argv[0])))

from lia.analysis.stopanalyzer.StopAnalyzerAlternativeTest import \
     StopAnalyzerAlternativeTest

StopAnalyzerAlternativeTest.main()

import lia.analysis.stopanalyzer.StopAnalyzerAlternativeTest
unittest.main(lia.analysis.stopanalyzer.StopAnalyzerAlternativeTest)
