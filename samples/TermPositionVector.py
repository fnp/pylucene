from lucene import \
    StandardAnalyzer, RAMDirectory, Document, Field, Version, \
    IndexWriter, IndexReader, TermPositionVector, initVM

if __name__ == '__main__':
    initVM()

directory = RAMDirectory()
iwriter = IndexWriter(directory, StandardAnalyzer(Version.LUCENE_CURRENT),
                      True, IndexWriter.MaxFieldLength.LIMITED)
ts = ["this bernhard is the text to be index text",
      "this claudia is the text to be index"]
for t in ts:
    doc = Document()
    doc.add(Field("fieldname", t,
                  Field.Store.YES, Field.Index.ANALYZED,
                  Field.TermVector.WITH_POSITIONS_OFFSETS))
    iwriter.addDocument(doc)
iwriter.optimize()
iwriter.close()

ireader = IndexReader.open(directory, True)
tpv = TermPositionVector.cast_(ireader.getTermFreqVector(0, 'fieldname'))

for (t,f,i) in zip(tpv.getTerms(),tpv.getTermFrequencies(),xrange(100000)):
    print 'term %s' % t
    print '  freq: %i' % f
    try:
        print '  pos: ' + str([p for p in tpv.getTermPositions(i)])
    except:
        print '  no pos'
    try:
        print '  off: ' + \
              str(["%i-%i" % (o.getStartOffset(), o.getEndOffset())
                   for o in tpv.getOffsets(i)])
    except:
        print '  no offsets'
