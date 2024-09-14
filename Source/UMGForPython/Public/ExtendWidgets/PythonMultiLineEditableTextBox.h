#pragma once
#include "CoreMinimal.h"
#include "EditorUtilityWidget.h"
#include "Components/Button.h"
#include "Blueprint/UserWidget.h"
#include "Components/Widget.h"
#include "UMG.h"
#include "Framework/Text/BaseTextLayoutMarshaller.h"
#include "PythonMultiLineEditableTextBox.generated.h"

class FPythonTextLayoutMarshaller : public FBaseTextLayoutMarshaller
{

public:

};


UCLASS()
class PythonMultiLineEditableTextBox : public UWidget
{
	GENERATED_BODY()

public:
	PythonMultiLineEditableTextBox();
protected:
	virtual TSharedRef<SWidget> RebuildWidget() override final;
	virtual void SynchronizeProperties();

protected:
	TSharedPtr<SMultiLineEditableTextBox> MyEditableTextBlock;
};