#pragma once
#include "CoreMinimal.h"
#include "Components/PanelWidget.h"
#include "Widgets/Layout/SSplitter.h"
#include "PythonSplitterBox.generated.h"


UCLASS()
class UPythonSplitterBox : public UPanelWidget
{
	GENERATED_UCLASS_BODY()

public:
	
	UFUNCTION(BlueprintCallable, Category = "PythonUMG|PythonSplitter")
	int32 GetNumWidgets() const;


public:
	
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "PythonUMG|PythonSplitter")
	TEnumAsByte<EOrientation> Orientation;


public:


protected:
	virtual void SynchronizeProperties();
	virtual UClass* GetSlotClass() const override;
	virtual void OnSlotAdded(UPanelSlot* Slot) override;
	virtual void OnSlotRemoved(UPanelSlot* Slot) override;
	virtual TSharedRef<SWidget> RebuildWidget() override final;
	TSharedPtr<SSplitter> Splitter;
	
};

