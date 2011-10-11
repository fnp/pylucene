
import os, sys, lucene
lucene.initVM()

sys.path.append(os.path.dirname(os.path.abspath(sys.argv[0])))

from lia.searching.Explainer import Explainer
Explainer.main(sys.argv)
