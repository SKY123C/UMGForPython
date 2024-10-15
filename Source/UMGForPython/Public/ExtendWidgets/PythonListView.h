#pragma once
#include "CoreMinimal.h"
#include "UMG.h"
#include "Widgets/Views/SlistView.h"
#include "PythonListView.generated.h"

UCLASS()
class UPythonListViewString : public UWidget
{
	GENERATED_UCLASS_BODY()

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

	UFUNCTION(BlueprintCallable)
	TArray<FString> GetItems();

	UFUNCTION(BlueprintCallable)
	TArray<FString> AddSingleHeaderRow(FName Name);

public:

	UPROPERTY(BlueprintAssignable)
	FOnSelectionChangedEvent OnSelectionChanged;

	UPROPERTY(BlueprintReadWrite,EditAnyWhere)
	bool Multi;

	UPROPERTY(BlueprintReadWrite,EditAnyWhere)
	int ItemHeight = 15;



public:


protected:
	
	TSharedRef<ITableRow> OnGenerateWidget(TSharedPtr<FString> Item, const TSharedRef< STableViewBase >& OwnerTable);
	virtual void SynchronizeProperties();
	void OnSelectioinChanged(TSharedPtr<FString> Item, ESelectInfo::Type SelectionType);
	TArray< TSharedPtr<FString> > ListItems;
	virtual TSharedRef<SWidget> RebuildWidget() override final;
	TSharedPtr< SListView< TSharedPtr<FString> >> MyListView;
	TSharedPtr<SHeaderRow> HeaderRow = SNew(SHeaderRow);
};

