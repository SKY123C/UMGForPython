#include "ExtendWidgets/PythonListView.h"

void UPythonListViewString::AddItem(const FString& InItem)
{
	ListItems.Add(MakeShareable(new FString(InItem)));
	if (MyListView)
	{
		MyListView->RequestListRefresh();
	}
}

bool UPythonListViewString::RemoveItem(const FString& InItem)
{
	
	return true;
}

void UPythonListViewString::SetListItems(const TArray<FString>& InListItems)
{
	ClearItems();
	for (const FString& Item : InListItems)
	{
		AddItem(Item);
	}
}

void UPythonListViewString::ClearSelection()
{
	if (MyListView)
	{
		MyListView->ClearSelection();
	}
}

void UPythonListViewString::ClearItems()
{
	ListItems.Reset();
	if (MyListView)
	{
		MyListView->RequestListRefresh();
	}
}

TArray<FString> UPythonListViewString::GetSelectedItems()
{
	TArray<FString> Result;
	if (MyListView)
	{
		for (auto Value : MyListView->GetSelectedItems())
		{
			Result.Add(*Value);
		}
	}
	return Result;
}

TSharedRef<ITableRow> UPythonListViewString::OnGenerateWidget(TSharedPtr<FString> Item, const TSharedRef<STableViewBase>& OwnerTable)
{
	return
		SNew(STableRow<TSharedPtr<FString>>, OwnerTable)
		[
			SNew( STextBlock )
			.Text( FText::FromString(*Item.Get()) )
		];
}

void UPythonListViewString::OnSelectioinChanged(TSharedPtr<FString> Item, ESelectInfo::Type SelectionType)
{
	
	OnSelectionChanged.Broadcast(Item.IsValid() ? *Item : FString(), SelectionType);
}

TSharedRef<SWidget> UPythonListViewString::RebuildWidget()
{
	MyListView = 
		SNew(SListView< TSharedPtr<FString> >)
		.ItemHeight((float)200)
		.ListItemsSource(&ListItems)
		.OnGenerateRow_UObject(this, &UPythonListViewString::OnGenerateWidget)
		.OnSelectionChanged_UObject(this, &UPythonListViewString::OnSelectioinChanged)
		;

	SynchronizeProperties();
	return MyListView.ToSharedRef();
}

void UPythonListViewString::SynchronizeProperties()
{
	Super::SynchronizeProperties();
	if (MyListView)
	{
		MyListView->SetSelectionMode(Multi ? ESelectionMode::Multi : ESelectionMode::Single);
		MyListView->RequestListRefresh();
	}

}
