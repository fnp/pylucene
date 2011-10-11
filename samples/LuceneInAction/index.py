
import os, sys, tarfile, lucene
lucene.initVM()

baseDir = os.path.dirname(os.path.abspath(sys.argv[0]))
sys.path.append(baseDir)

from lia.common.TestDataDocumentHandler import TestDataDocumentHandler

TestDataDocumentHandler.createIndex(os.path.join(baseDir, 'data'),
                                    os.path.join(baseDir, 'index'),
                                    False)

tar = tarfile.open(os.path.join(baseDir, 'indexes.tar.gz'), "r:gz")
while True:
    member = tar.next()
    if member is None:
        break
    print member.name
    tar.extract(member, baseDir)
tar.close()
