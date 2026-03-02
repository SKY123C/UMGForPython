#include "ExtendWidgets/PythonListView.h"
#include "Widgets/Views/SHeaderRow.h"

UPythonListViewString::UPythonListViewString(const FObjectInitializer& ObjectInitializer)
	: Super(ObjectInitializer)
{
}

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

TArray<FString> UPythonListViewString::GetItems()
{
	TArray<FString> Result;
	for (auto i : ListItems)
	{
		Result.Add(*i.Get());
	}
	return Result;
}

TArray<FString> UPythonListViewString::AddSingleHeaderRow(FName Name)
{
	ColumnName = Name;
	return TArray<FString>();
}


TSharedRef<ITableRow> UPythonListViewString::OnGenerateWidget(TSharedPtr<FString> Item, const TSharedRef<STableViewBase>& OwnerTable)
{
	return
		SNew(STableRow<TSharedPtr<FString>>, OwnerTable)
		.Padding(FMargin(4,4,4,4))
		[
			SNew(STextBlock)
			.Text( FText::FromString(*Item.Get()) )
		];
}

void UPythonListViewString::OnSelectioinChanged(TSharedPtr<FString> Item, ESelectInfo::Type SelectionType)
{
	
	OnSelectionChanged.Broadcast(Item.IsValid() ? *Item : FString(), SelectionType);
}

void UPythonListViewString::OnItemDoubleClicked(TSharedPtr<FString> Item)
{
	OnDoubleClicked.Broadcast(Item.IsValid() ? *Item : FString());
}

TSharedRef<SWidget> UPythonListViewString::RebuildWidget()
{
	if (!HeaderRow.IsValid())
	{
		HeaderRow = SNew(SHeaderRow);
		if (!ColumnName.IsNone())
		{
			HeaderRow->AddColumn(
				SHeaderRow::FColumn::FArguments()
				.ColumnId(ColumnName)
				.DefaultLabel(FText::FromName(ColumnName))
				.FillWidth(1.0f)
			);
		}
	}
	MyListView = 
		SNew(SListView< TSharedPtr<FString> >)
		.ListItemsSource(&ListItems)
		.OnGenerateRow_UObject(this, &UPythonListViewString::OnGenerateWidget)
		.OnSelectionChanged_UObject(this, &UPythonListViewString::OnSelectioinChanged)
		.OnMouseButtonDoubleClick_UObject(this, &UPythonListViewString::OnItemDoubleClicked)
		.AllowOverscroll(EAllowOverscroll::No)
		.HeaderRow(HeaderRow)
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
