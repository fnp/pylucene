#ifdef _java_generics

#include <jni.h>
#include "JCCEnv.h"
#include "java/lang/reflect/TypeVariable.h"
#include "java/lang/reflect/GenericDeclaration.h"
#include "java/lang/Class.h"
#include "java/lang/String.h"
#include "JArray.h"

namespace java {
    namespace lang {
        namespace reflect {

            java::lang::Class *TypeVariable::class$ = NULL;
            jmethodID *TypeVariable::mids$ = NULL;

            jclass TypeVariable::initializeClass()
            {
                if (!class$)
                {

                    jclass cls = (jclass) env->findClass("java/lang/reflect/TypeVariable");

                    mids$ = new jmethodID[max_mid];
                    mids$[mid_getBounds_6f565a00] = env->getMethodID(cls, "getBounds", "()[Ljava/lang/reflect/Type;");
                    mids$[mid_getGenericDeclaration_2dc62edd] = env->getMethodID(cls, "getGenericDeclaration", "()Ljava/lang/reflect/GenericDeclaration;");
                    mids$[mid_getName_14c7b5c5] = env->getMethodID(cls, "getName", "()Ljava/lang/String;");

                    class$ = (java::lang::Class *) new JObject(cls);
                }
                return (jclass) class$->this$;
            }

            JArray<java::lang::reflect::Type> TypeVariable::getBounds() const
            {
                return JArray<java::lang::reflect::Type>(env->callObjectMethod(this$, mids$[mid_getBounds_6f565a00]));
            }

            java::lang::reflect::GenericDeclaration TypeVariable::getGenericDeclaration() const
            {
                return java::lang::reflect::GenericDeclaration(env->callObjectMethod(this$, mids$[mid_getGenericDeclaration_2dc62edd]));
            }

            java::lang::String TypeVariable::getName() const
            {
                return java::lang::String(env->callObjectMethod(this$, mids$[mid_getName_14c7b5c5]));
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
            static PyObject *t_TypeVariable_cast_(PyTypeObject *type, PyObject *arg);
            static PyObject *t_TypeVariable_instance_(PyTypeObject *type, PyObject *arg);
            static PyObject *t_TypeVariable_getBounds(t_TypeVariable *self);
            static PyObject *t_TypeVariable_getGenericDeclaration(t_TypeVariable *self);
            static PyObject *t_TypeVariable_getName(t_TypeVariable *self);

            static PyMethodDef t_TypeVariable__methods_[] = {
                DECLARE_METHOD(t_TypeVariable, cast_, METH_O | METH_CLASS),
                DECLARE_METHOD(t_TypeVariable, instance_, METH_O | METH_CLASS),
                DECLARE_METHOD(t_TypeVariable, getBounds, METH_NOARGS),
                DECLARE_METHOD(t_TypeVariable, getGenericDeclaration, METH_NOARGS),
                DECLARE_METHOD(t_TypeVariable, getName, METH_NOARGS),
                { NULL, NULL, 0, NULL }
            };

            DECLARE_TYPE(TypeVariable, t_TypeVariable, java::lang::reflect::Type, TypeVariable, abstract_init, 0, 0, 0, 0, 0);

            static PyObject *t_TypeVariable_cast_(PyTypeObject *type, PyObject *arg)
            {
                if (!(arg = castCheck(arg, TypeVariable::initializeClass, 1)))
                    return NULL;
                return t_TypeVariable::wrap_Object(TypeVariable(((t_TypeVariable *) arg)->object.this$));
            }
            static PyObject *t_TypeVariable_instance_(PyTypeObject *type, PyObject *arg)
            {
                if (!castCheck(arg, TypeVariable::initializeClass, 0))
                    Py_RETURN_FALSE;
                Py_RETURN_TRUE;
            }

            static PyObject *t_TypeVariable_getBounds(t_TypeVariable *self)
            {
                JArray<java::lang::reflect::Type> result((jobject) NULL);
                OBJ_CALL(result = self->object.getBounds());

                return result.toSequence(t_Type::wrap_Object);
            }

            static PyObject *t_TypeVariable_getGenericDeclaration(t_TypeVariable *self)
            {
                java::lang::reflect::GenericDeclaration result((jobject) NULL);
                OBJ_CALL(result = self->object.getGenericDeclaration());
                return java::lang::reflect::t_GenericDeclaration::wrap_Object(result);
            }

            static PyObject *t_TypeVariable_getName(t_TypeVariable *self)
            {
                java::lang::String result((jobject) NULL);
                OBJ_CALL(result = self->object.getName());
                return j2p(result);
            }
        }
    }
}

#endif /* _java_generics */
