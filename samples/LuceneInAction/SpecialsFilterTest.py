
import os, sys, unittest, lucene
lucene.initVM()

baseDir = os.path.dirname(os.path.abspath(sys.argv[0]))
sys.path.append(baseDir)

import lia.extsearch.filters.SpecialsFilterTest
from lucene import System

System.setProperty("index.dir", os.path.join(baseDir, 'index'))
unittest.main(lia.extsearch.filters.SpecialsFilterTest)
