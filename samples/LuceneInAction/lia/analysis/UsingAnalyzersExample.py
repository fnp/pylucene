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

from lucene import \
     RAMDirectory, IndexWriter, StandardAnalyzer, Document, Field, \
     QueryParser

class UsingAnalyzersExample(object):

    #
    # This method doesn't do anything, except compile correctly.
    # This is used to show snippets of how Analyzers are used.
    #
    def someMethod(self):

        directory = RAMDirectory()

        analyzer = StandardAnalyzer()
        writer = IndexWriter(directory, analyzer, True)

        doc = Document()
        doc.add(Field.Text("title", "This is the title"))
        doc.add(Field.UnStored("contents", "...document contents..."))
        writer.addDocument(doc)

        writer.addDocument(doc, analyzer)

        expression = "some query"

        query = QueryParser.parse(expression, "contents", analyzer)

        parser = QueryParser("contents", analyzer)
        query = parser.parseQuery(expression)
