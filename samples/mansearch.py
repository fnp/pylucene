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
#
# Author: Erik Hatcher
#
# to query the index generated with manindex.py
#  python mansearch.py <query>
# by default, the index is stored in 'pages', which can be overriden with
# the MANDEX environment variable
# ====================================================================


import sys, os

from string import Template
from datetime import datetime
from getopt import getopt, GetoptError

from lucene import \
     Document, IndexSearcher, SimpleFSDirectory, File, QueryParser, \
     StandardAnalyzer, initVM, Version

if __name__ == '__main__':
    initVM()

def usage():
    print sys.argv[0], "[--format=<format string>] [--index=<index dir>] [--stats] <query...>"
    print "default index is found from MANDEX environment variable"

try:
    options, args = getopt(sys.argv[1:], '', ['format=', 'index=', 'stats'])
except GetoptError:
    usage()
    sys.exit(2)


format = "#name"
indexDir = os.environ.get('MANDEX') or 'pages'
stats = False
for o, a in options:
    if o == "--format":
        format = a
    elif o == "--index":
        indexDir = a
    elif o == "--stats":
        stats = True


class CustomTemplate(Template):
    delimiter = '#'

template = CustomTemplate(format)

fsDir = SimpleFSDirectory(File(indexDir))
searcher = IndexSearcher(fsDir, True)

analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
parser = QueryParser(Version.LUCENE_CURRENT, "keywords", analyzer)
parser.setDefaultOperator(QueryParser.Operator.AND)
query = parser.parse(' '.join(args))
start = datetime.now()
scoreDocs = searcher.search(query, 50).scoreDocs
duration = datetime.now() - start
if stats:
    print >>sys.stderr, "Found %d document(s) (in %s) that matched query '%s':" %(len(scoreDocs), duration, query)

for scoreDoc in scoreDocs:
    doc = searcher.doc(scoreDoc.doc)
    table = dict((field.name(), field.stringValue())
                 for field in doc.getFields())
    print template.substitute(table)
