#include "ExtendWidgets/PythonSplitterBox.h"
#include "ExtendWidgets/PythonSplitterBoxSlot.h"

UPythonSplitterBox::UPythonSplitterBox(const FObjectInitializer& ObjectInitializer)
	: Super(ObjectInitializer)
{
}

void UPythonSplitterBox::SynchronizeProperties()
{
	Super::SynchronizeProperties();
	if (Splitter.IsValid())
	{
		Splitter->SetOrientation(Orientation);
	}
}

UClass* UPythonSplitterBox::GetSlotClass() const
{
	return UPythonSplitterBoxSlot::StaticClass();
}

void UPythonSplitterBox::OnSlotAdded(UPanelSlot* InSlot)
{
	if (Splitter.IsValid())
	{
		CastChecked<UPythonSplitterBoxSlot>(InSlot)->BuildSlot(Splitter.ToSharedRef());
	}
}

void UPythonSplitterBox::OnSlotRemoved(UPanelSlot* InSlot)
{

	if (Splitter.IsValid() && InSlot->Content)
	{
		TSharedPtr<SWidget> Widget = InSlot->Content->GetCachedWidget();
		if (Widget.IsValid())
		{
			UPythonSplitterBoxSlot* TypedSlot = Cast<UPythonSplitterBoxSlot>(InSlot);
			for (int i = 0; i < Splitter->GetChildren()->Num(); i++)
			{
				if (TypedSlot && Splitter->SlotAt(i).GetWidget() == TypedSlot->GetSlot()->GetWidget())
				{
					
					Splitter->RemoveAt(i);
					break;
				}
			}
		}
	}
}

TSharedRef<SWidget> UPythonSplitterBox::RebuildWidget()
{
	Splitter = SNew(SSplitter);
	for (UPanelSlot* PanelSlot : Slots)
	{
		if (UPythonSplitterBoxSlot* TypedSlot = Cast<UPythonSplitterBoxSlot>(PanelSlot))
		{
			TypedSlot->Parent = this;
			TypedSlot->BuildSlot(Splitter.ToSharedRef());
		}
	}
	SynchronizeProperties();
	return Splitter.ToSharedRef();
}

int32 UPythonSplitterBox::GetNumWidgets() const
{
	if (Splitter.IsValid())
	{
		return Splitter->GetChildren()->Num();
	}
	return Slots.Num();
}

