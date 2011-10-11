#ifdef _java_generics

#include <jni.h>
#include "JCCEnv.h"
#include "java/lang/reflect/Type.h"
#include "java/lang/Class.h"
#include "JArray.h"

namespace java {
    namespace lang {
        namespace reflect {

            java::lang::Class *Type::class$ = NULL;
            jmethodID *Type::mids$ = NULL;

            jclass Type::initializeClass()
            {
                if (!class$)
                {

                    jclass cls = (jclass) env->findClass("java/lang/reflect/Type");

                    class$ = (java::lang::Class *) new JObject(cls);
                }
                return (jclass) class$->this$;
            }
        }
    }
}

#include "structmember.h"
#include "functions.h"
#include "macros.h"

namespace java {
    namespace lang {
        namespace reflect {
            static PyObject *t_Type_cast_(PyTypeObject *type, PyObject *arg);
            static PyObject *t_Type_instance_(PyTypeObject *type, PyObject *arg);

            static PyMethodDef t_Type__methods_[] = {
                DECLARE_METHOD(t_Type, cast_, METH_O | METH_CLASS),
                DECLARE_METHOD(t_Type, instance_, METH_O | METH_CLASS),
                { NULL, NULL, 0, NULL }
            };

            DECLARE_TYPE(Type, t_Type, java::lang::Object, Type, abstract_init, 0, 0, 0, 0, 0);

            static PyObject *t_Type_cast_(PyTypeObject *type, PyObject *arg)
            {
                if (!(arg = castCheck(arg, Type::initializeClass, 1)))
                    return NULL;
                return t_Type::wrap_Object(Type(((t_Type *) arg)->object.this$));
            }
            static PyObject *t_Type_instance_(PyTypeObject *type, PyObject *arg)
            {
                if (!castCheck(arg, Type::initializeClass, 0))
                    Py_RETURN_FALSE;
                Py_RETURN_TRUE;
            }
        }
    }
}

#endif /* _java_generics */
