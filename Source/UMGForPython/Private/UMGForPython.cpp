// Copyright Epic Games, Inc. All Rights Reserved.
#include "UMGForPython.h"
#include "Python.h"
#include "Async/Async.h"
#include "pystate.h"

#define LOCTEXT_NAMESPACE "FUMGForPythonModule"


void FUMGForPythonModule::StartupModule()
{

}

void FUMGForPythonModule::ShutdownModule()
{
}

#undef LOCTEXT_NAMESPACE

IMPLEMENT_MODULE(FUMGForPythonModule, UMGForPython)