// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "Modules/ModuleManager.h"
#include <Windows.h>
#include "Python.h"

using FUNC = void(*)(UObject*, FPropertyChangedEvent&);

class FUMGForPythonModule : public IModuleInterface
{
public:

	/** IModuleInterface implementation */
	virtual void StartupModule() override;
	virtual void ShutdownModule() override;

public:
    void AddPropertyEventHook(UObject* InObject, PyObject* InPyObject);
	void RemovePropertyEventHook(UObject* InObject);
	TArray<void*> GetOriginalFunction(UObject* InObject);
private:
	void RegisterStyle();
	void UnregisterStyle();
	TUniquePtr<FSlateStyleSet> StyleInstance;
	TArray<TMap<TWeakObjectPtr<UObject>, TArray<void*>>> PointerMapArray;
	void ReplaceFunc(UObject* InObject, void* Ptr);
};