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

from unittest import TestCase, main
from lucene import *

# run with -loop to test fix for string local ref leak reported
# by Aaron Lav.

class StopWordsTestCase(TestCase):

    def setUp(self):

        stopWords = ['the', 'and', 's']
        self.stop_set = HashSet()
        for stopWord in stopWords:
            self.stop_set.add(stopWord)

        self.reader = StringReader('foo')

    def testStopWords(self):

        try:
            result = StandardTokenizer(Version.LUCENE_CURRENT, self.reader)
            result = StopFilter(True, result, self.stop_set)
        except Exception, e:
            self.fail(str(e))


if __name__ == "__main__":
    import sys, lucene
    lucene.initVM()
    if '-loop' in sys.argv:
        sys.argv.remove('-loop')
        while True:
            try:
                main()
            except:
                pass
    else:
         main()
