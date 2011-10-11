#ifdef _java_generics

#ifndef java_lang_reflect_WildcardType_H
#define java_lang_reflect_WildcardType_H

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

            class WildcardType : public java::lang::reflect::Type {
            public:
                enum {
                    mid_getLowerBounds_6f565a00,
                    mid_getUpperBounds_6f565a00,
                    max_mid
                };

                static java::lang::Class *class$;
                static jmethodID *mids$;
                static jclass initializeClass();

                explicit WildcardType(jobject obj) : java::lang::reflect::Type(obj) {
                    if (obj != NULL)
                        initializeClass();
                }
                WildcardType(const WildcardType& obj) : java::lang::reflect::Type(obj) {}

                JArray<java::lang::reflect::Type> getLowerBounds() const;
                JArray<java::lang::reflect::Type> getUpperBounds() const;
            };
        }
    }
}

#include <Python.h>

namespace java {
    namespace lang {
        namespace reflect {
            extern PyTypeObject PY_TYPE(WildcardType);

            class t_WildcardType {
            public:
                PyObject_HEAD
                WildcardType object;
                static PyObject *wrap_Object(const WildcardType&);
                static PyObject *wrap_jobject(const jobject&);
            };
        }
    }
}

#endif
#endif /* _java_generics */
