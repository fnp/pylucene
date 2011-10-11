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

from unittest import TestCase
from lucene import \
    SimpleFSDirectory, Document, \
    System, SimpleDateFormat, File


class LiaTestCase(TestCase):

    def __init__(self, *args):

        super(LiaTestCase, self).__init__(*args)
        self.indexDir = System.getProperty("index.dir")

    def setUp(self):

        self.directory = SimpleFSDirectory(File(self.indexDir))

    def tearDown(self):

        self.directory.close()

    #
    # For troubleshooting
    #
    def dumpHits(self, searcher, scoreDocs):

        if not scoreDocs:
            print "No hits"
        else:
            for scoreDoc in scoreDocs:
                print "%s: %s" %(scoreDoc.score,
                                 searcher.doc(scoreDoc.doc).get('title'))

    def assertHitsIncludeTitle(self, searcher, scoreDocs, title,
                               fail=False):

        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)
            if title == doc.get("title"):
                if fail:
                    self.fail("title '%s' found" %(title))
                return

        if not fail:
            self.fail("title '%s' not found" %(title))

    def parseDate(self, s):

        return SimpleDateFormat("yyyy-MM-dd").parse(s)
