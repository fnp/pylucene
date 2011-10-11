#ifdef _java_generics

#include <jni.h>
#include "JCCEnv.h"
#include "java/lang/reflect/WildcardType.h"
#include "java/lang/Class.h"
#include "JArray.h"

namespace java {
    namespace lang {
        namespace reflect {

            java::lang::Class *WildcardType::class$ = NULL;
            jmethodID *WildcardType::mids$ = NULL;

            jclass WildcardType::initializeClass()
            {
                if (!class$)
                {

                    jclass cls = (jclass) env->findClass("java/lang/reflect/WildcardType");

                    mids$ = new jmethodID[max_mid];
                    mids$[mid_getLowerBounds_6f565a00] = env->getMethodID(cls, "getLowerBounds", "()[Ljava/lang/reflect/Type;");
                    mids$[mid_getUpperBounds_6f565a00] = env->getMethodID(cls, "getUpperBounds", "()[Ljava/lang/reflect/Type;");

                    class$ = (java::lang::Class *) new JObject(cls);
                }
                return (jclass) class$->this$;
            }

            JArray<java::lang::reflect::Type> WildcardType::getLowerBounds() const
            {
                return JArray<java::lang::reflect::Type>(env->callObjectMethod(this$, mids$[mid_getLowerBounds_6f565a00]));
            }

            JArray<java::lang::reflect::Type> WildcardType::getUpperBounds() const
            {
                return JArray<java::lang::reflect::Type>(env->callObjectMethod(this$, mids$[mid_getUpperBounds_6f565a00]));
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
            static PyObject *t_WildcardType_cast_(PyTypeObject *type, PyObject *arg);
            static PyObject *t_WildcardType_instance_(PyTypeObject *type, PyObject *arg);
            static PyObject *t_WildcardType_getLowerBounds(t_WildcardType *self);
            static PyObject *t_WildcardType_getUpperBounds(t_WildcardType *self);

            static PyMethodDef t_WildcardType__methods_[] = {
                DECLARE_METHOD(t_WildcardType, cast_, METH_O | METH_CLASS),
                DECLARE_METHOD(t_WildcardType, instance_, METH_O | METH_CLASS),
                DECLARE_METHOD(t_WildcardType, getLowerBounds, METH_NOARGS),
                DECLARE_METHOD(t_WildcardType, getUpperBounds, METH_NOARGS),
                { NULL, NULL, 0, NULL }
            };

            DECLARE_TYPE(WildcardType, t_WildcardType, java::lang::reflect::Type, WildcardType, abstract_init, 0, 0, 0, 0, 0);

            static PyObject *t_WildcardType_cast_(PyTypeObject *type, PyObject *arg)
            {
                if (!(arg = castCheck(arg, WildcardType::initializeClass, 1)))
                    return NULL;
                return t_WildcardType::wrap_Object(WildcardType(((t_WildcardType *) arg)->object.this$));
            }
            static PyObject *t_WildcardType_instance_(PyTypeObject *type, PyObject *arg)
            {
                if (!castCheck(arg, WildcardType::initializeClass, 0))
                    Py_RETURN_FALSE;
                Py_RETURN_TRUE;
            }

            static PyObject *t_WildcardType_getLowerBounds(t_WildcardType *self)
            {
                JArray<java::lang::reflect::Type> result((jobject) NULL);
                OBJ_CALL(result = self->object.getLowerBounds());

                return result.toSequence(java::lang::reflect::t_Type::wrap_Object);
            }

            static PyObject *t_WildcardType_getUpperBounds(t_WildcardType *self)
            {
                JArray<java::lang::reflect::Type> result((jobject) NULL);
                OBJ_CALL(result = self->object.getUpperBounds());

                return result.toSequence(java::lang::reflect::t_Type::wrap_Object);
            }
        }
    }
}

#endif /* _java_generics */
