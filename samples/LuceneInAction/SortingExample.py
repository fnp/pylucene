
import os, sys, lucene
lucene.initVM()

baseDir = os.path.dirname(os.path.abspath(sys.argv[0]))
sys.path.append(baseDir)

from lia.advsearching.SortingExample import SortingExample
from lucene import System

System.setProperty("index.dir", os.path.join(baseDir, 'index'))
SortingExample.main(sys.argv)
