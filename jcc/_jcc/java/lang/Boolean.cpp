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
#include "java/lang/Boolean.h"

namespace java {
    namespace lang {

        enum {
            mid__init_,
            mid_booleanValue,
            max_mid
        };

        Class *Boolean::class$ = NULL;
        jmethodID *Boolean::_mids = NULL;

        Boolean *Boolean::TRUE = NULL;
        Boolean *Boolean::FALSE = NULL;
        
        jclass Boolean::initializeClass()
        {
            if (!class$)
            {
                jclass cls = env->findClass("java/lang/Boolean");

                _mids = new jmethodID[max_mid];
                _mids[mid__init_] = env->getMethodID(cls, "<init>", "(Z)V");
                _mids[mid_booleanValue] =
                    env->getMethodID(cls, "booleanValue", "()Z");

                class$ = (Class *) new JObject(cls);

                FALSE = new Boolean(env->getStaticObjectField(cls, "FALSE", "Ljava/lang/Boolean;"));
                TRUE = new Boolean(env->getStaticObjectField(cls, "TRUE", "Ljava/lang/Boolean;"));
            }

            return (jclass) class$->this$;
        }

        Boolean::Boolean(jboolean b) : Object(env->newObject(initializeClass, &_mids, mid__init_, b)) {
        }

        int Boolean::booleanValue() const
        {
            return (int) env->callBooleanMethod(this$, _mids[mid_booleanValue]);
        }
    }
}


#include "structmember.h"
#include "functions.h"
#include "macros.h"

namespace java {
    namespace lang {

        static PyMethodDef t_Boolean__methods_[] = {
            { NULL, NULL, 0, NULL }
        };

        DECLARE_TYPE(Boolean, t_Boolean, Object, java::lang::Boolean,
                     abstract_init, 0, 0, 0, 0, 0);
    }
}
