#include "EditorWidgetExtension.h"
#include "Framework/Application/SlateApplication.h"
#include "Components/VerticalBox.h"
#include "Blueprint/WidgetTree.h"
#include "Widgets/SWindow.h"
#include "TextureCompiler.h"
#include "ImageUtils.h"
#include "UMG.h"

#if ENGINE_MAJOR_VERSION == 5 && ENGINE_MINOR_VERSION >=1
#define FEditorStyle FAppStyle
#endif


#define SETSTYLE(StyleTyle, InStyle, Style, StyleName) { \
    if(Style.Equals("FEditorStyle", ESearchCase::IgnoreCase)) \
    { \
        InStyle = FEditorStyle::Get().GetWidgetStyle<StyleTyle>(StyleName); \
    } \
    else if(Style.Equals("FCoreStyle", ESearchCase::IgnoreCase)) \
    { \
        InStyle = FCoreStyle::Get().GetWidgetStyle<StyleTyle>(StyleName); \
    } \
    else if(Style.Equals("FAppStyle", ESearchCase::IgnoreCase)) \
    { \
        InStyle = FAppStyle::Get().GetWidgetStyle<StyleTyle>(StyleName); \
    } \
    else \
    { \
        UE_LOG(LogTemp, Warning, TEXT("Style: %s Not Support yet"), *Style); \
    } \
};

UTexture2D* UPythonWidgetExtendLib::CreateTexture2DFromFile(FString FilePath)
{
    UTexture2D* Texture2D = nullptr;
    if (FPaths::FileExists(FilePath))
        Texture2D = FImageUtils::ImportFileAsTexture2D(FilePath);
    return Texture2D;
}
void UPythonWidgetExtendLib::GetRootWidget(UUserWidget* Widget)
{

}
void UPythonWidgetExtendLib::ShowWindow(UWidget* Widget)
{
    auto Window = SNew(SWindow)                       
        .Title(FText::FromString("CustomWindow"))     
        .ClientSize(FVector2D(600, 600))               
        [                                               
            Widget->TakeWidget()
        ];
   
    FSlateApplication::Get().AddWindow(Window, true);
}

void UPythonWidgetExtendLib::SpawnAndRegisterTab(FName TabID, FString TabLabel, UWidget* Widget)
{

    if (!FGlobalTabmanager::Get()->HasTabSpawner(TabID))
    {
        FGlobalTabmanager::Get()->RegisterTabSpawner(TabID, FOnSpawnTab::CreateLambda([TabID, Widget, TabLabel](const FSpawnTabArgs& Args)
        {
            return SNew(SDockTab)
                .Clipping(EWidgetClipping::ClipToBounds)
                .Label(FText::FromString(TabLabel))
                .OnTabClosed_Lambda([TabID](TSharedRef<SDockTab>){FGlobalTabmanager::Get()->UnregisterTabSpawner(TabID);})
                [
                    Widget->TakeWidget()
                ];
        }
        ));
    }
    else
    {
        TSharedPtr<SDockTab> DockTab = FGlobalTabmanager::Get()->FindExistingLiveTab(FTabId(TabID));
        if (DockTab.IsValid())
        {
            DockTab->SetContent(Widget->TakeWidget());
        }
    }
    FGlobalTabmanager::Get()->TryInvokeTab(FTabId(TabID));
}

void UPythonWidgetExtendLib::AddRootWidget(UUserWidget* Widget)
{
    UWidget* Root = Widget->WidgetTree->ConstructWidget<UVerticalBox>(UVerticalBox::StaticClass());
    Widget->WidgetTree->RootWidget = Root;
}

void UPythonWidgetExtendLib::GetCheckBoxStyle(FCheckBoxStyle& WidgetStyle, FString Style, FName StyleNmae)
{
    SETSTYLE(FCheckBoxStyle, WidgetStyle, Style, StyleNmae);
}

void UPythonWidgetExtendLib::GetComboBoxStyle(FComboButtonStyle& WidgetStyle, FString Style, FName StyleNmae)
{
    SETSTYLE(FComboButtonStyle, WidgetStyle, Style, StyleNmae);
}

void UPythonWidgetExtendLib::GetButtonStyle(FButtonStyle& WidgetStyle, FString Style, FName StyleNmae)
{
    SETSTYLE(FButtonStyle, WidgetStyle, Style, StyleNmae);
}

void UPythonWidgetExtendLib::GetTextBlockStyle(FTextBlockStyle& WidgetStyle, FString Style, FName StyleNmae)
{
    SETSTYLE(FTextBlockStyle, WidgetStyle, Style, StyleNmae);
}

void UPythonWidgetExtendLib::SetBorderBrush(UBorder* Widget, FString Style, FString BrushNmae)
{
    
}

void UPythonWidgetExtendLib::SetImageBrush(UImage* Widget, FString Style, FString BrushNmae)
{
    
}
void UPythonWidgetExtendLib::GetBrush(FSlateBrush& Brush, FString Style, FString BrushNmae)
{
    if (Style.Equals("FCoreStyle", ESearchCase::IgnoreCase))
    {
        Brush = *FCoreStyle::Get().GetBrush(*BrushNmae);
    }
    else if (Style.Equals("FEditorStyle", ESearchCase::IgnoreCase))
    {
        Brush = *FEditorStyle::Get().GetBrush(*BrushNmae);
    }
    else if (Style.Equals("FAppStyle", ESearchCase::IgnoreCase))
    {
#if ENGINE_MAJOR_VERSION == 4
        UE_LOG(PythonTA, Error, TEXT("FAppStyle, only supported in UE5."));
#else
        Brush = *FAppStyle::Get().GetBrush(*BrushNmae);
#endif
    }
    else {
        UE_LOG(LogTemp, Warning, TEXT("Style: %s Not Support yet. Supperted Style: FEditorStyle, FCoreStyle and FAppStyle."), *Style);
    }
}

UPythonUserWidget::UPythonUserWidget(const FObjectInitializer& ObjectInitializer)
    : Super(ObjectInitializer)
{
    WidgetTree = NewObject<UWidgetTree>(this, TEXT("WidgetTree"), RF_Transient);
    UWidget* RootLayout = WidgetTree->ConstructWidget<UVerticalBox>(UVerticalBox::StaticClass());
    WidgetTree->RootWidget = RootLayout;
}

bool UPythonUserWidget::Initialize()
{
    bool b = Super::Initialize();
    CustomInitialize();
    return true;
}

void UPythonUserWidget::CustomInitialize_Implementation()
{
    
}

FReply UPythonUserWidget::NativeOnMouseButtonDown(const FGeometry& InGeometry, const FPointerEvent& InMouseEvent)
{
    
    UE_LOG(LogTemp, Warning, TEXT("%d"), &InMouseEvent);
    return Super::NativeOnMouseButtonDown(InGeometry, InMouseEvent);
}