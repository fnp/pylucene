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

package org.apache.pylucene.store;

import java.io.IOException;
import org.apache.lucene.store.BufferedIndexOutput;


public class PythonIndexOutput extends BufferedIndexOutput {

    private long pythonObject;

    public PythonIndexOutput()
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

    public void seek(long pos)
        throws IOException
    {
        super.seek(pos);
        seekInternal(pos);
    }

    public native void pythonDecRef();
    public native long length()
        throws IOException;
    public native void flushBuffer(byte[] data)
        throws IOException;
    public native void seekInternal(long pos)
        throws IOException;
    public native void close()
        throws IOException;

    protected void flushBuffer(byte[] b, int offset, int len)
        throws IOException
    {
        byte[] data = new byte[len];
        System.arraycopy(b, offset, data, 0, len);
        flushBuffer(data);
    }
}
