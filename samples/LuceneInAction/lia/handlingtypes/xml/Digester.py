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

import xml.sax


class Digester(xml.sax.ContentHandler):

    attributes = {}
    tags = {}

    def addSetProperty(self, path, property, attribute=None):

        if attribute is not None:
            pairs = self.attributes.get(path)
            if pairs is None:
                self.attributes[path] = pairs = { attribute: property }
            else:
                pairs[property] = attribute

        else:
            self.tags[path] = property

    def parse(self, input):

        xml.sax.parse(input, self)
        return self.properties
    
    def startDocument(self):

        self.properties = {}
        self.path = []

    def startElement(self, tag, attrs):

        self.path.append(tag)
        pairs = self.attributes.get('/'.join(self.path))
        if pairs is not None:
            for name, value in attrs.items():
                property = pairs.get(name)
                if property is not None:
                    self.properties[property] = value

    def characters(self, data):

        self.data = data.strip()

    def endElement(self, tag):

        if self.data:
            property = self.tags.get('/'.join(self.path))
            if property is not None:
                self.properties[property] = self.data
            self.data = None
            
        self.path.pop()
