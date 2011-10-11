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

import os, popen2

from lucene import Document, Field, StringReader
from lia.util.Streams import InputStreamReader


class PDFHandler(object):

    def indexFile(self, writer, path):

        doc = Document()

        try:
            process = popen2.Popen4(["pdfinfo", "-enc", "UTF-8", path])
        except:
            raise
        else:
            while True:
                line = process.fromchild.readline().strip()
                if not line:
                    break
                name, value = line.split(':', 1)
                doc.add(Field(name.strip(), value.strip(),
                              Field.Store.YES, Field.Index.NOT_ANALYZED))

            exitCode = process.wait()
            if exitCode != 0:
                raise RuntimeError, "pdfinfo exit code %d" %(exitCode)
        
        try:
            process = popen2.Popen4(["pdftotext", "-enc", "UTF-8", path, "-"])
            string = InputStreamReader(process.fromchild, 'utf-8').read()
        except:
            raise
        else:
            doc.add(Field("contents", StringReader(string)))
            doc.add(Field("filename", os.path.abspath(path),
                          Field.Store.YES, Field.Index.NOT_ANALYZED))
            writer.addDocument(doc)

            exitCode = process.wait()
            if exitCode != 0:
                raise RuntimeError, "pdftotext exit code %d" %(exitCode)

            return doc
