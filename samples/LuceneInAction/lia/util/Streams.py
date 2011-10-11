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

from StringIO import StringIO
from HTMLParser import HTMLParser


class InputStreamReader(object):

    def __init__(self, inputStream, encoding):

        super(InputStreamReader, self).__init__()
        self.inputStream = inputStream
        self.encoding = encoding or 'utf-8'

    def _read(self, length):

        return self.inputStream.read(length)

    def read(self, length=-1):

        text = self._read(length)
        text = unicode(text, self.encoding)

        return text

    def close(self):

        self.inputStream.close()


class HTMLReader(object):

    def __init__(self, reader):

        self.reader = reader

        class htmlParser(HTMLParser):

            def __init__(self):

                HTMLParser.__init__(self)

                self.buffer = StringIO()
                self.position = 0

            def handle_data(self, data):

                self.buffer.write(data)

            def _read(self, length):

                buffer = self.buffer
                size = buffer.tell() - self.position

                if length > 0 and size > length:
                    buffer.seek(self.position)
                    data = buffer.read(length)
                    self.position += len(data)
                    buffer.seek(0, 2)

                elif size > 0:
                    buffer.seek(self.position)
                    data = buffer.read(size)
                    self.position = 0
                    buffer.seek(0)

                else:
                    data = ''

                return data
                
        self.parser = htmlParser()

    def read(self, length=-1):

        while True:
            data = self.reader.read(length)
            if len(data) > 0:
                self.parser.feed(data)
                data = self.parser._read(length)
                if len(data) == 0:
                    continue
            return data

    def close(self):

        self.reader.close()
