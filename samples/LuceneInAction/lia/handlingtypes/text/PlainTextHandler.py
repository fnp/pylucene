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

from lucene import Document, Field, \
    InputStreamReader, FileInputStream, JavaError


class PlainTextHandler(object):

    def indexFile(self, writer, path):

        try:
            reader = InputStreamReader(FileInputStream(path), 'iso-8859-1')
        except JavaError:
            raise
        else:
            doc = Document()
            doc.add(Field("contents", reader))
            doc.add(Field("filename", os.path.abspath(path),
                          Field.Store.YES, Field.Index.NOT_ANALYZED))
            writer.addDocument(doc)
            reader.close()

            return doc
