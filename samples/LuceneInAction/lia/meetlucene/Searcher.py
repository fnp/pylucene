# ====================================================================
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
# ====================================================================

import os

from time import time
from datetime import timedelta

from lucene import \
     Document, IndexSearcher, FSDirectory, QueryParser, StandardAnalyzer, \
     SimpleFSDirectory, File, Version


class Searcher(object):

    def main(cls, argv):

        if len(argv) != 3:
            print "Usage: python Searcher.py <index dir> <query>"

        else:
            indexDir = argv[1]
            q = argv[2]

            if not (os.path.exists(indexDir) and os.path.isdir(indexDir)):
                raise IOError, "%s does not exist or is not a directory" %(indexDir)

            cls.search(indexDir, q)

    def search(cls, indexDir, q):

        fsDir = SimpleFSDirectory(File(indexDir))
        searcher = IndexSearcher(fsDir, True)

        query = QueryParser(Version.LUCENE_CURRENT, "contents",
                            StandardAnalyzer(Version.LUCENE_CURRENT)).parse(q)
        start = time()
        hits = searcher.search(query, 50).scoreDocs
        duration = timedelta(seconds=time() - start)

        print "Found %d document(s) (in %s) that matched query '%s':" %(len(hits), duration, q)

        for hit in hits:
            doc = searcher.doc(hit.doc)
            print 'path:', doc.get("path")

    main = classmethod(main)
    search = classmethod(search)


if __name__ == "__main__":
    import sys
    Searcher.main(sys.argv)
