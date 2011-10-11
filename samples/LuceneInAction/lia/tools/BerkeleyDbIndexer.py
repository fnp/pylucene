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

from bsddb.db import DBEnv, DB
from bsddb.db import \
     DB_INIT_MPOOL, DB_INIT_LOCK, DB_INIT_TXN, DB_THREAD, DB_CREATE, DB_BTREE

# missing from python interface at the moment
DB_LOG_INMEMORY = 0x00020000

from lucene import \
     DbDirectory, IndexWriter, StandardAnalyzer, Document, Field


class BerkeleyDbIndexer(object):

    def main(cls, argv):

        if len(argv) < 2:
            print "Usage: BerkeleyDbIndexer <index dir> -create"
            return

        dbHome = argv[1]
        create = len(argv) > 2 and argv[2] == "-create"

        if not os.path.exists(dbHome):
            os.makedirs(dbHome)
        elif create:
            for name in os.listdir(dbHome):
                if name.startswith('__'):
                    os.remove(os.path.join(dbHome, name))

        env = DBEnv()
        env.set_flags(DB_LOG_INMEMORY, 1);
        if os.name == 'nt':
            env.set_cachesize(0, 0x4000000, 1)
        elif os.name == 'posix':
            from commands import getstatusoutput
            if getstatusoutput('uname') == (0, 'Linux'):
                env.set_cachesize(0, 0x4000000, 1)

        env.open(dbHome, (DB_CREATE | DB_THREAD |
                          DB_INIT_MPOOL | DB_INIT_LOCK | DB_INIT_TXN), 0)

        index = DB(env)
        blocks = DB(env)
        txn = None
        
        try:
            txn = env.txn_begin(None)
            index.open(filename = '__index__', dbtype = DB_BTREE,
                       flags = DB_CREATE | DB_THREAD, txn = txn)
            blocks.open(filename = '__blocks__', dbtype = DB_BTREE,
                        flags = DB_CREATE | DB_THREAD, txn = txn)
        except:
            if txn is not None:
                txn.abort()
                txn = None
            raise
        else:
            txn.commit()
            txn = None

        try:
            txn = env.txn_begin(None)
            directory = DbDirectory(txn, index, blocks, 0)
            writer = IndexWriter(directory, StandardAnalyzer(), create,
                                 IndexWriter.MaxFieldLength.UNLIMITED)
            writer.setUseCompoundFile(False)

            doc = Document()
            doc.add(Field("contents", "The quick brown fox...",
                          Field.Store.YES, Field.Index.ANALYZED))
            writer.addDocument(doc)

            writer.optimize()
            writer.close()
        except:
            if txn is not None:
                txn.abort()
                txn = None
            raise
        else:
            txn.commit()
            index.close()
            blocks.close()
            env.close()

        print "Indexing Complete"

    main = classmethod(main)
