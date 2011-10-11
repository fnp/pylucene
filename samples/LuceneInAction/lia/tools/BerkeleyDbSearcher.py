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
     DB_INIT_MPOOL, DB_INIT_LOCK, DB_INIT_TXN, DB_THREAD, DB_BTREE

# missing from python interface at the moment
DB_LOG_INMEMORY = 0x00020000

from lucene import DbDirectory, IndexSearcher, Term, TermQuery


class BerkeleyDbSearcher(object):

    def main(cls, argv):

        if len(argv) != 2:
            print "Usage: BerkeleyDbSearcher <index dir>"
            return

        dbHome = argv[1]

        env = DBEnv()
        env.set_flags(DB_LOG_INMEMORY, 1);
        if os.name == 'nt':
            env.set_cachesize(0, 0x4000000, 1)
        elif os.name == 'posix':
            from commands import getstatusoutput
            if getstatusoutput('uname') == (0, 'Linux'):
                env.set_cachesize(0, 0x4000000, 1)

        env.open(dbHome, (DB_THREAD |
                          DB_INIT_MPOOL | DB_INIT_LOCK | DB_INIT_TXN), 0)

        index = DB(env)
        blocks = DB(env)
        txn = None

        try:
            txn = env.txn_begin(None)
            index.open(filename = '__index__', dbtype = DB_BTREE,
                       flags = DB_THREAD, txn = txn)
            blocks.open(filename = '__blocks__', dbtype = DB_BTREE,
                        flags = DB_THREAD, txn = txn)
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
            searcher = IndexSearcher(directory, True)

            topDocs = searcher.search(TermQuery(Term("contents", "fox")), 50)
            print topDocs.totalHits, "document(s) found"
            searcher.close()
        except:
            if txn is not None:
                txn.abort()
                txn = None
            raise
        else:
            txn.abort()

            index.close()
            blocks.close()
            env.close()

    main = classmethod(main)
