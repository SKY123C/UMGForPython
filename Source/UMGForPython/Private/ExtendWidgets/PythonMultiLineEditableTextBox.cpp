#include "ExtendWidgets/PythonMultiLineEditableTextBox.h"
#include "DataTableEditorUtils.h"
#include "Components/RichTextBlock.h"
#include "Framework/Text/RichTextMarkupProcessing.h"
#include "Framework/Text/ITextDecorator.h"
#include "Framework/Text/SlateTextRun.h"


class FPythonRichTextDecorator : public ITextDecorator
{
public:
	FPythonRichTextDecorator(const FTextBlockStyle& TextStyle);

	virtual ~FPythonRichTextDecorator(){};

	virtual bool Supports(const FTextRunParseResults& RunParseResult, const FString& Text) const override;

	virtual TSharedRef<ISlateRun> Create(const TSharedRef<FTextLayout>& TextLayout, const FTextRunParseResults& RunParseResult, const FString& OriginalText, const TSharedRef<FString>& InOutModelText, const ISlateStyle* Style) override;
	
	void ExplodeRunInfo(const FRunInfo& InRunInfo, uint16& OutFontSize, FLinearColor& OutFontColor) const;

	FTextBlockStyle CreateTextBlockStyle(const FRunInfo& InRunInfo);

protected:
	FTextBlockStyle DefaultStyle;
};

FPythonRichTextDecorator::FPythonRichTextDecorator(const FTextBlockStyle& TextStyle)
	:DefaultStyle(TextStyle)
{
}


bool FPythonRichTextDecorator::Supports(const FTextRunParseResults& RunParseResult, const FString& Text) const
{
	return (RunParseResult.Name == TEXT("PythonRichText"));
}

TSharedRef<ISlateRun> FPythonRichTextDecorator::Create(const TSharedRef<FTextLayout>& TextLayout, const FTextRunParseResults& RunParseResult, const FString& OriginalText, const TSharedRef<FString>& InOutModelText, const ISlateStyle* Style)
{
	FRunInfo RunInfo(RunParseResult.Name);
	for (const TPair<FString, FTextRange>& Pair : RunParseResult.MetaData)
	{
		RunInfo.MetaData.Add(Pair.Key, OriginalText.Mid(Pair.Value.BeginIndex, Pair.Value.EndIndex - Pair.Value.BeginIndex));
	}
	FTextRange ModelRange;
	ModelRange.BeginIndex = InOutModelText->Len();
	*InOutModelText += OriginalText.Mid(RunParseResult.ContentRange.BeginIndex, RunParseResult.ContentRange.EndIndex - RunParseResult.ContentRange.BeginIndex);
	ModelRange.EndIndex = InOutModelText->Len();


	return FSlateTextRun::Create(RunInfo, InOutModelText, CreateTextBlockStyle(RunInfo), ModelRange);
}

void FPythonRichTextDecorator::ExplodeRunInfo(const FRunInfo& InRunInfo, uint16& OutFontSize, FLinearColor& OutFontColor) const
{
	const FString* const FontSizeString = InRunInfo.MetaData.Find(TEXT("FontSize"));
	OutFontSize = 10;
	if (FontSizeString)
	{
		OutFontSize = static_cast<uint16>(FPlatformString::Atoi(**FontSizeString));
	}

	OutFontColor = FLinearColor::White;
	const FString* const FontColorString = InRunInfo.MetaData.Find(TEXT("FontColor"));
	if (FontColorString && !OutFontColor.InitFromString(*FontColorString))
	{
		OutFontColor = FLinearColor::White;
	}
}

FTextBlockStyle FPythonRichTextDecorator::CreateTextBlockStyle(const FRunInfo& InRunInfo)
{
	uint16 FontSize;
	FLinearColor FontColor;
	ExplodeRunInfo(InRunInfo, FontSize, FontColor);
	FTextBlockStyle TextBlockStyle;
	TextBlockStyle.SetFont(FCoreStyle::GetDefaultFontStyle("Regular", FontSize));
	TextBlockStyle.SetColorAndOpacity(FontColor);
	return TextBlockStyle;
}

UPythonMultiLineEditableTextBox::UPythonMultiLineEditableTextBox()
{
}

void UPythonMultiLineEditableTextBox::SetText(FText InText)
{
	if (MyEditableTextBlock.IsValid())
	{
		MyEditableTextBlock->SetText(InText);
	}
	else
	{
		Text = InText;
	}
}

FText UPythonMultiLineEditableTextBox::GetText()
{
	FText OutText;
	if (MyEditableTextBlock.IsValid())
	{
		OutText = MyEditableTextBlock->GetText();
	}
	return OutText;
}

TSharedRef<SWidget> UPythonMultiLineEditableTextBox::RebuildWidget()
{
	StyleInstance = MakeShareable(new FSlateStyleSet("RichTextStyle"));
	StyleInstance->Set("PythonRichText", TextBlockStyle);
	TArray< TSharedRef< class ITextDecorator > > Decorators;
	Decorators.Add(MakeShareable(new FPythonRichTextDecorator(TextBlockStyle)));
	MessagesTextMarshaller = FRichTextLayoutMarshaller::Create(
		Decorators,
		StyleInstance.Get()
	);
	MyEditableTextBlock = SNew(SMultiLineEditableTextBox)
							.Marshaller(MessagesTextMarshaller)
							.AutoWrapText(true)
							.AlwaysShowScrollbars(true)
							.Text(Text)
							.IsReadOnly(ReadOnly);
	return MyEditableTextBlock.ToSharedRef();
}

void UPythonMultiLineEditableTextBox::SynchronizeProperties()
{
	Super::SynchronizeProperties();
	if (MyEditableTextBlock.IsValid())
	{
		MyEditableTextBlock->SetText(Text);
		MyEditableTextBlock->Refresh();
	}
}

TSharedRef<FPythonTextLayoutMarshaller> FPythonTextLayoutMarshaller::Create(TArray<TSharedPtr<FPythonTextMessage>> InMessages)
{
	return MakeShareable(new FPythonTextLayoutMarshaller(MoveTemp(InMessages)));
}

void FPythonTextLayoutMarshaller::SetText(const FString& SourceString, FTextLayout& TargetTextLayout)
{
	TextLayout = &TargetTextLayout;
}

void FPythonTextLayoutMarshaller::GetText(FString& TargetString, const FTextLayout& SourceTextLayout)
{
	SourceTextLayout.GetAsText(TargetString);
}

FPythonTextLayoutMarshaller::FPythonTextLayoutMarshaller(TArray<TSharedPtr<FPythonTextMessage>> InMessages)
{
	Messages = MoveTemp(InMessages);
	StyleSet = &FAppStyle::Get();
}
