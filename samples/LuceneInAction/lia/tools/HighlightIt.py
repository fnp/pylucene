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

from sys import stdout

from lucene import \
     StandardAnalyzer, Term, TermQuery, StringReader, Version, \
     Fragmenter, Highlighter, QueryScorer, SimpleFragmenter, SimpleHTMLFormatter


class HighlightIt(object):

    # from http://www.lipsum.com
    text = \
      """
      Contrary to popular belief, Lorem Ipsum is
      not simply random text. It has roots in a piece of
      classical Latin literature from 45 BC, making it over
      2000 years old. Richard McClintock, a Latin professor
      at Hampden-Sydney College in Virginia, looked up one
      of the more obscure Latin words, consectetur, from
      a Lorem Ipsum passage, and going through the cites
      of the word in classical literature, discovered the
      undoubtable source. Lorem Ipsum comes from sections
      1.10.32 and 1.10.33 of "de Finibus Bonorum et
      Malorum" (The Extremes of Good and Evil) by Cicero,
      written in 45 BC. This book is a treatise on the
      theory of ethics, very popular during the
      Renaissance. The first line of Lorem Ipsum, "Lorem
      ipsum dolor sit amet..", comes from a line in
      section 1.10.32.
      """

    def main(cls, argv):

        query = TermQuery(Term("f", "ipsum"))
        scorer = QueryScorer(query)
        formatter = SimpleHTMLFormatter("<span class=\"highlight\">", "</span>")
        highlighter = Highlighter(formatter, scorer)
        fragmenter = SimpleFragmenter(50)
        highlighter.setTextFragmenter(fragmenter)

        analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
        tokenStream = analyzer.tokenStream("f", StringReader(cls.text))
        result = highlighter.getBestFragments(tokenStream, cls.text, 5, "...")

        stdout.write("<html>")
        stdout.write("<style>\n")
        stdout.write(".highlight {\n")
        stdout.write(" background: yellow\n")
        stdout.write("}\n")
        stdout.write("</style>")

        stdout.write("<body>")
        stdout.write(result)
        stdout.write("</body></html>\n")
        stdout.flush()
        
    main = classmethod(main)
