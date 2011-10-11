#ifdef _java_generics

#ifndef java_lang_reflect_TypeVariable_H
#define java_lang_reflect_TypeVariable_H

#include "java/lang/reflect/Type.h"

namespace java {
    namespace lang {
        namespace reflect {
            class GenericDeclaration;
        }
        class Class;
        class String;
    }
}
template<class T> class JArray;

namespace java {
    namespace lang {
        namespace reflect {

            class TypeVariable : public java::lang::reflect::Type {
            public:
                enum {
                    mid_getBounds_6f565a00,
                    mid_getGenericDeclaration_2dc62edd,
                    mid_getName_14c7b5c5,
                    max_mid
                };

                static java::lang::Class *class$;
                static jmethodID *mids$;
                static jclass initializeClass();

                explicit TypeVariable(jobject obj) : java::lang::reflect::Type(obj) {
                    if (obj != NULL)
                        initializeClass();
                }
                TypeVariable(const TypeVariable& obj) : java::lang::reflect::Type(obj) {}

                JArray<java::lang::reflect::Type> getBounds() const;
                java::lang::reflect::GenericDeclaration getGenericDeclaration() const;
                java::lang::String getName() const;
            };
        }
    }
}

#include <Python.h>

namespace java {
    namespace lang {
        namespace reflect {
            extern PyTypeObject PY_TYPE(TypeVariable);

            class t_TypeVariable {
            public:
                PyObject_HEAD
                TypeVariable object;
                static PyObject *wrap_Object(const TypeVariable&);
                static PyObject *wrap_jobject(const jobject&);
            };
        }
    }
}

#endif

#endif /* _java_generics */
