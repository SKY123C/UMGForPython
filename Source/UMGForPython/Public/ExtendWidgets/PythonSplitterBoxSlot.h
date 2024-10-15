#pragma once
#include "CoreMinimal.h"
#include "Components/PanelWidget.h"
#include "Widgets/Layout/SSplitter.h"
#include "Components/PanelSlot.h"
#include "PythonSplitterBoxSlot.generated.h"

UCLASS()
class UPythonSplitterBoxSlot : public UPanelSlot
{
	GENERATED_UCLASS_BODY()

public:

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "PythonUMG|PythonSplitterBoxSlot")
	float Value = 1.0f;

public:

	UFUNCTION(BlueprintCallable, Category = "PythonUMG|PythonSplitterBoxSlot")
	void SetValue(float InValue);

	UFUNCTION(BlueprintCallable, Category = "PythonUMG|PythonSplitterBoxSlot")
	FSlateChildSize GetSize();

	UFUNCTION(BlueprintCallable, Category = "PythonUMG|PythonSplitterBoxSlot")
	void SetSize(FSlateChildSize InSize);

public:

	//~ UPanelSlot interface
	virtual void SynchronizeProperties() override;
	//~ End of UPanelSlot interface

	virtual void ReleaseSlateResources(bool bReleaseChildren) override;

	/** Builds the underlying FSlot for the Slate layout panel. */
	void BuildSlot(TSharedRef<SSplitter> InSSplitter);

	/** Sets the content of this slot, removing existing content if needed. */
	void SetContent(UWidget* NewContent);

	SSplitter::FSlot* GetSlot() const;
private:
	SSplitter::FSlot* Slot;
	FSlateChildSize Size;
};