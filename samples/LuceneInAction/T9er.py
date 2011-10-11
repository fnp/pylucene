
import os, sys, lucene
lucene.initVM()

sys.path.append(os.path.dirname(os.path.abspath(sys.argv[0])))

from lia.tools.T9er import T9er
T9er.main(sys.argv)
