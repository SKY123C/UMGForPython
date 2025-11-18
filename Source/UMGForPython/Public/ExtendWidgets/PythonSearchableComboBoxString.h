// copyright lolol

#pragma once

#include "CoreMinimal.h"
#include "SSearchableComboBox.h"
#include "Components/Widget.h"
#include "PythonSearchableComboBoxString.generated.h"

/**
 * Combo box that can be searched.
 */
UCLASS()
class UPythonSearchableComboBoxString : public UWidget
{
	GENERATED_UCLASS_BODY()
	DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnSelectionChangedEvent, FString, SelectedItem, ESelectInfo::Type, SelectionType);
	DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnOpeningEvent);

public:
	UFUNCTION(BlueprintCallable, Category = "PythonUMG|PythonSearchableComboBox")
	void AddOption(const FString& Option);

	UFUNCTION(BlueprintCallable, Category = "PythonUMG|PythonSearchableComboBox")
	bool RemoveOption(const FString& Option);

	UFUNCTION(BlueprintCallable, Category = "PythonUMG|PythonSearchableComboBox")
	void ClearOptions();

	UFUNCTION(BlueprintCallable, Category = "PythonUMG|PythonSearchableComboBox")
	FString GetSelectedOption() const;

	UFUNCTION(BlueprintCallable, Category = "PythonUMG|PythonSearchableComboBox")
	void RefreshOptions();

	UFUNCTION(BlueprintCallable, Category = "PythonUMG|PythonSearchableComboBox")
	void ClearSelection();

	UFUNCTION(BlueprintCallable, Category = "PythonUMG|PythonSearchableComboBox")
	int32 FindOptionIndex(const FString& Option) const;

public:
	UPROPERTY(BlueprintAssignable, Category = Events)
	FOnOpeningEvent OnOpening;

	UPROPERTY(BlueprintReadWrite, EditAnywhere)
	int MaxHeight;

public:
	void HandleSelectionChanged(TSharedPtr<FString> InItem, ESelectInfo::Type SelectionType);
	FText GetSelectedText() const;

protected:
	virtual TSharedRef<SWidget> RebuildWidget() override final;
	TSharedPtr<FString> CurrentOptionPtr;

	void HandleOpening();

private:
	TArray< TSharedPtr<FString> > Options;
	TSharedPtr<SSearchableComboBox> MyComboBox;
};