#pragma once
#include "CoreMinimal.h"
#include "EditorSubsystem.h"
#include "UObject/UObjectGlobals.h"
#include "EditorDelegateSubsystem.generated.h"


UCLASS()
class UEditorDelegateSubsystem : public UEditorSubsystem
{
	GENERATED_BODY()

public:
	/** Callback for object property modifications, called by UObject::PostEditChangeProperty with a single property event */
	DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnObjectPropertyChanged, UObject*, InObject, FString, PropertyName);
	DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnCreatedFolder, FString, CreatePathString);
public:

	UPROPERTY(BlueprintReadWrite, EditAnywhere)
	FOnObjectPropertyChanged OnObjectPropertyChanged;

	UPROPERTY(BlueprintReadWrite, EditAnywhere)
	FOnCreatedFolder OnCreateFloder;
public:
	UEditorDelegateSubsystem();
	void OnCreateNewFolder(const FString& InPath);
};

