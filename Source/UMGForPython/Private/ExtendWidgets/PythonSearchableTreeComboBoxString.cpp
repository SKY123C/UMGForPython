#pragma once

#include "ExtendWidgets/PythonSearchableTreeComboBoxString.h"

UPythonSearchableTreeComboBoxString::UPythonSearchableTreeComboBoxString(const FObjectInitializer& ObjectInitializer)
	: Super(ObjectInitializer)
{
	MaxHeight = 500;
}

void UPythonSearchableTreeComboBoxString::ParseTreeNodes(const FString& JsonStr)
{
	//{"Root": [{"DisplayName": "W_Game", "NodeType": "CATEGORY", "Plot": "", "ID": "", "Children": []}]}
	RootElements.Empty();
	TSharedPtr<FJsonObject> JsonObject;
	TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(JsonStr);
	FJsonSerializer::Deserialize(Reader, JsonObject);
	if (!JsonObject.IsValid())
	{
		UE_LOG(LogTemp, Warning, TEXT("Failed to parse JSON string."));
		return;
	}
    const TArray<TSharedPtr<FJsonValue>>& SourceList = JsonObject->GetArrayField(TEXT("Root"));
	for (TSharedPtr<FJsonValue> Value : SourceList)
	{
		TSharedPtr<FJsonObject> Root = Value->AsObject();
		TSharedRef<FPythonTreeNode> Node = FPythonTreeNode::Make(
			Root->GetStringField(TEXT("DisplayName")), 
			Root->GetStringField(TEXT("ID")), 
			Root->GetStringField(TEXT("Plot"))
		);
		Node->SetNodeType(Root->GetStringField(TEXT("NodeType")));
		RecursiveAddChildren(Node, Root->GetArrayField(TEXT("Children")));
		RootElements.Add(Node);
	}
	if (MyTreeView.IsValid())
	{
		MyTreeView->RefreshOptions();
	}
}

FString UPythonSearchableTreeComboBoxString::GetSelectedOption() const
{
	if (MyTreeView.IsValid() && MyTreeView->GetSelectedItem().IsValid())
	{
		return MyTreeView->GetSelectedItem()->GetName();
	}
	return FString();
}


void UPythonSearchableTreeComboBoxString::RecursiveAddChildren(TSharedPtr<FPythonTreeNode> ParentNode, const TArray<TSharedPtr<FJsonValue>>& JsonArray)
{
	if (!ParentNode.IsValid())
	{
		return;
	}
	for (TSharedPtr<FJsonValue> Value : JsonArray)
	{
		TSharedPtr<FJsonObject> ChildObject = Value->AsObject();
		if (ChildObject.IsValid())
		{
			TSharedRef<FPythonTreeNode> ChildNode = FPythonTreeNode::Make(
				ChildObject->GetStringField(TEXT("DisplayName")),
				ChildObject->GetStringField(TEXT("ID")),
				ChildObject->GetStringField(TEXT("Plot"))
			);
			ChildNode->SetNodeType(ChildObject->GetStringField(TEXT("NodeType")));
			ParentNode->AddChild(ChildNode);
			// Recursively add children if they exist
			if (ChildObject->HasField(TEXT("Children")))
			{
				const TArray<TSharedPtr<FJsonValue>>& GrandChildren = ChildObject->GetArrayField(TEXT("Children"));
				RecursiveAddChildren(ChildNode, GrandChildren);
			}
		}
	}
}

void UPythonSearchableTreeComboBoxString::HandleOpening()
{
	OnOpening.Broadcast();
}

TSharedRef<SWidget> UPythonSearchableTreeComboBoxString::RebuildWidget()
{
	MyTreeView = SNew(SSearchableTreeCombobox)
		.OptionsSource(&RootElements)
		.MaxHeight(MaxHeight)
		.OnComboBoxOpening(BIND_UOBJECT_DELEGATE(FOnComboBoxOpening, HandleOpening))
		.Content()
		[
			SNew(STextBlock)
				.Text_Lambda([this]() { return FText::FromString(this->GetSelectedOption()); })
		];
	return MyTreeView.ToSharedRef();
}
