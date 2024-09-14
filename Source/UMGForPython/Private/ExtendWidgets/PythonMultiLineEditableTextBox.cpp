#include "ExtendWidgets/PythonMultiLineEditableTextBox.h"

TSharedRef<SWidget> PythonMultiLineEditableTextBox::RebuildWidget()
{
	MyEditableTextBlock = SNew(SMultiLineEditableTextBox);
	return MyEditableTextBlock.ToSharedRef();
}

void PythonMultiLineEditableTextBox::SynchronizeProperties()
{
}
