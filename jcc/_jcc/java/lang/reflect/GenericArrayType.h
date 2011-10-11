#ifdef _java_generics

#ifndef java_lang_reflect_GenericArrayType_H
#define java_lang_reflect_GenericArrayType_H

#include "java/lang/reflect/Type.h"

namespace java {
    namespace lang {
        class Class;
    }
}
template<class T> class JArray;

namespace java {
    namespace lang {
        namespace reflect {

            class GenericArrayType : public java::lang::reflect::Type {
            public:
                enum {
                    mid_getGenericComponentType_86037cf0,
                    max_mid
                };

                static java::lang::Class *class$;
                static jmethodID *mids$;
                static jclass initializeClass();

                explicit GenericArrayType(jobject obj) : java::lang::reflect::Type(obj) {
                    if (obj != NULL)
                        initializeClass();
                }
                GenericArrayType(const GenericArrayType& obj) : java::lang::reflect::Type(obj) {}

                java::lang::reflect::Type getGenericComponentType() const;
            };
        }
    }
}

#include <Python.h>

namespace java {
    namespace lang {
        namespace reflect {
            extern PyTypeObject PY_TYPE(GenericArrayType);

            class t_GenericArrayType {
            public:
                PyObject_HEAD
                GenericArrayType object;
                static PyObject *wrap_Object(const GenericArrayType&);
                static PyObject *wrap_jobject(const jobject&);
            };
        }
    }
}

#endif

#endif /* _java_generics */
