#ifdef _java_generics

#include <jni.h>
#include "JCCEnv.h"
#include "java/lang/reflect/ParameterizedType.h"
#include "java/lang/Class.h"
#include "JArray.h"

namespace java {
    namespace lang {
        namespace reflect {

            java::lang::Class *ParameterizedType::class$ = NULL;
            jmethodID *ParameterizedType::mids$ = NULL;

            jclass ParameterizedType::initializeClass()
            {
                if (!class$)
                {

                    jclass cls = (jclass) env->findClass("java/lang/reflect/ParameterizedType");

                    mids$ = new jmethodID[max_mid];
                    mids$[mid_getActualTypeArguments_6f565a00] = env->getMethodID(cls, "getActualTypeArguments", "()[Ljava/lang/reflect/Type;");
                    mids$[mid_getOwnerType_86037cf0] = env->getMethodID(cls, "getOwnerType", "()Ljava/lang/reflect/Type;");
                    mids$[mid_getRawType_86037cf0] = env->getMethodID(cls, "getRawType", "()Ljava/lang/reflect/Type;");

                    class$ = (java::lang::Class *) new JObject(cls);
                }
                return (jclass) class$->this$;
            }

            JArray<java::lang::reflect::Type> ParameterizedType::getActualTypeArguments() const
            {
                return JArray<java::lang::reflect::Type>(env->callObjectMethod(this$, mids$[mid_getActualTypeArguments_6f565a00]));
            }

            java::lang::reflect::Type ParameterizedType::getOwnerType() const
            {
                return java::lang::reflect::Type(env->callObjectMethod(this$, mids$[mid_getOwnerType_86037cf0]));
            }

            java::lang::reflect::Type ParameterizedType::getRawType() const
            {
                return java::lang::reflect::Type(env->callObjectMethod(this$, mids$[mid_getRawType_86037cf0]));
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
            static PyObject *t_ParameterizedType_cast_(PyTypeObject *type, PyObject *arg);
            static PyObject *t_ParameterizedType_instance_(PyTypeObject *type, PyObject *arg);
            static PyObject *t_ParameterizedType_getActualTypeArguments(t_ParameterizedType *self);
            static PyObject *t_ParameterizedType_getOwnerType(t_ParameterizedType *self);
            static PyObject *t_ParameterizedType_getRawType(t_ParameterizedType *self);

            static PyMethodDef t_ParameterizedType__methods_[] = {
                DECLARE_METHOD(t_ParameterizedType, cast_, METH_O | METH_CLASS),
                DECLARE_METHOD(t_ParameterizedType, instance_, METH_O | METH_CLASS),
                DECLARE_METHOD(t_ParameterizedType, getActualTypeArguments, METH_NOARGS),
                DECLARE_METHOD(t_ParameterizedType, getOwnerType, METH_NOARGS),
                DECLARE_METHOD(t_ParameterizedType, getRawType, METH_NOARGS),
                { NULL, NULL, 0, NULL }
            };

            DECLARE_TYPE(ParameterizedType, t_ParameterizedType, java::lang::reflect::Type, ParameterizedType, abstract_init, 0, 0, 0, 0, 0);

            static PyObject *t_ParameterizedType_cast_(PyTypeObject *type, PyObject *arg)
            {
                if (!(arg = castCheck(arg, ParameterizedType::initializeClass, 1)))
                    return NULL;
                return t_ParameterizedType::wrap_Object(ParameterizedType(((t_ParameterizedType *) arg)->object.this$));
            }
            static PyObject *t_ParameterizedType_instance_(PyTypeObject *type, PyObject *arg)
            {
                if (!castCheck(arg, ParameterizedType::initializeClass, 0))
                    Py_RETURN_FALSE;
                Py_RETURN_TRUE;
            }

            static PyObject *t_ParameterizedType_getActualTypeArguments(t_ParameterizedType *self)
            {
                JArray<java::lang::reflect::Type> result((jobject) NULL);
                OBJ_CALL(result = self->object.getActualTypeArguments());

                return result.toSequence(t_Type::wrap_Object);
            }

            static PyObject *t_ParameterizedType_getOwnerType(t_ParameterizedType *self)
            {
                java::lang::reflect::Type result((jobject) NULL);
                OBJ_CALL(result = self->object.getOwnerType());
                return java::lang::reflect::t_Type::wrap_Object(result);
            }

            static PyObject *t_ParameterizedType_getRawType(t_ParameterizedType *self)
            {
                java::lang::reflect::Type result((jobject) NULL);
                OBJ_CALL(result = self->object.getRawType());
                return java::lang::reflect::t_Type::wrap_Object(result);
            }
        }
    }
}

#endif /* _java_generics */
