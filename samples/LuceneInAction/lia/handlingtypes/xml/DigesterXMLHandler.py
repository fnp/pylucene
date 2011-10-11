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

from lucene import Document, Field
from lia.handlingtypes.xml.Digester import Digester


class DigesterXMLHandler(object):

    def __init__(self):

        self.digester = digester = Digester()

        digester.addSetProperty("address-book/contact", "type", "type")
        digester.addSetProperty("address-book/contact/name", "name")
        digester.addSetProperty("address-book/contact/address", "address")
        digester.addSetProperty("address-book/contact/city", "city")
        digester.addSetProperty("address-book/contact/province", "province")
        digester.addSetProperty("address-book/contact/postalcode", "postalcode")
        digester.addSetProperty("address-book/contact/country", "country")
        digester.addSetProperty("address-book/contact/telephone", "telephone")

    def indexFile(self, writer, path):

        try:
            file = open(path)
        except IOError, e:
            raise
        else:
            props = self.digester.parse(file)
            doc = Document()
            doc.add(Field("type", props['type'],
                          Field.Store.YES, Field.Index.NOT_ANALYZED))
            doc.add(Field("name", props['name'],
                          Field.Store.YES, Field.Index.NOT_ANALYZED))
            doc.add(Field("address", props['address'],
                          Field.Store.YES, Field.Index.NOT_ANALYZED))
            doc.add(Field("city", props['city'],
                          Field.Store.YES, Field.Index.NOT_ANALYZED))
            doc.add(Field("province", props['province'],
                          Field.Store.YES, Field.Index.NOT_ANALYZED))
            doc.add(Field("postalcode", props['postalcode'],
                          Field.Store.YES, Field.Index.NOT_ANALYZED))
            doc.add(Field("country", props['country'],
                          Field.Store.YES, Field.Index.NOT_ANALYZED))
            doc.add(Field("telephone", props['telephone'],
                          Field.Store.YES, Field.Index.NOT_ANALYZED))
            doc.add(Field("filename", os.path.abspath(path),
                          Field.Store.YES, Field.Index.NOT_ANALYZED))
            writer.addDocument(doc)
            file.close()

            return doc
