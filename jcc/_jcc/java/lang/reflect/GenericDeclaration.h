#ifdef _java_generics

#ifndef java_lang_reflect_GenericDeclaration_H
#define java_lang_reflect_GenericDeclaration_H

#include "java/lang/Object.h"

namespace java {
    namespace lang {
        namespace reflect {
            class TypeVariable;
        }
        class Class;
    }
}
template<class T> class JArray;

namespace java {
    namespace lang {
        namespace reflect {

            class GenericDeclaration : public java::lang::Object {
            public:
                enum {
                    mid_getTypeParameters_837d3468,
                    max_mid
                };

                static java::lang::Class *class$;
                static jmethodID *mids$;
                static jclass initializeClass();

                explicit GenericDeclaration(jobject obj) : java::lang::Object(obj) {
                    if (obj != NULL)
                        initializeClass();
                }
                GenericDeclaration(const GenericDeclaration& obj) : java::lang::Object(obj) {}

                JArray<java::lang::reflect::TypeVariable> getTypeParameters() const;
            };
        }
    }
}

#include <Python.h>

namespace java {
    namespace lang {
        namespace reflect {
            extern PyTypeObject PY_TYPE(GenericDeclaration);

            class t_GenericDeclaration {
            public:
                PyObject_HEAD
                GenericDeclaration object;
                static PyObject *wrap_Object(const GenericDeclaration&);
                static PyObject *wrap_jobject(const jobject&);
            };
        }
    }
}

#endif

#endif /* _java_generics */
