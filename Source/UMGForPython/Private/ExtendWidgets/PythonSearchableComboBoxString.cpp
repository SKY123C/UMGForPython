// Copyright Epic Games, Inc. All Rights Reserved.

#include "ExtendWidgets/PythonSearchableComboBoxString.h"
#include "Widgets/SNullWidget.h"
#include "UObject/EditorObjectVersion.h"
#include "UObject/ConstructorHelpers.h"
#include "Engine/Font.h"
#include "Styling/UMGCoreStyle.h"

UPythonSearchableComboBoxString::UPythonSearchableComboBoxString(const FObjectInitializer& ObjectInitializer)
	: Super(ObjectInitializer)
{
	MaxHeight = 500;
}


void UPythonSearchableComboBoxString::HandleSelectionChanged(TSharedPtr<FString> InItem, ESelectInfo::Type SelectionType)
{
	CurrentOptionPtr = InItem;
}

FText UPythonSearchableComboBoxString::GetSelectedText() const
{
	FString OutString = GetSelectedOption();
	return FText::FromString(OutString);
}

TSharedRef<SWidget> UPythonSearchableComboBoxString::RebuildWidget()
{
	PRAGMA_DISABLE_DEPRECATION_WARNINGS
	MyComboBox = SNew(SSearchableComboBox)
	.OptionsSource(&Options).OnGenerateWidget_Lambda([](TSharedPtr<FString> InItem) {
		return
		SNew(STextBlock)
		.Text(FText::FromString(*InItem));
	})
	.OnSelectionChanged(BIND_UOBJECT_DELEGATE(SSearchableComboBox::FOnSelectionChanged, HandleSelectionChanged))
	.OnComboBoxOpening(BIND_UOBJECT_DELEGATE(FOnComboBoxOpening, HandleOpening))
	.MaxListHeight(MaxHeight)
	.Content()
	[
		SNew(STextBlock)
			.Text_UObject(this, &UPythonSearchableComboBoxString::GetSelectedText)
	];
	PRAGMA_ENABLE_DEPRECATION_WARNINGS
	return MyComboBox.ToSharedRef();
}

void UPythonSearchableComboBoxString::HandleOpening()
{
	OnOpening.Broadcast();
}

void UPythonSearchableComboBoxString::AddOption(const FString& Option)
{
	Options.Add(MakeShareable(new FString(Option)));
	RefreshOptions();
}

bool UPythonSearchableComboBoxString::RemoveOption(const FString& Option)
{

	const int32 OptionIndex = FindOptionIndex(Option);

	if (OptionIndex != -1)
	{
		if (Options[OptionIndex] == CurrentOptionPtr)
		{
			ClearSelection();
		}

		Options.RemoveAt(OptionIndex);

		RefreshOptions();

		return true;
	}

	return false;
}

void UPythonSearchableComboBoxString::ClearOptions()
{
	ClearSelection();
	Options.Empty();

	if (MyComboBox.IsValid())
	{
		MyComboBox->RefreshOptions();
	}
}

FString UPythonSearchableComboBoxString::GetSelectedOption() const
{
	if (CurrentOptionPtr.IsValid())
	{
		return *CurrentOptionPtr;
	}
	return FString();
}

void UPythonSearchableComboBoxString::RefreshOptions()
{
	if (MyComboBox.IsValid())
	{
		MyComboBox->RefreshOptions();
	}
}

void UPythonSearchableComboBoxString::ClearSelection()
{
	CurrentOptionPtr.Reset();

	if (MyComboBox.IsValid())
	{
		MyComboBox->ClearSelection();
	}
}

int32 UPythonSearchableComboBoxString::FindOptionIndex(const FString& Option) const
{
	for (int32 OptionIndex = 0; OptionIndex < Options.Num(); OptionIndex++)
	{
		const TSharedPtr<FString>& OptionAtIndex = Options[OptionIndex];

		if ((*OptionAtIndex) == Option)
		{
			return OptionIndex;
		}
	}

	return -1;
}
