// Copyright Epic Games, Inc. All Rights Reserved.
#include "UMGForPython.h"
#include "Styling/SlateStyle.h"
#include "Styling/SlateStyleRegistry.h"

#define LOCTEXT_NAMESPACE "FUMGForPythonModule"


void FUMGForPythonModule::StartupModule()
{
	StyleSet = MakeShareable(new FSlateStyleSet("UMGForPythonStyleSet"));
	FString ProjectResourceDir = FPaths::ProjectPluginsDir() / TEXT("UMGForPython/Resources");
	if (IFileManager::Get().DirectoryExists(*ProjectResourceDir))
	{
		StyleSet->SetContentRoot(ProjectResourceDir);
		StyleSet->SetCoreContentRoot(ProjectResourceDir);

		StyleSet->Set("UMGForPython.Icon", new FSlateImageBrush(ProjectResourceDir / "toolbar.png", FVector2D(32.0f, 32.0f)));
	}
	FSlateStyleRegistry::RegisterSlateStyle(*StyleSet.Get());
}

void FUMGForPythonModule::ShutdownModule()
{
	if (StyleSet.IsValid())
	{
		FSlateStyleRegistry::UnRegisterSlateStyle(*StyleSet.Get());
		ensure(StyleSet.IsUnique());
		StyleSet.Reset();
	}
}

#undef LOCTEXT_NAMESPACE

IMPLEMENT_MODULE(FUMGForPythonModule, UMGForPython)