#include "ExtendWidgets/PythonWindowSlot.h"

UPythonWindowSlot::UPythonWindowSlot(const FObjectInitializer& ObjectInitializer)
	: Super(ObjectInitializer)
{
}


void UPythonWindowSlot::SynchronizeProperties()
{
	Super::SynchronizeProperties();
}

void UPythonWindowSlot::ReleaseSlateResources(bool bReleaseChildren)
{
	Super::ReleaseSlateResources(bReleaseChildren);
}

void UPythonWindowSlot::BuildSlot(TSharedRef<SWindow> InWindow)
{
    MyWindow = InWindow;
	

	InWindow->SetContent(Content ? Content->TakeWidget() : SNullWidget::NullWidget);
}
