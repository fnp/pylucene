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

#ifndef _Character_H
#define _Character_H

#include <Python.h>
#include "java/lang/Object.h"
#include "java/lang/Class.h"

namespace java {
    namespace lang {

        class Character : public Object {
        public:
            static Class *class$;
            static jmethodID *_mids;
            static jclass initializeClass();

            explicit Character(jobject obj) : Object(obj) {
                initializeClass();
            }
            Character(jchar);

            jchar charValue() const;
        };

        extern PyTypeObject PY_TYPE(Character);

        class t_Character {
        public:
            PyObject_HEAD
            Character object;
            static PyObject *wrap_Object(const Character& object);
            static PyObject *wrap_jobject(const jobject& object);
        };
    }
}

#endif /* _Character_H */
