/*
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
 */

#include <Python.h>
#include "macros.h"

namespace java {
    namespace lang {

        extern PyTypeObject PY_TYPE(Object);
        extern PyTypeObject PY_TYPE(String);
        extern PyTypeObject PY_TYPE(Class);
        extern PyTypeObject PY_TYPE(Throwable);
        extern PyTypeObject PY_TYPE(Exception);
        extern PyTypeObject PY_TYPE(RuntimeException);
        extern PyTypeObject PY_TYPE(Boolean);
        extern PyTypeObject PY_TYPE(Byte);
        extern PyTypeObject PY_TYPE(Character);
        extern PyTypeObject PY_TYPE(Integer);
        extern PyTypeObject PY_TYPE(Double);
        extern PyTypeObject PY_TYPE(Float);
        extern PyTypeObject PY_TYPE(Long);
        extern PyTypeObject PY_TYPE(Short);
        
        namespace reflect {
            void __install__(PyObject *module);
        }

        void __install__(PyObject *m)
        {
            INSTALL_TYPE(Object, m);
            INSTALL_TYPE(String, m);
            INSTALL_TYPE(Class, m);
            INSTALL_TYPE(Throwable, m);
            INSTALL_TYPE(Exception, m);
            INSTALL_TYPE(RuntimeException, m);
            INSTALL_TYPE(Boolean, m);
            INSTALL_TYPE(Byte, m);
            INSTALL_TYPE(Character, m);
            INSTALL_TYPE(Double, m);
            INSTALL_TYPE(Float, m);
            INSTALL_TYPE(Integer, m);
            INSTALL_TYPE(Long, m);
            INSTALL_TYPE(Short, m);
            reflect::__install__(m);
        }
    }
}
