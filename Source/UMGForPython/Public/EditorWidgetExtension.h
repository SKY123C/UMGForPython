﻿#pragma once
#include "CoreMinimal.h"
#include "Blueprint/UserWidget.h"
#include "Components/Widget.h"
#include "UMG.h"
#include "EditorWidgetExtension.generated.h"

UCLASS()
class UPythonWidgetExtendLib : public UBlueprintFunctionLibrary
{

	GENERATED_BODY()

public:

	UFUNCTION(BlueprintCallable)
	static UTexture2D* CreateTexture2DFromRaw(TArray<uint8> RawData, int32 Width, int32 Height, int32 ChannelNum, bool bUseSRGB = false, int32 TextureFilterValue = -1, bool bBGR = false, bool FlipY = false);

	UFUNCTION(BlueprintCallable)
	static UTexture2D* CreateTexture2DFromFile(FString FilePath);

	UFUNCTION(BlueprintCallable)
	static void GetRootWidget(UUserWidget* Widget);

	UFUNCTION(BlueprintCallable)
	static void ShowWindow(UWidget* Widget);

	UFUNCTION(BlueprintCallable)
	static void SpawnAndRegisterTab(FName TabID, FString TabLabel, UWidget* Widget);

	UFUNCTION(BlueprintCallable)
	static void AddRootWidget(UUserWidget* Widget);

	UFUNCTION(BlueprintCallable)
	static void GetCheckBoxStyle(FCheckBoxStyle& WidgetStyle, FString Style, FName StyleNmae);

	UFUNCTION(BlueprintCallable)
	static void GetComboBoxStyle(FComboButtonStyle& WidgetStyle, FString Style, FName StyleNmae);

	UFUNCTION(BlueprintCallable)
	static void GetButtonStyle(FButtonStyle& WidgetStyle, FString Style, FName StyleNmae);

	UFUNCTION(BlueprintCallable)
	static void GetTextBlockStyle(FTextBlockStyle& WidgetStyle, FString Style, FName StyleNmae);

	UFUNCTION(BlueprintCallable)
	static void SetBorderBrush(UBorder* Widget, FString Style, FString BrushNmae);

	UFUNCTION(BlueprintCallable)
	static void SetImageBrush(UImage* Widget, FString Style, FString BrushNmae);

	UFUNCTION(BlueprintCallable)
	static void GetBrush(FSlateBrush& Brush, FString Style, FString BrushNmae);

	UFUNCTION(BlueprintCallable)
	static void CallFuncByAddress(FString Address);

};