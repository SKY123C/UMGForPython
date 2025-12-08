// Copyright Epic Games, Inc. All Rights Reserved.
#include "UMGForPython.h"
#include "Async/Async.h"
#include "pystate.h"
#include "Interfaces/IPluginManager.h"
#include "Styling/SlateStyleRegistry.h"
#include "Modules/ModuleManager.h"
#include "PyWrapperObject.h"
#include "PyPtr.h"
#include "PyWrapperTypeRegistry.h"
#include <Windows.h>
#define LOCTEXT_NAMESPACE "FUMGForPythonModule"

void CustomFunc(UObject* self, FPropertyChangedEvent& PropertyChangedEvent)
{
    UE_LOG(LogTemp, Display, TEXT("PrintVirtual Called on %s"), *self->GetName());
    UE_LOG(LogTemp, Display, TEXT("Property Name %s"), *PropertyChangedEvent.GetPropertyName().ToString());
    FUMGForPythonModule& Module = FModuleManager::Get().LoadModuleChecked<FUMGForPythonModule>("UMGForPython");
    TArray<void*> Array = Module.GetOriginalFunction(self);
	FUNC OriginalFunc = (FUNC)Array[0];
	PyObject* Args = (PyObject*)Array[1];
    char* PropertyName = TCHAR_TO_ANSI(*PropertyChangedEvent.GetPropertyName().ToString());
    if (OriginalFunc)
        OriginalFunc(self, PropertyChangedEvent);
	if (Args)
    {
		
        PyObject* PyPropertyName = PyUnicode_FromString(PropertyName);
        PyGILState_STATE State = PyGILState_Ensure();
        PyObject* HookMethod = PyTuple_GET_ITEM(Args, 1);
        PyObject* OutArgs = PyTuple_New(2);
        PyTuple_SetItem(OutArgs, 0, PyTuple_GET_ITEM(Args, 0));
        PyTuple_SetItem(OutArgs, 1, PyPropertyName);
        PyObject_Call(HookMethod, OutArgs, nullptr);
        PyGILState_Release(State);
	}
}

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
        FEvent* DoneEvent = FPlatformProcess::GetSynchEventFromPool();
        Py_BEGIN_ALLOW_THREADS
            auto Ticker = FTSTicker::GetCoreTicker().AddTicker(FTickerDelegate::CreateLambda([=, &Result](float DeltaTime) -> bool
        {
            if (!FUObjectThreadContext::Get().IsRoutingPostLoad)
            {
                PyGILState_STATE State = PyGILState_Ensure();
                Result = CallFunc(InArgs, InKwargs);
                PyGILState_Release(State);
                DoneEvent->Trigger();
                return false;
            }
            return true;
        }), 1);
        DoneEvent->Wait();
        FTSTicker::GetCoreTicker().RemoveTicker(Ticker);
        FPlatformProcess::ReturnSynchEventToPool(DoneEvent);
        Py_END_ALLOW_THREADS
    }
    else
    {
        Result = CallFunc(InArgs, InKwargs);
    }
    return Result;
}

static PyObject* AddPropertyEventHook(PyObject* ModuleSelf, PyObject* InArgs, PyObject* InKwargs)
{
    PyObject* PyObj = PyTuple_GET_ITEM(InArgs, 0);
    FPyWrapperObject* PyWrappedObj = (FPyWrapperObject*)PyObj;
    FUMGForPythonModule& Module = FModuleManager::Get().LoadModuleChecked<FUMGForPythonModule>("UMGForPython");
    Py_NewRef(InArgs);
	Module.AddPropertyEventHook(PyWrappedObj->ObjectInstance, InArgs);
    return Py_None;
}
PyMethodDef PyhonExtendsion[] = {
    { "executeInMainThreadWithResult", (PyCFunction)(void*)(&ExecuteInMainThreadWithResult), METH_VARARGS | METH_KEYWORDS, ""},
    { "add_property_event_hook", (PyCFunction)(void*)(&AddPropertyEventHook), METH_VARARGS | METH_KEYWORDS, ""},
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

void FUMGForPythonModule::AddPropertyEventHook(UObject* InObject, PyObject* InPyObject)
{
    RemovePropertyEventHook(InObject);
    auto* vptr = *(void***)InObject;
    FUNC OriginalFunc = (FUNC)vptr[39];
    ReplaceFunc(InObject, (void*)&CustomFunc);
    TArray<void*> Array;
    Array.Reset();
	Array.Add(OriginalFunc);
	Array.Add(InPyObject);
	TWeakObjectPtr WeakPtr(InObject);
    TMap<TWeakObjectPtr<UObject>, TArray<void*>> SaveMap;
    SaveMap.Add(WeakPtr, Array);
    PointerMapArray.Add(SaveMap);
}

void FUMGForPythonModule::RemovePropertyEventHook(UObject* InObject)
{
    for (int32 i = PointerMapArray.Num() - 1; i >= 0; --i)
    {
        TMap<TWeakObjectPtr<UObject>, TArray<void*>>& Map = PointerMapArray[i];
        for (auto It = Map.CreateConstIterator(); It; ++It)
        {

            PyObject* PyObjectPtr = (PyObject*)It->Value[1];
            if (!It->Key.IsValid())
            {
                Py_DECREF(PyObjectPtr);
                PointerMapArray.RemoveAt(i);
            }
            else
            {
                if (It->Key.Pin().Get() == InObject)
                {
                    ReplaceFunc(InObject, It->Value[0]);
                    Py_DECREF(PyObjectPtr);
                    PointerMapArray.RemoveAt(i);
                }
            }
        }
    }
}

TArray<void*> FUMGForPythonModule::GetOriginalFunction(UObject* InObject)
{
    for(auto& map : PointerMapArray)
    {
        for (auto& Item : map)
        {
            if (Item.Key.IsValid() && Item.Key.Pin().Get() == InObject)
               {
                FUNC func = FUNC(Item.Value[0]);
                return Item.Value;
			}
        }
	}
    return TArray<void*>();
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

void FUMGForPythonModule::ReplaceFunc(UObject* InObject, void* Ptr)
{
    auto* vptr = *(void***)InObject;
    DWORD old;
    FUNC OriginalFunc = (FUNC)vptr[39];
    VirtualProtect(&vptr[39], sizeof(void*), PAGE_EXECUTE_READWRITE, &old);
    vptr[39] = Ptr;
    VirtualProtect(&vptr[39], sizeof(void*), old, &old);
}

#undef LOCTEXT_NAMESPACE

IMPLEMENT_MODULE(FUMGForPythonModule, UMGForPython)

