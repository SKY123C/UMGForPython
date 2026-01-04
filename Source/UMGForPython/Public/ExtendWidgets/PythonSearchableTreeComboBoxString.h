#pragma once
#include "Widgets/Views/STreeView.h"
#include "Components/Widget.h"
#include "Serialization/JsonTypes.h"
#include "Serialization/JsonReader.h"
#include "Serialization/JsonSerializer.h"
#include "NativeWidgets/SSearchableTreeCombobox.h"
#include "PythonSearchableTreeComboBoxString.generated.h"


UCLASS()
class UPythonSearchableTreeComboBoxString : public UWidget
{
	GENERATED_UCLASS_BODY()
	DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnSelectionChangedEvent, FString, SelectedItem, ESelectInfo::Type, SelectionType);
	DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnOpeningEvent);
public:
	UFUNCTION(BlueprintCallable)
	void ParseTreeNodes(const FString& JsonStr);

	UFUNCTION(BlueprintCallable)
	FString GetSelectedOption() const;

public:
	UPROPERTY(BlueprintAssignable, Category = Events)
	FOnOpeningEvent OnOpening;

	UPROPERTY(BlueprintReadWrite, EditAnywhere)
	int MaxHeight;

public:
	
	void RecursiveAddChildren(TSharedPtr<FPythonTreeNode> ParentNode, const TArray<TSharedPtr<FJsonValue>>& JsonArray);
	void HandleOpening();
protected:
	virtual TSharedRef<SWidget> RebuildWidget() override final;
protected:
	TSharedPtr<SSearchableTreeCombobox> MyTreeView;
	TArray<TSharedPtr<FPythonTreeNode>> RootElements;
};