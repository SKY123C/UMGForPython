#pragma once
#include "CoreMinimal.h"
#include "EditorUtilityWidget.h"
#include "Components/Button.h"
#include "Blueprint/UserWidget.h"
#include "Components/Widget.h"
#include "UMG.h"
#include "InputCoreTypes.h"
#include "Input/Events.h"
#include "UMGExtendWidgets.generated.h"

UCLASS()
class UPythonExpandableArea : public UExpandableArea
{
	GENERATED_BODY()
public:
	UFUNCTION(BlueprintCallable, Category = "Expansion")
	void SetExpandableAreaBody(UWidget* InWidget) { BodyContent = InWidget; };

	UFUNCTION(BlueprintCallable, Category = "Expansion")
	void SetExpandableAreaHead(UWidget* InWidget) { HeaderContent = InWidget; };
};

UCLASS()
class UMYTest : public UObject
{
	GENERATED_BODY()
public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	TObjectPtr<UObject> Ptr;
};