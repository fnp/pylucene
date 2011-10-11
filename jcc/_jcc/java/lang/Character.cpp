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

#include <jni.h>
#include "JCCEnv.h"
#include "java/lang/Object.h"
#include "java/lang/Class.h"
#include "java/lang/Character.h"

namespace java {
    namespace lang {

        enum {
            mid__init_,
            mid_charValue,
            max_mid
        };

        Class *Character::class$ = NULL;
        jmethodID *Character::_mids = NULL;

        jclass Character::initializeClass()
        {
            if (!class$)
            {
                jclass cls = env->findClass("java/lang/Character");

                _mids = new jmethodID[max_mid];
                _mids[mid__init_] = env->getMethodID(cls, "<init>", "(C)V");
                _mids[mid_charValue] =
                    env->getMethodID(cls, "charValue", "()C");

                class$ = (Class *) new JObject(cls);
            }

            return (jclass) class$->this$;
        }

        Character::Character(jchar c) : Object(env->newObject(initializeClass, &_mids, mid__init_, c)) {
        }

        jchar Character::charValue() const
        {
            return env->callCharMethod(this$, _mids[mid_charValue]);
        }
    }
}


#include "structmember.h"
#include "functions.h"
#include "macros.h"

namespace java {
    namespace lang {

        static PyMethodDef t_Character__methods_[] = {
            { NULL, NULL, 0, NULL }
        };

        DECLARE_TYPE(Character, t_Character, Object, java::lang::Character,
                     abstract_init, 0, 0, 0, 0, 0);
    }
}
