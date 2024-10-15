#pragma once
#include "CoreMinimal.h"
#include "UMG.h"
#include "Framework/Text/BaseTextLayoutMarshaller.h"
#include "Framework/Text/RichTextLayoutMarshaller.h"
#include "PythonMultiLineEditableTextBox.generated.h"


struct FPythonTextMessage
{
	TSharedRef<FString> Message;
	FTextBlockStyle TextStyle;
	FPythonTextMessage(const TSharedRef<FString>& NewMessage, FTextBlockStyle& Style)
		: Message(NewMessage)
	{
		TextStyle.Font.Size = 5;
	}
};

class FPythonTextLayoutMarshaller : public FBaseTextLayoutMarshaller
{

public:
	static TSharedRef< FPythonTextLayoutMarshaller > Create(TArray<TSharedPtr<FPythonTextMessage>> InMessages);
	virtual ~FPythonTextLayoutMarshaller(){};

	// ITextLayoutMarshaller
	virtual void SetText(const FString& SourceString, FTextLayout& TargetTextLayout) override;
	virtual void GetText(FString& TargetString, const FTextLayout& SourceTextLayout) override;

public:
	FPythonTextLayoutMarshaller(TArray< TSharedPtr<FPythonTextMessage> > InMessages);

protected:
	const ISlateStyle* StyleSet;
	FTextLayout* TextLayout;
	TArray< TSharedPtr<FPythonTextMessage> > Messages;
};


UCLASS()
class UPythonMultiLineEditableTextBox : public UWidget
{
	GENERATED_BODY()

public:
	UPythonMultiLineEditableTextBox();

public:
	UPROPERTY()
	FText Text;
	UFUNCTION(BlueprintCallable)
	void SetText(FText InText);

	UFUNCTION(BlueprintCallable)
	FText GetText();

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	FTextBlockStyle TextBlockStyle;

	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	bool ReadOnly;

protected:
	virtual TSharedRef<SWidget> RebuildWidget() override final;
	virtual void SynchronizeProperties();

protected:
	TSharedPtr< FRichTextLayoutMarshaller > MessagesTextMarshaller;
	TSharedPtr<SMultiLineEditableTextBox> MyEditableTextBlock;
	TSharedPtr<class FSlateStyleSet> StyleInstance;
};