#include "ExtendWidgets/PythonWindow.h"
#include "ExtendWidgets/PythonWindowSlot.h"

UPythonWindow::UPythonWindow(const FObjectInitializer& ObjectInitializer)
	: Super(ObjectInitializer)
{
}

UPythonWindow::~UPythonWindow()
{
	if (PythonWindow.IsValid())
	{
		PythonWindow->RequestDestroyWindow();
		PythonWindow.Reset();
	}
}

void UPythonWindow::SynchronizeProperties()
{

	Super::SynchronizeProperties();
	if (PythonWindow.IsValid())
	{
		PythonWindow->SetTitle(WindowText);
	}
}

UClass* UPythonWindow::GetSlotClass() const
{
	return UPythonWindowSlot::StaticClass();

}

void UPythonWindow::OnSlotAdded(UPanelSlot* InSlot)
{
	if (PythonWindow.IsValid())
	{
		CastChecked<UPythonWindowSlot>(InSlot)->BuildSlot(PythonWindow.ToSharedRef());
	}
}

void UPythonWindow::OnSlotRemoved(UPanelSlot* InSlot)
{
	if (PythonWindow.IsValid())
	{
		PythonWindow->SetContent(SNullWidget::NullWidget);
	}
}

TSharedRef<SWidget> UPythonWindow::RebuildWidget()
{
	PythonWindow = SNew(SWindow)
		.Title(WindowText)
		.ClientSize(FVector2D(800, 600))
		.SupportsMaximize(true)
		.SupportsMinimize(true)
		.IsTopmostWindow(IsTopmostWindow);
	SynchronizeProperties();
	if (GetChildrenCount() > 0)
	{
		Cast<UPythonWindowSlot>(GetContentSlot())->BuildSlot(PythonWindow.ToSharedRef());
	}
	return PythonWindow.ToSharedRef();
}
