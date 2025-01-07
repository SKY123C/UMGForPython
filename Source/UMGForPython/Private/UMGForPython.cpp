// Copyright Epic Games, Inc. All Rights Reserved.
#include "UMGForPython.h"
#include "Python.h"
#include "Async/Async.h"
#include "pystate.h"
#include "Interfaces/IPluginManager.h"
#include "Styling/SlateStyleRegistry.h"
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
    RegisterStyle();
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
    UnregisterStyle();
}

void FUMGForPythonModule::RegisterStyle()
{
#define IMAGE_BRUSH_SVG(RelativePath, ...) FSlateVectorImageBrush(StyleInstance->RootToContentDir(RelativePath, TEXT(".svg")), __VA_ARGS__)

    StyleInstance = MakeUnique<FSlateStyleSet>("UMGForPythonStyleSet");
    TSharedPtr<IPlugin> Plugin = IPluginManager::Get().FindPlugin(TEXT("UMGForPython"));
    if (Plugin.IsValid())
    {
        StyleInstance->SetContentRoot(FPaths::Combine(Plugin->GetBaseDir(), TEXT("Resources")));
    }
    const FVector2D Icon32x32(32.0f, 32.0f);

    StyleInstance->Set("UMGForPython.Icon", new IMAGE_BRUSH_SVG("toolbar", Icon32x32));
    FSlateStyleRegistry::RegisterSlateStyle(*StyleInstance.Get());


#undef IMAGE_BRUSH
}

void FUMGForPythonModule::UnregisterStyle()
{
    FSlateStyleRegistry::UnRegisterSlateStyle(*StyleInstance.Get());
    StyleInstance.Reset();
}

#undef LOCTEXT_NAMESPACE

IMPLEMENT_MODULE(FUMGForPythonModule, UMGForPython)