
import os, sys, unittest, lucene
lucene.initVM()

sys.path.append(os.path.dirname(os.path.abspath(sys.argv[0])))

from lia.analysis.positional.PositionalPorterStopAnalyzerTest import \
     PositionalPorterStopAnalyzerTest

PositionalPorterStopAnalyzerTest.main()

import lia.analysis.positional.PositionalPorterStopAnalyzerTest
unittest.main(lia.analysis.positional.PositionalPorterStopAnalyzerTest)
