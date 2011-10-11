#ifdef _java_generics

#include <jni.h>
#include "JCCEnv.h"
#include "java/lang/reflect/GenericDeclaration.h"
#include "java/lang/Class.h"
#include "java/lang/reflect/TypeVariable.h"
#include "JArray.h"

namespace java {
    namespace lang {
        namespace reflect {

            java::lang::Class *GenericDeclaration::class$ = NULL;
            jmethodID *GenericDeclaration::mids$ = NULL;

            jclass GenericDeclaration::initializeClass()
            {
                if (!class$)
                {

                    jclass cls = (jclass) env->findClass("java/lang/reflect/GenericDeclaration");

                    mids$ = new jmethodID[max_mid];
                    mids$[mid_getTypeParameters_837d3468] = env->getMethodID(cls, "getTypeParameters", "()[Ljava/lang/reflect/TypeVariable;");

                    class$ = (java::lang::Class *) new JObject(cls);
                }
                return (jclass) class$->this$;
            }

            JArray<java::lang::reflect::TypeVariable> GenericDeclaration::getTypeParameters() const
            {
                return JArray<java::lang::reflect::TypeVariable>(env->callObjectMethod(this$, mids$[mid_getTypeParameters_837d3468]));
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
            static PyObject *t_GenericDeclaration_cast_(PyTypeObject *type, PyObject *arg);
            static PyObject *t_GenericDeclaration_instance_(PyTypeObject *type, PyObject *arg);
            static PyObject *t_GenericDeclaration_getTypeParameters(t_GenericDeclaration *self);

            static PyMethodDef t_GenericDeclaration__methods_[] = {
                DECLARE_METHOD(t_GenericDeclaration, cast_, METH_O | METH_CLASS),
                DECLARE_METHOD(t_GenericDeclaration, instance_, METH_O | METH_CLASS),
                DECLARE_METHOD(t_GenericDeclaration, getTypeParameters, METH_NOARGS),
                { NULL, NULL, 0, NULL }
            };

            DECLARE_TYPE(GenericDeclaration, t_GenericDeclaration, java::lang::Object, GenericDeclaration, abstract_init, 0, 0, 0, 0, 0);

            static PyObject *t_GenericDeclaration_cast_(PyTypeObject *type, PyObject *arg)
            {
                if (!(arg = castCheck(arg, GenericDeclaration::initializeClass, 1)))
                    return NULL;
                return t_GenericDeclaration::wrap_Object(GenericDeclaration(((t_GenericDeclaration *) arg)->object.this$));
            }
            static PyObject *t_GenericDeclaration_instance_(PyTypeObject *type, PyObject *arg)
            {
                if (!castCheck(arg, GenericDeclaration::initializeClass, 0))
                    Py_RETURN_FALSE;
                Py_RETURN_TRUE;
            }

            static PyObject *t_GenericDeclaration_getTypeParameters(t_GenericDeclaration *self)
            {
                JArray<TypeVariable> result((jobject) NULL);
                OBJ_CALL(result = self->object.getTypeParameters());

                return result.toSequence(t_TypeVariable::wrap_Object);
            }
        }
    }
}

#endif /* _java_generics */
