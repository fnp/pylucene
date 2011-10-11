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

package org.apache.jcc;


public class PythonVM {
    static protected PythonVM vm;

    static {
        System.loadLibrary("jcc");
    }

    /**
     * Start the embedded Python interpreter.  The specified
     * program name and args are set into the Python variable sys.argv.
     * This returns an instance of the Python VM; it may be called
     * multiple times, and will return the same VM instance each time.
     *
     * @param programName the name of the Python program, typically
     * /usr/bin/python.  This is informational; the program is not
     * actually executed.
     * @param args additional arguments to be put into sys.argv.
     * @return a singleton instance of PythonVM
     */
    static public PythonVM start(String programName, String[] args)
    {
        if (vm == null)
        {
            vm = new PythonVM();
            vm.init(programName, args);
        }

        return vm;
    }

    /**
     * Start the embedded Python interpreter.  The specified
     * program name is set into the Python variable sys.argv[0].
     * This returns an instance of the Python VM; it may be called
     * multiple times, and will return the same VM instance each time.
     *
     * @param programName the name of the Python program, typically
     * /usr/bin/python.  This is informational; the program is not
     * actually executed.
     * @return a singleton instance of PythonVM
     */
    static public PythonVM start(String programName)
    {
        return start(programName, null);
    }

    /**
     * Obtain the PythonVM instance, or null if the Python VM
     * has not yet been started.
     *
     * @return a singleton instance of PythonVM, or null
     */
    static public PythonVM get()
    {
        return vm;
    }

    protected PythonVM()
    {
    }

    protected native void init(String programName, String[] args);

    /**
     * Instantiate the specified Python class, and return the instance.
     *
     * @param moduleName the Python module the class is defined in
     * @param className the Python class to instantiate.
     * @return a handle on the Python instance.
     */
    public native Object instantiate(String moduleName, String className)
        throws PythonException;

    /**
     * Bump the Python thread state counter.  Every thread should
     * do this before calling into Python, to prevent the Python
     * thread state from being inadvertently collected (and causing loss
     * of thread-local variables)
     *
     * @return the Python thread state counter.  A return value less
     * than zero signals an error.
     */
    public native int acquireThreadState();

    /**
     * Release the Python thread state counter.  Every thread that has
     * called acquireThreadState() should call this before
     * terminating.
     *
     * @return the Python thread state counter.  A return value less
     * than zero signals an error.
     */
    public native int releaseThreadState();
}
