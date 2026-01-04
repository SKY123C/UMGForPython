#include "NativeWidgets/SSearchableTreeCombobox.h"
#include "Algo/AllOf.h"
#include "Widgets/Layout/SScrollBorder.h"

void SSearchableTreeCombobox::Construct(const FArguments& InArgs)
{
	this->bAlwaysSelectItem = InArgs._bAlwaysSelectItem;
	this->OnComboBoxOpening = InArgs._OnComboBoxOpening;
	const FComboButtonStyle& OurComboButtonStyle = InArgs._ComboBoxStyle->ComboButtonStyle;
	const FButtonStyle* const OurButtonStyle = InArgs._ButtonStyle ? InArgs._ButtonStyle : &OurComboButtonStyle.ButtonStyle;
	OptionsSource = InArgs._OptionsSource;
	FilteredOptionsSource.Append(*OptionsSource);
	TAttribute<EVisibility> SearchVisibility = InArgs._SearchVisibility;

	SAssignNew(this->MyTreeView, STreeView<TSharedPtr<FPythonTreeNode>>)
		.OnGetChildren(this, &SSearchableTreeCombobox::OnGetChildren)
		.OnGenerateRow(this, &SSearchableTreeCombobox::OnGenerateRow)
		.OnSelectionChanged(this, &SSearchableTreeCombobox::OnSelectionChanged_Internal)
		.OnKeyDownHandler(this, &SSearchableTreeCombobox::OnKeyDownHandler)
		.SelectionMode(ESelectionMode::Single)
		.TreeItemsSource(&FilteredOptionsSource)
		.HeaderRow
		(
			SNew(SHeaderRow)
			+ SHeaderRow::Column("Name").DefaultLabel(FText::FromString(TEXT("名称")))
			.Visibility(EVisibility::Visible)
			+ SHeaderRow::Column("Plot").DefaultLabel(FText::FromString(TEXT("剧情")))
			.Visibility(EVisibility::Visible)
			+ SHeaderRow::Column("ID").DefaultLabel(FText::FromString(TEXT("ID")))
			.Visibility(EVisibility::Visible)
		);
	TSharedRef<SWidget> ComboBoxMenuContent =
		SNew(SBox)
		.MaxDesiredHeight(InArgs._MaxHeight)
		[
			SNew(SVerticalBox)

				+ SVerticalBox::Slot()
				.AutoHeight()
				[
					SAssignNew(this->SearchField, SEditableTextBox)
						.HintText(FText::FromString(TEXT("Search")))
						.OnTextChanged(this, &SSearchableTreeCombobox::OnSearchTextChanged)
						.OnTextCommitted(this, &SSearchableTreeCombobox::OnSearchTextCommitted)
						.Visibility(SearchVisibility)
				]

				+ SVerticalBox::Slot()
				.FillHeight(1)
				[
					SNew(SScrollBorder, MyTreeView.ToSharedRef())
					[
						MyTreeView.ToSharedRef()
					]
				]
		];
	TSharedPtr<SWidget> ButtonContent = InArgs._Content.Widget;
	if (InArgs._Content.Widget == SNullWidget::NullWidget)
	{
		SAssignNew(ButtonContent, STextBlock)
			.Text(NSLOCTEXT("SSearchableComboBox", "ContentWarning", "No Content Provided"))
			.ColorAndOpacity(FLinearColor::Red);
	}

	SComboButton::Construct(SComboButton::FArguments()
		.ComboButtonStyle(&OurComboButtonStyle)
		.ButtonStyle(OurButtonStyle)
		.ButtonContent()
		[
			ButtonContent.ToSharedRef()
		]
		.MenuContent()
		[
			ComboBoxMenuContent
		]
		.HasDownArrow(InArgs._HasDownArrow)
		.ContentPadding(InArgs._ContentPadding)
		.ForegroundColor(InArgs._ForegroundColor)
		.IsFocusable(true)
	);
}

FReply SSearchableTreeCombobox::OnButtonClicked()
{
	if (this->IsOpen())
	{
		// Re-select first selected item, just in case it was selected by navigation previously
		TArray<TSharedPtr<FPythonTreeNode>> SelectedItems = MyTreeView->GetSelectedItems();
		if (SelectedItems.Num() > 0)
		{
			OnSelectionChanged_Internal(SelectedItems[0], ESelectInfo::Direct);
		}
	}
	else
	{
		SearchField->SetText(FText::GetEmpty());
		OnComboBoxOpening.ExecuteIfBound();
	}

	return SComboButton::OnButtonClicked();
}

