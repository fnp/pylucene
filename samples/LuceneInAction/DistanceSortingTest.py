
import os, sys, unittest, lucene
lucene.initVM()

sys.path.append(os.path.dirname(os.path.abspath(sys.argv[0])))

import lia.extsearch.sorting.DistanceSortingTest
unittest.main(lia.extsearch.sorting.DistanceSortingTest)
