// Copyright Epic Games, Inc. All Rights Reserved.
#include "UMGForPython.h"
#include "Python.h"
#include "Async/Async.h"
#include "pystate.h"
#define LOCTEXT_NAMESPACE "FUMGForPythonModule"

static PyObject* CallFunc(PyObject* InArgs, PyObject* InKwargs)
{
    PyObject* Result = Py_None;
    PyObject* Callable = Py_None;
    PyObject* Args = nullptr;
    Callable = PyTuple_GET_ITEM(InArgs, 0);
    if (PyTuple_Size(InArgs) > 1)
    {
        Args = PyTuple_GetSlice(InArgs, 1, PyTuple_Size(InArgs));
    }
    if (Args)
    {
        Result = PyObject_Call(Callable, Args, InKwargs);

    }
    else
    {
        Result = PyObject_Call(Callable, PyTuple_New(0), InKwargs);
    }
    return Result;
}

static PyObject* ExecuteInMainThreadWithResult(PyObject* ModuleSelf, PyObject* InArgs, PyObject* InKwargs) //PyObject* Args, PyObject* Keywds)
{
    PyObject* Result = Py_None;
    Py_XINCREF(InArgs);
    if (!IsInGameThread())
    {
        Py_BEGIN_ALLOW_THREADS
            FGraphEventRef Task = FFunctionGraphTask::CreateAndDispatchWhenReady([=, &Result]()
                {
                    //PyEval_InitThreads();
                    PyGILState_STATE State = PyGILState_Ensure();
                    Result = CallFunc(InArgs, InKwargs);
                    PyGILState_Release(State);

                }, TStatId(), NULL, ENamedThreads::GameThread);

        FTaskGraphInterface::Get().WaitUntilTaskCompletes(Task);
        Py_END_ALLOW_THREADS
    }
    else
    {
        Result = CallFunc(InArgs, InKwargs);
    }
    return Result;
}

PyMethodDef PyhonExtendsion[] = {
    { "executeInMainThreadWithResult", (PyCFunction)(void*)(&ExecuteInMainThreadWithResult), METH_VARARGS | METH_KEYWORDS, ""},
    { nullptr, nullptr, 0, nullptr }
};


void FUMGForPythonModule::StartupModule()
{
    PyGILState_STATE State = PyGILState_Ensure();
    PyObject* Modules = PyImport_GetModuleDict();
    PyObject* UnrealModule = PyDict_GetItemString(Modules, "unreal");
    if (UnrealModule)
    {
        PyModule_AddFunctions(UnrealModule, PyhonExtendsion);
    }
    PyGILState_Release(State);
}

void FUMGForPythonModule::ShutdownModule()
{
}

#undef LOCTEXT_NAMESPACE

IMPLEMENT_MODULE(FUMGForPythonModule, UMGForPython)