
import os, sys, lucene
lucene.initVM()

baseDir = os.path.dirname(os.path.abspath(sys.argv[0]))
sys.path.append(baseDir)

from lia.analysis.synonym.SynonymAnalyzerViewer import SynonymAnalyzerViewer
SynonymAnalyzerViewer.main([sys.argv[0], os.path.join(baseDir,
                                                      'indexes', 'wordnet')])
