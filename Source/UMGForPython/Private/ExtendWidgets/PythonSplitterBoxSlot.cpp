#include "ExtendWidgets/PythonSplitterBoxSlot.h"

UPythonSplitterBoxSlot::UPythonSplitterBoxSlot(const FObjectInitializer& ObjectInitializer)
	: Super(ObjectInitializer)
{
}

void UPythonSplitterBoxSlot::SetValue(float InValue)
{
	if ( Slot )
	{
		Slot->SetSizeValue(InValue);
	}
}

FSlateChildSize UPythonSplitterBoxSlot::GetSize()
{
	return Size;
}

void UPythonSplitterBoxSlot::SetSize(FSlateChildSize InSize)
{
	
}

void UPythonSplitterBoxSlot::SynchronizeProperties()
{
	SetValue(Value);
}

void UPythonSplitterBoxSlot::ReleaseSlateResources(bool bReleaseChildren)
{
	Super::ReleaseSlateResources(bReleaseChildren);

	Slot = nullptr;
}

void UPythonSplitterBoxSlot::BuildSlot(TSharedRef<SSplitter> InSSplitter)
{
	InSSplitter->AddSlot()
		.SizeRule(SSplitter::ESizeRule::FractionOfParent)
		.Resizable(true)
		.Expose(Slot)
		.Value(Value)
		[
			Content == nullptr ? SNullWidget::NullWidget : Content->TakeWidget()
		];
}

void UPythonSplitterBoxSlot::SetContent(UWidget* NewContent)
{
	Content = NewContent;
	if (Slot)
	{
		Slot->AttachWidget(NewContent ? NewContent->TakeWidget() : SNullWidget::NullWidget);
	}
}

SSplitter::FSlot* UPythonSplitterBoxSlot::GetSlot() const
{
	return Slot;
}
