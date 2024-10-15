#pragma once
#include "CoreMinimal.h"
#include "UMG.h"
#include "EditorUtilityWidgetComponents.h"
#include "PythonExpandableArea.generated.h"

UCLASS()
class UPythonExpandableArea : public UEditorUtilityExpandableArea
{
	GENERATED_UCLASS_BODY()
public:
	UFUNCTION(BlueprintCallable, Category = "Expansion")
	void SetExpandableAreaBody(UWidget* InWidget) { BodyContent = InWidget; };

	UFUNCTION(BlueprintCallable, Category = "Expansion")
	void SetExpandableAreaHead(UWidget* InWidget) { HeaderContent = InWidget; };
};

