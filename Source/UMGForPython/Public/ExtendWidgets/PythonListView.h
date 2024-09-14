#pragma once
#include "CoreMinimal.h"
#include "EditorUtilityWidget.h"
#include "Components/Button.h"
#include "Blueprint/UserWidget.h"
#include "Components/Widget.h"
#include "UMG.h"
#include "InputCoreTypes.h"
#include "Input/Events.h"
#include "Widgets/Views/SlistView.h"
#include "PythonListView.generated.h"

UCLASS()
class UPythonListViewString : public UWidget
{
	GENERATED_BODY()

	DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnSelectionChangedEvent, FString, SelectedItem, ESelectInfo::Type, SelectionType);

public:
	UFUNCTION(BlueprintCallable)
	void AddItem(const FString& InItem);

	UFUNCTION(BlueprintCallable)
	bool RemoveItem(const FString& InItem);

	UFUNCTION(BlueprintCallable)
	void SetListItems(const TArray<FString>& InListItems);

	UFUNCTION(BlueprintCallable)
	void ClearSelection();

	UFUNCTION(BlueprintCallable)
	void ClearItems();

	UFUNCTION(BlueprintCallable)
	TArray<FString> GetSelectedItems();

public:

	UPROPERTY(BlueprintAssignable)
	FOnSelectionChangedEvent OnSelectionChanged;

	UPROPERTY(EditAnyWhere)
	bool Multi;

	UPROPERTY(EditAnyWhere)
	int ItemHeight = 15;

public:


protected:
	
	TSharedRef<ITableRow> OnGenerateWidget(TSharedPtr<FString> Item, const TSharedRef< STableViewBase >& OwnerTable);
	virtual void SynchronizeProperties();
	void OnSelectioinChanged(TSharedPtr<FString> Item, ESelectInfo::Type SelectionType);
	TArray< TSharedPtr<FString> > ListItems;
	virtual TSharedRef<SWidget> RebuildWidget() override final;
	TSharedPtr< SListView< TSharedPtr<FString> >> MyListView;
};

