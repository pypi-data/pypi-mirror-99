#ifndef CPYCPPYY_CPPCONSTRUCTOR_H
#define CPYCPPYY_CPPCONSTRUCTOR_H

// Bindings
#include "CPPMethod.h"


namespace CPyCppyy {

class CPPConstructor : public CPPMethod {
public:
    using CPPMethod::CPPMethod;

public:
    virtual PyObject* GetDocString();
    virtual PyCallable* Clone() { return new CPPConstructor(*this); }

public:
    virtual PyObject* Call(
        CPPInstance*& self, PyObject* args, PyObject* kwds, CallContext* ctxt = nullptr);

protected:
    virtual bool InitExecutor_(Executor*&, CallContext* ctxt = nullptr);
};


// specialization for multiple inheritance disambiguation
class CPPMultiConstructor : public CPPConstructor {
public:
    CPPMultiConstructor(Cppyy::TCppScope_t scope, Cppyy::TCppMethod_t method);
    CPPMultiConstructor(const CPPMultiConstructor&);
    CPPMultiConstructor& operator=(const CPPMultiConstructor&);

public:
    virtual PyObject* Call(CPPInstance*&, PyObject*, PyObject*, CallContext* = nullptr);

private:
    Py_ssize_t fNumBases;
};


// specializations of prohibiting constructors
class CPPAbstractClassConstructor : public CPPConstructor {
public:
    using CPPConstructor::CPPConstructor;

public:
    virtual PyObject* Call(CPPInstance*&, PyObject*, PyObject*, CallContext* = nullptr);
};

class CPPNamespaceConstructor : public CPPConstructor {
public:
    using CPPConstructor::CPPConstructor;

public:
    virtual PyObject* Call(CPPInstance*&, PyObject*, PyObject*, CallContext* = nullptr);
};

class CPPIncompleteClassConstructor : public CPPConstructor {
public:
    using CPPConstructor::CPPConstructor;

public:
    virtual PyObject* Call(CPPInstance*&, PyObject*, PyObject*, CallContext* = nullptr);
};

} // namespace CPyCppyy

#endif // !CPYCPPYY_CPPCONSTRUCTOR_H
