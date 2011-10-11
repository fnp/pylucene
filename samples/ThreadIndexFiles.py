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

# This sample illustrates how to use a thread with PyLucene

import sys, os, threading

from datetime import datetime
from lucene import StandardAnalyzer, VERSION, initVM, Version
from IndexFiles import IndexFiles


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print IndexFiles.__doc__
        sys.exit(1)
    env=initVM()
    print 'lucene', VERSION

    def fn():
        env.attachCurrentThread()
        start = datetime.now()
        IndexFiles(sys.argv[1], "index",
                   StandardAnalyzer(Version.LUCENE_CURRENT))
        end = datetime.now()
        print end - start

    threading.Thread(target=fn).start()
