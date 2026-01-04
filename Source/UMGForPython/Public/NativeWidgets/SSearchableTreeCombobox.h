#pragma once
#include "CoreMinimal.h"
#include "Widgets/Views/STreeView.h"
#include "Components/Widget.h"
#include "Widgets/Input/SComboButton.h"

enum EPythonTreeNodeType
{
	ENTITY,
	CATEGORY
};
class FPythonTreeNode
{
public:

	static TSharedRef<FPythonTreeNode> Make(const FString& InName, const FString& InID, const FString& InPlot)
	{
		return MakeShareable(new FPythonTreeNode(InName, InID, InPlot));
	}

	static TSharedRef<FPythonTreeNode> Make(TSharedPtr<FPythonTreeNode> InNode)
	{

		return MakeShareable(new FPythonTreeNode(InNode->GetName(), InNode->GetID(), InNode->GetPlot(), InNode->GetNodeType()));
	}

	FPythonTreeNode(const FString& InName)
	{
		Name = InName;
	}

	FPythonTreeNode(const FString& InName, const FString& InNodeType)
	{
		Name = InName;
		SetNodeType(InNodeType);
	}

	FPythonTreeNode(const FString& InName, EPythonTreeNodeType InNodeType)
	{
		Name = InName;
		SetNodeType(InNodeType);
	}
	FPythonTreeNode(const FString& InName, const FString& InID, const FString& InPlot)
	{
		Name = InName;
		ID = InID;
		Plot = InPlot;
	}

	FPythonTreeNode(const FString& InName, const FString& InID, const FString& InPlot, EPythonTreeNodeType InNodeType)
	{	
		Name = InName;
		ID = InID;
		Plot = InPlot;
		NodeType = InNodeType;
	}

	~FPythonTreeNode()
	{

	}
	void GetChildren(TArray< TSharedPtr<FPythonTreeNode> >& OutChildren)
	{
		OutChildren = Children;
	}

	void AddChild(TSharedRef<FPythonTreeNode> InChild)
	{
		Children.Add(InChild);
	}

	FString GetName()
	{
		return Name;
	}

	FString GetID()
	{
		return ID;
	}

	FString GetPlot()
	{
		return Plot;
	}

	void SetNodeType(EPythonTreeNodeType InType)
	{
		NodeType = InType;
	}

	void SetNodeType(FString InType)
	{
		if (InType == "ENTITY")
		{
			NodeType = EPythonTreeNodeType::ENTITY;
		}
		else if (InType == "CATEGORY")
		{
			NodeType = EPythonTreeNodeType::CATEGORY;
		}
	}

	EPythonTreeNodeType GetNodeType() const
	{
		return NodeType;
	}

	EVisibility GetVisibility() const
	{
		return Visibility;
	}

	void SetVisibility(EVisibility InVisibility)
	{
		Visibility = InVisibility;
	}	
private:
	TArray< TSharedPtr<FPythonTreeNode> > Children;
	FString Name;
	FString ID;
	FString Plot;
	EPythonTreeNodeType NodeType;
	EVisibility Visibility;
};
class SSearchableTreeCombobox : public SComboButton
{
public:

	typedef typename TSlateDelegates< TSharedPtr<FPythonTreeNode> >::FOnGenerateWidget FOnGenerateWidget;
	typedef typename TSlateDelegates< TSharedPtr<FPythonTreeNode> >::FOnSelectionChanged FOnSelectionChanged;

	SLATE_BEGIN_ARGS(SSearchableTreeCombobox)
		: _Content()
		, _ComboBoxStyle(&FAppStyle::Get().GetWidgetStyle<FComboBoxStyle>("ComboBox"))
		, _ButtonStyle(nullptr)
		, _ItemStyle(&FAppStyle::Get().GetWidgetStyle<FTableRowStyle>("ComboBox.Row"))
		, _ContentPadding(_ComboBoxStyle->ContentPadding)
		, _ForegroundColor(FSlateColor::UseStyle())
		, _OptionsSource()
		, _OnSelectionChanged()
		, _bAlwaysSelectItem(false)
		, _OnGenerateWidget()
		, _InitiallySelectedItem(nullptr)
		, _MaxHeight(800.0f)
		, _HasDownArrow(true)
		, _SearchVisibility()
		{
		}

		/** Slot for this button's content (optional) */
		SLATE_DEFAULT_SLOT(FArguments, Content)

		SLATE_STYLE_ARGUMENT(FComboBoxStyle, ComboBoxStyle)

