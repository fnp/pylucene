
import os, sys, lucene
lucene.initVM()

sys.path.append(os.path.dirname(os.path.abspath(sys.argv[0])))

from lia.analysis.AnalyzerUtils import AnalyzerUtils
AnalyzerUtils.main(sys.argv)
