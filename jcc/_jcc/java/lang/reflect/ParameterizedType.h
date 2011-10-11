#ifdef _java_generics

#ifndef java_lang_reflect_ParameterizedType_H
#define java_lang_reflect_ParameterizedType_H

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

            class ParameterizedType : public java::lang::reflect::Type {
            public:
                enum {
                    mid_getActualTypeArguments_6f565a00,
                    mid_getOwnerType_86037cf0,
                    mid_getRawType_86037cf0,
                    max_mid
                };

                static java::lang::Class *class$;
                static jmethodID *mids$;
                static jclass initializeClass();

                explicit ParameterizedType(jobject obj) : java::lang::reflect::Type(obj) {
                    if (obj != NULL)
                        initializeClass();
                }
                ParameterizedType(const ParameterizedType& obj) : java::lang::reflect::Type(obj) {}

                JArray<java::lang::reflect::Type> getActualTypeArguments() const;
                java::lang::reflect::Type getOwnerType() const;
                java::lang::reflect::Type getRawType() const;
            };
        }
    }
}

#include <Python.h>

namespace java {
    namespace lang {
        namespace reflect {
            extern PyTypeObject PY_TYPE(ParameterizedType);

            class t_ParameterizedType {
            public:
                PyObject_HEAD
                ParameterizedType object;
                static PyObject *wrap_Object(const ParameterizedType&);
                static PyObject *wrap_jobject(const jobject&);
            };
        }
    }
}

#endif

#endif /* _java_generics */