		/** The visual style of the button part of the combo box (overrides ComboBoxStyle) */
		SLATE_STYLE_ARGUMENT(FButtonStyle, ButtonStyle)

		SLATE_STYLE_ARGUMENT(FTableRowStyle, ItemStyle)

		SLATE_ATTRIBUTE(FMargin, ContentPadding)
		SLATE_ATTRIBUTE(FSlateColor, ForegroundColor)

		SLATE_ARGUMENT(const TArray< TSharedPtr<FPythonTreeNode> >*, OptionsSource)
		SLATE_EVENT(FOnSelectionChanged, OnSelectionChanged)
		SLATE_ARGUMENT(bool, bAlwaysSelectItem)
		SLATE_EVENT(FOnGenerateWidget, OnGenerateWidget)

		/** Called when combo box is opened, before list is actually created */
		SLATE_EVENT(FOnComboBoxOpening, OnComboBoxOpening)

		/** The custom scrollbar to use in the ListView */
		SLATE_ARGUMENT(TSharedPtr<SScrollBar>, CustomScrollbar)

		/** The option that should be selected when the combo box is first created */
		SLATE_ARGUMENT(TSharedPtr<FString>, InitiallySelectedItem)

		/** The max height of the combo box menu */
		SLATE_ARGUMENT(float, MaxHeight)

		/**
		 * When false, the down arrow is not generated and it is up to the API consumer
		 * to make their own visual hint that this is a drop down.
		 */
		SLATE_ARGUMENT(bool, HasDownArrow)

		/** Allow setting the visibility of the search box dynamically */
		SLATE_ATTRIBUTE(EVisibility, SearchVisibility)

	SLATE_END_ARGS()

public:

	void Construct(const FArguments& InArgs);

	virtual FReply OnButtonClicked() override;

public:
	void OnSearchTextChanged(const FText& ChangedText);
	void OnGetChildren(TSharedPtr<FPythonTreeNode> InItem, TArray<TSharedPtr<FPythonTreeNode>>& OutChildren);
	TSharedRef<ITableRow> OnGenerateRow(TSharedPtr<FPythonTreeNode> InItem, const TSharedRef<STableViewBase>& OwnerTable);
	void RefreshOptions();
	void RebuildTreeByFilterText(TSharedPtr<FPythonTreeNode> ParentNode, const FString& InFilter);
	void OnSearchTextCommitted(const FText& InText, ETextCommit::Type InCommitType);
	void IsShouldVisible(TSharedPtr<FPythonTreeNode> InItem);
	void OnSelectionChanged_Internal(TSharedPtr<FPythonTreeNode> ProposedSelection, ESelectInfo::Type SelectInfo);
	FReply OnKeyDownHandler(const FGeometry& MyGeometry, const FKeyEvent& InKeyEvent);
	TSharedPtr<FPythonTreeNode> GetSelectedItem();
	TSharedPtr<FPythonTreeNode> RebuildTree(TSharedPtr<FPythonTreeNode> InNode, const FString& FilterText);
	void ExpandAllNode(TSharedPtr<FPythonTreeNode> InNode);
	void OnMenuOpenChanged(bool bOpen);
private:
	TSharedPtr<SEditableTextBox> SearchField;
	FOnSelectionChanged OnSelectionChanged;
	TSharedPtr<FPythonTreeNode> SelectedItem;
	TSharedPtr<STreeView<TSharedPtr<FPythonTreeNode>>> MyTreeView;
	const TArray<TSharedPtr<FPythonTreeNode>>* OptionsSource;
	TArray<TSharedPtr<FPythonTreeNode>> FilteredOptionsSource;
	FText SearchText;
	bool bAlwaysSelectItem;
	FOnComboBoxOpening OnComboBoxOpening;
	TSharedPtr< SScrollBar > CustomScrollbar;
};


class SPythonListRow : public SMultiColumnTableRow<TSharedPtr<FPythonTreeNode>>
{
public:
	SLATE_BEGIN_ARGS(SPythonListRow)
		{
		}
		SLATE_ARGUMENT(TSharedPtr<FPythonTreeNode>, Item)

	SLATE_END_ARGS()

	void Construct(const FArguments& InArgs, const TSharedRef<STableViewBase>& InOwnerTableView);
	virtual TSharedRef<SWidget> GenerateWidgetForColumn(const FName& InColumnName);

private:
	TSharedPtr<FPythonTreeNode> Item;
};