void SSearchableTreeCombobox::OnSearchTextChanged(const FText& ChangedText)
{
	SearchText = ChangedText;
;	RefreshOptions();
	for (TSharedPtr<FPythonTreeNode> Root : FilteredOptionsSource)
	{
		ExpandAllNode(Root);
	}
	MyTreeView->RequestTreeRefresh();
}

void SSearchableTreeCombobox::OnGetChildren(TSharedPtr<FPythonTreeNode> InItem, TArray<TSharedPtr<FPythonTreeNode>>& OutChildren)
{
	InItem->GetChildren(OutChildren);
}

TSharedRef<ITableRow> SSearchableTreeCombobox::OnGenerateRow(TSharedPtr<FPythonTreeNode> InItem, const TSharedRef<STableViewBase>& OwnerTable)
{
	//return SNew(STableRow<TSharedPtr<FPythonTreeNode>>, OwnerTable)
	//	//.Style(FAppStyle::Get(), "PlacementBrowser.PlaceableItemRow")
	//	[
	//		SNew(STextBlock)
	//			.Text(FText::FromString(InItem->GetName()))
	//	];
	return SNew(SPythonListRow, OwnerTable)
		.Item(InItem);
	
}

void SSearchableTreeCombobox::RefreshOptions()
{
	FilteredOptionsSource.Reset();

	if (SearchText.IsEmpty())
	{

		for (auto& Root : *OptionsSource)
		{
			FilteredOptionsSource.Add(Root);
		}
	}
	else
	{
		FString Filter = SearchText.ToString();

		for (TSharedPtr<FPythonTreeNode> Root : *OptionsSource)
		{
			TSharedPtr<FPythonTreeNode> Result = RebuildTree(Root, Filter);

			if (Result.IsValid())
			{
				FilteredOptionsSource.Add(Result);
			}
		}
	}
	MyTreeView->RequestTreeRefresh();
}

void SSearchableTreeCombobox::RebuildTreeByFilterText(TSharedPtr<FPythonTreeNode> ParentNode, const FString& InFilter)
{
}

void SSearchableTreeCombobox::OnSearchTextCommitted(const FText& InText, ETextCommit::Type InCommitType)
{
	if ((InCommitType == ETextCommit::Type::OnEnter) && FilteredOptionsSource.Num() > 0)
	{
		MyTreeView->SetSelection(FilteredOptionsSource[0], ESelectInfo::OnKeyPress);
	}
}

void SSearchableTreeCombobox::IsShouldVisible(TSharedPtr<FPythonTreeNode> InItem)
{

}

void SSearchableTreeCombobox::OnSelectionChanged_Internal(TSharedPtr<FPythonTreeNode> ProposedSelection, ESelectInfo::Type SelectInfo)
{
	if (!ProposedSelection)
	{
		return;
	}
	if (ProposedSelection->GetNodeType() == EPythonTreeNodeType::CATEGORY)
	{
		MyTreeView->ClearSelection();
		return;
	}
	// Ensure that the proposed selection is different from selected
	if (ProposedSelection != SelectedItem || bAlwaysSelectItem)
	{
		SelectedItem = ProposedSelection;
		OnSelectionChanged.ExecuteIfBound(ProposedSelection, SelectInfo);
	}

	// close combo as long as the selection wasn't from navigation
	if (SelectInfo != ESelectInfo::OnNavigation)
	{
		this->SetIsOpen(false);
	}
	else
	{
		MyTreeView->RequestScrollIntoView(SelectedItem, 0);
	}
}

FReply SSearchableTreeCombobox::OnKeyDownHandler(const FGeometry& MyGeometry, const FKeyEvent& InKeyEvent)
{
	if (InKeyEvent.GetKey() == EKeys::Enter)
	{
		// Select the first selected item on hitting enter
		TArray<TSharedPtr<FPythonTreeNode>> SelectedItems = MyTreeView->GetSelectedItems();
		if (SelectedItems.Num() > 0)
		{
			OnSelectionChanged_Internal(SelectedItems[0], ESelectInfo::OnKeyPress);
			return FReply::Handled();
		}
	}

	return FReply::Unhandled();
}

TSharedPtr<FPythonTreeNode> SSearchableTreeCombobox::GetSelectedItem()
{

	return SelectedItem;
}

