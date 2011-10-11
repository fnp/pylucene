#ifdef _java_generics

#ifndef java_lang_reflect_Type_H
#define java_lang_reflect_Type_H

#include "java/lang/Object.h"

namespace java {
    namespace lang {
        class Class;
    }
}
template<class T> class JArray;

namespace java {
    namespace lang {
        namespace reflect {

            class Type : public java::lang::Object {
            public:

                static java::lang::Class *class$;
                static jmethodID *mids$;
                static jclass initializeClass();

                explicit Type(jobject obj) : java::lang::Object(obj) {
                    if (obj != NULL)
                        initializeClass();
                }
                Type(const Type& obj) : java::lang::Object(obj) {}
            };
        }
    }
}

#include <Python.h>

namespace java {
    namespace lang {
        namespace reflect {
            extern PyTypeObject PY_TYPE(Type);

            class t_Type {
            public:
                PyObject_HEAD
                Type object;
                static PyObject *wrap_Object(const Type&);
                static PyObject *wrap_jobject(const jobject&);
            };
        }
    }
}

#endif
#endif /* _java_generics */
