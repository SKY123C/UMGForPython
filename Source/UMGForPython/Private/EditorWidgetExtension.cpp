#include "EditorWidgetExtension.h"
#include "Framework/Application/SlateApplication.h"
#include "Components/VerticalBox.h"
#include "Blueprint/WidgetTree.h"
#include "Widgets/SWindow.h"
#include "TextureCompiler.h"
#include "ImageUtils.h"
#include "UMG.h"
#include <iostream>
#include <sstream>
#include <string>
#include "Misc/Parse.h"
#include "UMGForPython.h"
#include "ExtendWidgets/PythonWindow.h"

#undef UpdateResource
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
UTexture2D* UPythonWidgetExtendLib::CreateTexture2DFromRaw(TArray<uint8> RawData, int32 Width, int32 Height, int32 ChannelNum, bool bUseSRGB, int32 TextureFilterValue, bool bBGR, bool bFlipY)
{

    // Decompress PNG image

    if (Width <= 0 || Height <= 0)
        return nullptr;
    if (RawData.Num() != Width * Height * ChannelNum)
    {
        UE_LOG(LogTemp, Warning, TEXT("RawData.Num(%d) != Width(%d) * Height(%d) * ChannelNum(%d)"), RawData.Num(), Width, Height, ChannelNum);
        return nullptr;
    }


    // Fill in the base mip for the texture we created
    UTexture2D* NewTexture2D = UTexture2D::CreateTransient(Width, Height, EPixelFormat::PF_B8G8R8A8);

    NewTexture2D->Source.Init(Width, Height, 1, 1, ETextureSourceFormat::TSF_BGRA8, nullptr);
    NewTexture2D->UpdateResource();
    // Fill in the base mip for the texture we created
#if ENGINE_MAJOR_VERSION == 5
    uint8* MipData = NewTexture2D->Source.LockMip(0);
#else
    uint8* MipData = (uint8*)NewTexture2D->PlatformData->Mips[0].BulkData.Lock(LOCK_READ_WRITE);
#endif
    for (int32 y = 0; y < Height; y++)
    {
        uint8* DestPtr = bFlipY ? &MipData[y * Width * sizeof(FColor)] : &MipData[(Height - 1 - y) * Width * sizeof(FColor)];
        //const FColor* SrcPtr = &((FColor*)(RawData.GetData()))[(Height - 1 - y) * Width];

        for (int32 x = 0; x < Width; x++)
        {
            int32 Index = (x + Width * y) * ChannelNum;
            uint8 r = RawData[Index];
            uint8 g = 0, b = 0, a = 0;
            if (ChannelNum == 1)
            {
                g = b = r;
                a = 255;
            }
            else if (ChannelNum == 2)
            {
                g = b = r;
                a = RawData[Index + 1];
            }
            else if (ChannelNum == 3)
            {
                g = RawData[Index + 1];
                b = RawData[Index + 2];
                a = 255;
            }
            else if (ChannelNum == 4) {
                g = RawData[Index + 1];
                b = RawData[Index + 2];
                a = RawData[Index + 3];
            }
            *DestPtr++ = bBGR ? r : b;
            *DestPtr++ = g;
            *DestPtr++ = bBGR ? b : r;
            *DestPtr++ = a;

        }
    }
#if ENGINE_MAJOR_VERSION == 5
    NewTexture2D->Source.UnlockMip(0);
#else
    NewTexture2D->PlatformData->Mips[0].BulkData.Unlock();
#endif

    // Set options
    NewTexture2D->SRGB = bUseSRGB;
    NewTexture2D->CompressionNone = true;
    NewTexture2D->MipGenSettings = TMGS_NoMipmaps;
    NewTexture2D->CompressionSettings = TC_Default;
    NewTexture2D->AddressX = TextureAddress::TA_Clamp;
    NewTexture2D->AddressY = TextureAddress::TA_Clamp;
    NewTexture2D->CompressionSettings = TextureCompressionSettings::TC_VectorDisplacementmap;

    NewTexture2D->Filter = TF_Default;
    if (0 <= TextureFilterValue && TextureFilterValue < TF_MAX) {
        NewTexture2D->Filter = (TextureFilter)(TextureFilterValue);
    }
    // Update the remote texture data
    NewTexture2D->UpdateResource();

    NewTexture2D->PostEditChange();
    FTextureCompilingManager::Get().FinishCompilation({ NewTexture2D });
    return NewTexture2D;
}
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
void UPythonWidgetExtendLib::ShowWindow(UPythonWindow* InWindow, bool bModal)
{
    bool Vaild = InWindow->isVaild();
    if (Vaild)
    {
        InWindow->Reset();
    }
    
    TSharedRef<SWindow> WindowRef = StaticCastSharedRef<SWindow>(InWindow->TakeWidget());
    TSharedPtr<SWindow> TopWindow = FSlateApplication::Get().GetActiveTopLevelWindow();
    
    if (bModal)
    {
        GEditor->EditorAddModalWindow(WindowRef);
    }
    else
    {
        FSlateApplication::Get().AddWindow(WindowRef, true);
    }
}

void UPythonWidgetExtendLib::CloseWindow(UPythonWindow* InWindow)
{
    if (InWindow->isVaild())
    {
        TSharedPtr<SWindow> Window = FSlateApplication::Get().FindWidgetWindow(InWindow->WindowRef());
        if (Window.IsValid())
        {
            Window->RequestDestroyWindow();
        }
    }

}



void UPythonWidgetExtendLib::SpawnAndRegisterTab(FName TabID, FString TabLabel, UWidget* Widget)
{
    if (Widget && !Widget->IsRooted())
    {
        Widget->AddToRoot();
    }
    if (!FGlobalTabmanager::Get()->HasTabSpawner(TabID))
    {
        FGlobalTabmanager::Get()->RegisterTabSpawner(TabID, FOnSpawnTab::CreateLambda([TabID, Widget, TabLabel](const FSpawnTabArgs& Args)
        {
            return SNew(SDockTab)
                .Clipping(EWidgetClipping::ClipToBounds)
                .Label(FText::FromString(TabLabel))
                .OnTabClosed_Lambda([TabID, Widget](TSharedRef<SDockTab>) {
                    FGlobalTabmanager::Get()->UnregisterTabSpawner(TabID);
                    if (Widget && Widget->IsRooted())
                    {
                        Widget->RemoveFromRoot();
                    }
                })
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