TSharedPtr<FPythonTreeNode> SSearchableTreeCombobox::RebuildTree(TSharedPtr<FPythonTreeNode> Node, const FString& FilterText)
{
	
	TArray<TSharedPtr<FPythonTreeNode>> ChildList;
	Node->GetChildren(ChildList);

	TArray<TSharedPtr<FPythonTreeNode>> FilteredChildren;

	for (auto& Child : ChildList)
	{
		TSharedPtr<FPythonTreeNode> FilteredChild = RebuildTree(Child, FilterText);

		// 子树有效 → 添加
		if (FilteredChild.IsValid())
		{
			FilteredChildren.Add(FilteredChild);
		}
	}

	const bool bIsEntity = Node->GetNodeType() == EPythonTreeNodeType::ENTITY;

	if (bIsEntity)
	{

		if (FilterText.IsEmpty() || Node->GetName().Find(FilterText, ESearchCase::Type::IgnoreCase) != INDEX_NONE || 
			Node->GetID().Find(FilterText, ESearchCase::Type::IgnoreCase) != INDEX_NONE || 
			Node->GetID().Find(FilterText, ESearchCase::Type::IgnoreCase) != INDEX_NONE)
		{
			return FPythonTreeNode::Make(Node);
		}
		else
		{
			return nullptr;
		}
	}

	// ------------------------------
	// CATEGORY 节点过滤规则
	// ------------------------------
	// CATEGORY 显示条件：有子节点通过过滤
	if (FilteredChildren.Num() > 0)
	{
		TSharedPtr<FPythonTreeNode> NewNode = FPythonTreeNode::Make(Node);
		for (TSharedPtr<FPythonTreeNode> i : FilteredChildren)
		{
			NewNode->AddChild(i.ToSharedRef());
		}
		return NewNode;
	}

	// CATEGORY 下所有子节点都没通过 → 隐藏
	return nullptr;

}

void SSearchableTreeCombobox::ExpandAllNode(TSharedPtr<FPythonTreeNode> InNode)
{
	TArray<TSharedPtr<FPythonTreeNode>> ChildList;
	InNode->GetChildren(ChildList);
	for (TSharedPtr<FPythonTreeNode> Child : ChildList)
	{
		MyTreeView->SetItemExpansion(Child, true);
		ExpandAllNode(Child);
	}
	MyTreeView->SetItemExpansion(InNode, true);
}

void SSearchableTreeCombobox::OnMenuOpenChanged(bool bOpen)
{
	if (bOpen == false)
	{
		if (TListTypeTraits<TSharedPtr<FPythonTreeNode>>::IsPtrValid(SelectedItem))
		{
			// Ensure the ListView selection is set back to the last committed selection
			MyTreeView->SetSelection(SelectedItem, ESelectInfo::OnNavigation);
		}

		// Set focus back to ComboBox for users focusing the ListView that just closed
		FSlateApplication::Get().ForEachUser([this](FSlateUser& User)
		{
			TSharedRef<SWidget> ThisRef = this->AsShared();
			if (User.IsWidgetInFocusPath(MyTreeView))
			{
				User.SetFocus(ThisRef);
			}
		});

	}
}

void SPythonListRow::Construct(const FArguments& InArgs, const TSharedRef<STableViewBase>& InOwnerTableView)
{
	Item = InArgs._Item;
	SMultiColumnTableRow<TSharedPtr<FPythonTreeNode>>::Construct(FSuperRowType::FArguments(), InOwnerTableView);
}

TSharedRef<SWidget> SPythonListRow::GenerateWidgetForColumn(const FName& InColumnName)
{
	if (!Item.IsValid())
	{
		return SNew(STextBlock)
			.Text(FText::FromString(TEXT("Invalid Item")));
	}
	else
	{
		if (InColumnName.IsEqual((TEXT("Name"))))
		{

			return SNew(SHorizontalBox)
				+ SHorizontalBox::Slot()
				.AutoWidth()
				.Padding(6, 0, 0, 0)
				[
					SNew(SExpanderArrow, SharedThis(this))
				]
				+ SHorizontalBox::Slot()
				.FillWidth(1.0f)
				[
					SNew(SBox)
					.HeightOverride(28)
					.VAlign(VAlign_Center)
					[
						SNew(STextBlock)
							.Text(FText::FromString(Item->GetName()))
					]
				];
		}
		else if (InColumnName.IsEqual(TEXT("ID")))
		{
			return SNew(SBox)
				.HeightOverride(28)
				.VAlign(VAlign_Center)
				[
					SNew(STextBlock)
					.Text(FText::FromString(Item->GetID()))
				];
		}
		else if (InColumnName.IsEqual(TEXT("Plot")))
		{
			return SNew(SBox)
				.HeightOverride(28)
				.VAlign(VAlign_Center)
				[
					SNew(STextBlock)
						.Text(FText::FromString(Item->GetPlot()))
				];
		}
	}

	return SNew(STextBlock)
		.Text(FText::FromString(TEXT("Invalid Field")));
}
