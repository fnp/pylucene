#ifdef _java_generics

#include <jni.h>
#include "JCCEnv.h"
#include "java/lang/reflect/GenericArrayType.h"
#include "java/lang/Class.h"
#include "JArray.h"

namespace java {
    namespace lang {
        namespace reflect {

            java::lang::Class *GenericArrayType::class$ = NULL;
            jmethodID *GenericArrayType::mids$ = NULL;

            jclass GenericArrayType::initializeClass()
            {
                if (!class$)
                {

                    jclass cls = (jclass) env->findClass("java/lang/reflect/GenericArrayType");

                    mids$ = new jmethodID[max_mid];
                    mids$[mid_getGenericComponentType_86037cf0] = env->getMethodID(cls, "getGenericComponentType", "()Ljava/lang/reflect/Type;");

                    class$ = (java::lang::Class *) new JObject(cls);
                }
                return (jclass) class$->this$;
            }

            java::lang::reflect::Type GenericArrayType::getGenericComponentType() const
            {
                return java::lang::reflect::Type(env->callObjectMethod(this$, mids$[mid_getGenericComponentType_86037cf0]));
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
            static PyObject *t_GenericArrayType_cast_(PyTypeObject *type, PyObject *arg);
            static PyObject *t_GenericArrayType_instance_(PyTypeObject *type, PyObject *arg);
            static PyObject *t_GenericArrayType_getGenericComponentType(t_GenericArrayType *self);

            static PyMethodDef t_GenericArrayType__methods_[] = {
                DECLARE_METHOD(t_GenericArrayType, cast_, METH_O | METH_CLASS),
                DECLARE_METHOD(t_GenericArrayType, instance_, METH_O | METH_CLASS),
                DECLARE_METHOD(t_GenericArrayType, getGenericComponentType, METH_NOARGS),
                { NULL, NULL, 0, NULL }
            };

            DECLARE_TYPE(GenericArrayType, t_GenericArrayType, java::lang::reflect::Type, GenericArrayType, abstract_init, 0, 0, 0, 0, 0);

            static PyObject *t_GenericArrayType_cast_(PyTypeObject *type, PyObject *arg)
            {
                if (!(arg = castCheck(arg, GenericArrayType::initializeClass, 1)))
                    return NULL;
                return t_GenericArrayType::wrap_Object(GenericArrayType(((t_GenericArrayType *) arg)->object.this$));
            }
            static PyObject *t_GenericArrayType_instance_(PyTypeObject *type, PyObject *arg)
            {
                if (!castCheck(arg, GenericArrayType::initializeClass, 0))
                    Py_RETURN_FALSE;
                Py_RETURN_TRUE;
            }

            static PyObject *t_GenericArrayType_getGenericComponentType(t_GenericArrayType *self)
            {
                java::lang::reflect::Type result((jobject) NULL);
                OBJ_CALL(result = self->object.getGenericComponentType());
                return java::lang::reflect::t_Type::wrap_Object(result);
            }
        }
    }
}

#endif /* _java_generics */
