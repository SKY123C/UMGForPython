#pragma once
#include "CoreMinimal.h"
#include "UMG.h"
#include "EditorUtilityWidgetComponents.h"
#include "Widgets/SWindow.h"
#include "Components/ContentWidget.h"
#include "PythonWindow.generated.h"

UCLASS()
class UPythonWindow : public UContentWidget
{
	GENERATED_UCLASS_BODY()

public:
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	FText WindowText;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	bool IsTopmostWindow = true;

public:
	bool isVaild(){return PythonWindow.IsValid();};
	void Reset()
	{
		if (isVaild())
		{
			PythonWindow.Reset();
		}
	}
	TSharedRef<SWidget> WindowRef(){return PythonWindow.ToSharedRef(); };
	~UPythonWindow();

protected:
	virtual void SynchronizeProperties();
	virtual UClass* GetSlotClass() const override;
	virtual void OnSlotAdded(UPanelSlot* Slot) override;
	virtual void OnSlotRemoved(UPanelSlot* Slot) override;

private:
	TSharedPtr<SWindow> PythonWindow;
	virtual TSharedRef<SWidget> RebuildWidget() override final;

};