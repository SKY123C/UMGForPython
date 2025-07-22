#pragma once
#include "CoreMinimal.h"
#include "Components/PanelWidget.h"
#include "Components/PanelSlot.h"
#include "Widgets/SWindow.h"
#include "PythonWindowSlot.generated.h"

UCLASS()
class UPythonWindowSlot : public UPanelSlot
{
	GENERATED_UCLASS_BODY()

public:

public:


public:

	//~ UPanelSlot interface
	virtual void SynchronizeProperties() override;
	//~ End of UPanelSlot interface

	virtual void ReleaseSlateResources(bool bReleaseChildren) override;

	/** Builds the underlying FSlot for the Slate layout panel. */
	void BuildSlot(TSharedRef<SWindow> InWindow);


private:
	TWeakPtr<SWindow> MyWindow;
	FSlateChildSize Size;
};