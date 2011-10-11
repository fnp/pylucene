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
    PythonQueryParser, PythonMultiFieldQueryParser, \
    PhraseQuery, TermRangeQuery, SpanNearQuery, SpanTermQuery, \
    Term, PhraseQuery, Version

from lia.extsearch.queryparser.NumberUtils import NumberUtils

#
# A QueryParser extension
#

class CustomQueryParser(PythonQueryParser):

    def __init__(self, field, analyzer):
        super(CustomQueryParser, self).__init__(Version.LUCENE_CURRENT, field, analyzer)

    def getFuzzyQuery(self, field, termText, minSimilarity):
        raise AssertionError, "Fuzzy queries not allowed"

    def getWildcardQuery(self, field, termText):
        raise AssertionError, "Wildcard queries not allowed"

    #
    # Special handling for the "id" field, pads each part
    # to match how it was indexed.
    #
    def getRangeQuery(self, field, part1, part2, inclusive):

        if field == "id":

            num1 = int(part1)
            num2 = int(part2)

            return TermRangeQuery(field,
                                  NumberUtils.pad(num1),
                                  NumberUtils.pad(num2),
                                  inclusive, True)

        if field == "special":
            print part1, "->", part2

            return TermRangeQuery("field", part1, part2, inclusive, True)

        return super(CustomQueryParser,
                     self).getRangeQuery(field, part1, part2, inclusive)


    def getFieldQuery_quoted(self, field, queryText, quoted):

        return super(CustomQueryParser,
                     self).getFieldQuery_quoted_super(field, queryText, quoted)

    #
    # Replace PhraseQuery with SpanNearQuery to force in-order
    # phrase matching rather than reverse.
    #
    def getFieldQuery_slop(self, field, queryText, slop):

        orig = super(CustomQueryParser,
                     self).getFieldQuery_slop_super(field, queryText, slop)

        if not PhraseQuery.instance_(orig):
            return orig

        pq = PhraseQuery.cast_(orig)
        clauses = [SpanTermQuery(term) for term in pq.getTerms()]

        return SpanNearQuery(clauses, slop, True);



class MultiFieldCustomQueryParser(PythonMultiFieldQueryParser):

    def __init__(self, fields, analyzer):
        super(MultiFieldCustomQueryParser, self).__init__(Version.LUCENE_CURRENT, fields, analyzer)

    def getFuzzyQuery(self, super, field, termText, minSimilarity):
        raise AssertionError, "Fuzzy queries not allowed"

    def getWildcardQuery(self, super, field, termText):
        raise AssertionError, "Wildcard queries not allowed"

    #
    # Special handling for the "id" field, pads each part
    # to match how it was indexed.
    #
    def getRangeQuery(self, field, part1, part2, inclusive):

        if field == "id":

            num1 = int(part1)
            num2 = int(part2)

            return TermRangeQuery(field,
                                  NumberUtils.pad(num1),
                                  NumberUtils.pad(num2),
                                  inclusive, True)

        if field == "special":
            print part1, "->", part2

            return TermRangeQuery("field", part1, part2, inclusive, True)

        return super(CustomQueryParser,
                     self).getRangeQuery(field, part1, part2, inclusive)

    def getFieldQuery_quoted(self, field, queryText, quoted):

        return super(CustomQueryParser,
                     self).getFieldQuery_quoted_super(field, queryText, quoted)

    #
    # Replace PhraseQuery with SpanNearQuery to force in-order
    # phrase matching rather than reverse.
    #
    def getFieldQuery_slop(self, field, queryText, slop):

        # let QueryParser's implementation do the analysis
        orig = super(CustomQueryParser,
                     self).getFieldQuery_slop_super(field, queryText, slop)

        if not PhraseQuery.instance_(orig):
            return orig

        pq = PhraseQuery.cast_(orig)
        clauses = [SpanTermQuery(term) for term in pq.getTerms()]

        return SpanNearQuery(clauses, slop, True);
