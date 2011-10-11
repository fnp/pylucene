/* ====================================================================
 *   Licensed under the Apache License, Version 2.0 (the "License");
 *   you may not use this file except in compliance with the License.
 *   You may obtain a copy of the License at
 *
 *       http://www.apache.org/licenses/LICENSE-2.0
 *
 *   Unless required by applicable law or agreed to in writing, software
 *   distributed under the License is distributed on an "AS IS" BASIS,
 *   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *   See the License for the specific language governing permissions and
 *   limitations under the License.
 * ====================================================================
 */

package org.apache.pylucene.search;

import java.io.IOException;
import org.apache.lucene.search.FieldComparator;
import org.apache.lucene.index.IndexReader;

/**
 * @author Andi Vajda
 */

public class PythonFieldComparator<T> extends FieldComparator<T> {

    private long pythonObject;

    public PythonFieldComparator()
    {
    }

    public void pythonExtension(long pythonObject)
    {
        this.pythonObject = pythonObject;
    }
    public long pythonExtension()
    {
        return this.pythonObject;
    }

    public void finalize()
        throws Throwable
    {
        pythonDecRef();
    }

    public native void pythonDecRef();

    public native int compare(int slot1, int slot2);
    public native void setBottom(final int slot);
    public native int compareBottom(int doc)
        throws IOException;
    public native void copy(int slot, int doc) 
        throws IOException;
    public native void setNextReader(IndexReader reader, int docBase)
        throws IOException;
    public native T value(int slot);
}
