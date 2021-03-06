void AddText(int length, const char* text, BOOL bDirect);
void AddStyledText(int length, char* c, BOOL bDirect);
void InsertText(long pos, const char* text, BOOL bDirect);
void ClearAll(BOOL bDirect);
void DeleteRange(long pos, int deleteLength, BOOL bDirect);
void ClearDocumentStyle(BOOL bDirect);
int GetLength(BOOL bDirect);
int GetCharAt(long pos, BOOL bDirect);
long GetCurrentPos(BOOL bDirect);
long GetAnchor(BOOL bDirect);
int GetStyleAt(long pos, BOOL bDirect);
void Redo(BOOL bDirect);
void SetUndoCollection(BOOL collectUndo, BOOL bDirect);
void SelectAll(BOOL bDirect);
void SetSavePoint(BOOL bDirect);
int GetStyledText(TextRange* tr, BOOL bDirect);
BOOL CanRedo(BOOL bDirect);
int MarkerLineFromHandle(int handle, BOOL bDirect);
void MarkerDeleteHandle(int handle, BOOL bDirect);
BOOL GetUndoCollection(BOOL bDirect);
int GetViewWS(BOOL bDirect);
void SetViewWS(int viewWS, BOOL bDirect);
long PositionFromPoint(int x, int y, BOOL bDirect);
long PositionFromPointClose(int x, int y, BOOL bDirect);
void GotoLine(int line, BOOL bDirect);
void GotoPos(long pos, BOOL bDirect);
void SetAnchor(long posAnchor, BOOL bDirect);
int GetCurLine(int length, char* text, BOOL bDirect);
long GetEndStyled(BOOL bDirect);
void ConvertEOLs(int eolMode, BOOL bDirect);
int GetEOLMode(BOOL bDirect);
void SetEOLMode(int eolMode, BOOL bDirect);
void StartStyling(long pos, int mask, BOOL bDirect);
void SetStyling(int length, int style, BOOL bDirect);
BOOL GetBufferedDraw(BOOL bDirect);
void SetBufferedDraw(BOOL buffered, BOOL bDirect);
void SetTabWidth(int tabWidth, BOOL bDirect);
int GetTabWidth(BOOL bDirect);
void SetCodePage(int codePage, BOOL bDirect);
void MarkerDefine(int markerNumber, int markerSymbol, BOOL bDirect);
void MarkerSetFore(int markerNumber, COLORREF fore, BOOL bDirect);
void MarkerSetBack(int markerNumber, COLORREF back, BOOL bDirect);
void MarkerSetBackSelected(int markerNumber, COLORREF back, BOOL bDirect);
void MarkerEnableHighlight(BOOL enabled, BOOL bDirect);
int MarkerAdd(int line, int markerNumber, BOOL bDirect);
void MarkerDelete(int line, int markerNumber, BOOL bDirect);
void MarkerDeleteAll(int markerNumber, BOOL bDirect);
int MarkerGet(int line, BOOL bDirect);
int MarkerNext(int lineStart, int markerMask, BOOL bDirect);
int MarkerPrevious(int lineStart, int markerMask, BOOL bDirect);
void MarkerDefinePixmap(int markerNumber, const char* pixmap, BOOL bDirect);
void MarkerAddSet(int line, int set, BOOL bDirect);
void MarkerSetAlpha(int markerNumber, int alpha, BOOL bDirect);
void SetMarginTypeN(int margin, int marginType, BOOL bDirect);
int GetMarginTypeN(int margin, BOOL bDirect);
void SetMarginWidthN(int margin, int pixelWidth, BOOL bDirect);
int GetMarginWidthN(int margin, BOOL bDirect);
void SetMarginMaskN(int margin, int mask, BOOL bDirect);
int GetMarginMaskN(int margin, BOOL bDirect);
void SetMarginSensitiveN(int margin, BOOL sensitive, BOOL bDirect);
BOOL GetMarginSensitiveN(int margin, BOOL bDirect);
void SetMarginCursorN(int margin, int cursor, BOOL bDirect);
int GetMarginCursorN(int margin, BOOL bDirect);
void StyleClearAll(BOOL bDirect);
void StyleSetFore(int style, COLORREF fore, BOOL bDirect);
void StyleSetBack(int style, COLORREF back, BOOL bDirect);
void StyleSetBold(int style, BOOL bold, BOOL bDirect);
void StyleSetItalic(int style, BOOL italic, BOOL bDirect);
void StyleSetSize(int style, int sizePoints, BOOL bDirect);
void StyleSetFont(int style, const char* fontName, BOOL bDirect);
void StyleSetEOLFilled(int style, BOOL filled, BOOL bDirect);
void StyleResetDefault(BOOL bDirect);
void StyleSetUnderline(int style, BOOL underline, BOOL bDirect);
COLORREF StyleGetFore(int style, BOOL bDirect);
COLORREF StyleGetBack(int style, BOOL bDirect);
BOOL StyleGetBold(int style, BOOL bDirect);
BOOL StyleGetItalic(int style, BOOL bDirect);
int StyleGetSize(int style, BOOL bDirect);
int StyleGetFont(int style, char* fontName, BOOL bDirect);
BOOL StyleGetEOLFilled(int style, BOOL bDirect);
BOOL StyleGetUnderline(int style, BOOL bDirect);
int StyleGetCase(int style, BOOL bDirect);
int StyleGetCharacterSet(int style, BOOL bDirect);
BOOL StyleGetVisible(int style, BOOL bDirect);
BOOL StyleGetChangeable(int style, BOOL bDirect);
BOOL StyleGetHotSpot(int style, BOOL bDirect);
void StyleSetCase(int style, int caseForce, BOOL bDirect);
void StyleSetSizeFractional(int style, int sizeInHundredthPoints, BOOL bDirect);
int StyleGetSizeFractional(int style, BOOL bDirect);
void StyleSetWeight(int style, int weight, BOOL bDirect);
int StyleGetWeight(int style, BOOL bDirect);
void StyleSetCharacterSet(int style, int characterSet, BOOL bDirect);
void StyleSetHotSpot(int style, BOOL hotspot, BOOL bDirect);
void SetSelFore(BOOL useSetting, COLORREF fore, BOOL bDirect);
void SetSelBack(BOOL useSetting, COLORREF back, BOOL bDirect);
int GetSelAlpha(BOOL bDirect);
void SetSelAlpha(int alpha, BOOL bDirect);
BOOL GetSelEOLFilled(BOOL bDirect);
void SetSelEOLFilled(BOOL filled, BOOL bDirect);
void SetCaretFore(COLORREF fore, BOOL bDirect);
void AssignCmdKey(DWORD km, int msg, BOOL bDirect);
void ClearCmdKey(DWORD km, BOOL bDirect);
void ClearAllCmdKeys(BOOL bDirect);
void SetStylingEx(int length, const char* styles, BOOL bDirect);
void StyleSetVisible(int style, BOOL visible, BOOL bDirect);
int GetCaretPeriod(BOOL bDirect);
void SetCaretPeriod(int periodMilliseconds, BOOL bDirect);
void SetWordChars(const char* characters, BOOL bDirect);
int GetWordChars(char* characters, BOOL bDirect);
void BeginUndoAction(BOOL bDirect);
void EndUndoAction(BOOL bDirect);
void IndicSetStyle(int indic, int style, BOOL bDirect);
int IndicGetStyle(int indic, BOOL bDirect);
void IndicSetFore(int indic, COLORREF fore, BOOL bDirect);
COLORREF IndicGetFore(int indic, BOOL bDirect);
void IndicSetUnder(int indic, BOOL under, BOOL bDirect);
BOOL IndicGetUnder(int indic, BOOL bDirect);
void SetWhitespaceFore(BOOL useSetting, COLORREF fore, BOOL bDirect);
void SetWhitespaceBack(BOOL useSetting, COLORREF back, BOOL bDirect);
void SetWhitespaceSize(int size, BOOL bDirect);
int GetWhitespaceSize(BOOL bDirect);
void SetStyleBits(int bits, BOOL bDirect);
int GetStyleBits(BOOL bDirect);
void SetLineState(int line, int state, BOOL bDirect);
int GetLineState(int line, BOOL bDirect);
int GetMaxLineState(BOOL bDirect);
BOOL GetCaretLineVisible(BOOL bDirect);
void SetCaretLineVisible(BOOL show, BOOL bDirect);
COLORREF GetCaretLineBack(BOOL bDirect);
void SetCaretLineBack(COLORREF back, BOOL bDirect);
void StyleSetChangeable(int style, BOOL changeable, BOOL bDirect);
void AutoCShow(int lenEntered, const char* itemList, BOOL bDirect);
void AutoCCancel(BOOL bDirect);
BOOL AutoCActive(BOOL bDirect);
long AutoCPosStart(BOOL bDirect);
void AutoCComplete(BOOL bDirect);
void AutoCStops(const char* characterSet, BOOL bDirect);
void AutoCSetSeparator(int separatorCharacter, BOOL bDirect);
int AutoCGetSeparator(BOOL bDirect);
void AutoCSelect(const char* text, BOOL bDirect);
void AutoCSetCancelAtStart(BOOL cancel, BOOL bDirect);
BOOL AutoCGetCancelAtStart(BOOL bDirect);
void AutoCSetFillUps(const char* characterSet, BOOL bDirect);
void AutoCSetChooseSingle(BOOL chooseSingle, BOOL bDirect);
BOOL AutoCGetChooseSingle(BOOL bDirect);
void AutoCSetIgnoreCase(BOOL ignoreCase, BOOL bDirect);
BOOL AutoCGetIgnoreCase(BOOL bDirect);
void UserListShow(int listType, const char* itemList, BOOL bDirect);
void AutoCSetAutoHide(BOOL autoHide, BOOL bDirect);
BOOL AutoCGetAutoHide(BOOL bDirect);
void AutoCSetDropRestOfWord(BOOL dropRestOfWord, BOOL bDirect);
BOOL AutoCGetDropRestOfWord(BOOL bDirect);
void RegisterImage(int type, const char* xpmData, BOOL bDirect);
void ClearRegisteredImages(BOOL bDirect);
int AutoCGetTypeSeparator(BOOL bDirect);
void AutoCSetTypeSeparator(int separatorCharacter, BOOL bDirect);
void AutoCSetMaxWidth(int characterCount, BOOL bDirect);
int AutoCGetMaxWidth(BOOL bDirect);
void AutoCSetMaxHeight(int rowCount, BOOL bDirect);
int AutoCGetMaxHeight(BOOL bDirect);
void SetIndent(int indentSize, BOOL bDirect);
int GetIndent(BOOL bDirect);
void SetUseTabs(BOOL useTabs, BOOL bDirect);
BOOL GetUseTabs(BOOL bDirect);
void SetLineIndentation(int line, int indentSize, BOOL bDirect);
int GetLineIndentation(int line, BOOL bDirect);
long GetLineIndentPosition(int line, BOOL bDirect);
int GetColumn(long pos, BOOL bDirect);
int CountCharacters(int startPos, int endPos, BOOL bDirect);
void SetHScrollBar(BOOL show, BOOL bDirect);
BOOL GetHScrollBar(BOOL bDirect);
void SetIndentationGuides(int indentView, BOOL bDirect);
int GetIndentationGuides(BOOL bDirect);
void SetHighlightGuide(int column, BOOL bDirect);
int GetHighlightGuide(BOOL bDirect);
long GetLineEndPosition(int line, BOOL bDirect);
int GetCodePage(BOOL bDirect);
COLORREF GetCaretFore(BOOL bDirect);
BOOL GetReadOnly(BOOL bDirect);
void SetCurrentPos(long pos, BOOL bDirect);
void SetSelectionStart(long pos, BOOL bDirect);
long GetSelectionStart(BOOL bDirect);
void SetSelectionEnd(long pos, BOOL bDirect);
long GetSelectionEnd(BOOL bDirect);
void SetEmptySelection(long pos, BOOL bDirect);
void SetPrintMagnification(int magnification, BOOL bDirect);
int GetPrintMagnification(BOOL bDirect);
void SetPrintColourMode(int mode, BOOL bDirect);
int GetPrintColourMode(BOOL bDirect);
long FindText(int flags, TextToFind* ft, BOOL bDirect);
long FormatRange(BOOL draw, RangeToFormat* fr, BOOL bDirect);
int GetFirstVisibleLine(BOOL bDirect);
int GetLine(int line, char* text, BOOL bDirect);
int GetLineCount(BOOL bDirect);
void SetMarginLeft(int pixelWidth, BOOL bDirect);
int GetMarginLeft(BOOL bDirect);
void SetMarginRight(int pixelWidth, BOOL bDirect);
int GetMarginRight(BOOL bDirect);
BOOL GetModify(BOOL bDirect);
void SetSel(long start, long end, BOOL bDirect);
int GetSelText(char* text, BOOL bDirect);
int GetTextRange(TextRange* tr, BOOL bDirect);
void HideSelection(BOOL normal, BOOL bDirect);
int PointXFromPosition(long pos, BOOL bDirect);
int PointYFromPosition(long pos, BOOL bDirect);
int LineFromPosition(long pos, BOOL bDirect);
long PositionFromLine(int line, BOOL bDirect);
void LineScroll(int columns, int lines, BOOL bDirect);
void ScrollCaret(BOOL bDirect);
void ScrollRange(long secondary, long primary, BOOL bDirect);
void ReplaceSel(const char* text, BOOL bDirect);
void SetReadOnly(BOOL readOnly, BOOL bDirect);
void Null(BOOL bDirect);
BOOL CanPaste(BOOL bDirect);
BOOL CanUndo(BOOL bDirect);
void EmptyUndoBuffer(BOOL bDirect);
void Undo(BOOL bDirect);
void Cut(BOOL bDirect);
void Copy(BOOL bDirect);
void Paste(BOOL bDirect);
void Clear(BOOL bDirect);
void SetText(const char* text, BOOL bDirect);
int GetText(int length, char* text, BOOL bDirect);
int GetTextLength(BOOL bDirect);
void SetOvertype(BOOL overtype, BOOL bDirect);
BOOL GetOvertype(BOOL bDirect);
void SetCaretWidth(int pixelWidth, BOOL bDirect);
int GetCaretWidth(BOOL bDirect);
void SetTargetStart(long pos, BOOL bDirect);
long GetTargetStart(BOOL bDirect);
void SetTargetEnd(long pos, BOOL bDirect);
long GetTargetEnd(BOOL bDirect);
int ReplaceTarget(int length, const char* text, BOOL bDirect);
int ReplaceTargetRE(int length, const char* text, BOOL bDirect);
int SearchInTarget(int length, const char* text, BOOL bDirect);
void SetSearchFlags(int flags, BOOL bDirect);
int GetSearchFlags(BOOL bDirect);
void CallTipShow(long pos, const char* definition, BOOL bDirect);
void CallTipCancel(BOOL bDirect);
BOOL CallTipActive(BOOL bDirect);
long CallTipPosStart(BOOL bDirect);
void CallTipSetHlt(int start, int end, BOOL bDirect);
void CallTipSetBack(COLORREF back, BOOL bDirect);
void CallTipSetFore(COLORREF fore, BOOL bDirect);
void CallTipSetForeHlt(COLORREF fore, BOOL bDirect);
void CallTipUseStyle(int tabSize, BOOL bDirect);
void CallTipSetPosition(BOOL above, BOOL bDirect);
int VisibleFromDocLine(int line, BOOL bDirect);
int DocLineFromVisible(int lineDisplay, BOOL bDirect);
int WrapCount(int line, BOOL bDirect);
void SetFoldLevel(int line, int level, BOOL bDirect);
int GetFoldLevel(int line, BOOL bDirect);
int GetLastChild(int line, int level, BOOL bDirect);
int GetFoldParent(int line, BOOL bDirect);
void ShowLines(int lineStart, int lineEnd, BOOL bDirect);
void HideLines(int lineStart, int lineEnd, BOOL bDirect);
BOOL GetLineVisible(int line, BOOL bDirect);
BOOL GetAllLinesVisible(BOOL bDirect);
void SetFoldExpanded(int line, BOOL expanded, BOOL bDirect);
BOOL GetFoldExpanded(int line, BOOL bDirect);
void ToggleFold(int line, BOOL bDirect);
void FoldLine(int line, int action, BOOL bDirect);
void FoldChildren(int line, int action, BOOL bDirect);
void ExpandChildren(int line, int level, BOOL bDirect);
void FoldAll(int action, BOOL bDirect);
void EnsureVisible(int line, BOOL bDirect);
void SetAutomaticFold(int automaticFold, BOOL bDirect);
int GetAutomaticFold(BOOL bDirect);
void SetFoldFlags(int flags, BOOL bDirect);
void EnsureVisibleEnforcePolicy(int line, BOOL bDirect);
void SetTabIndents(BOOL tabIndents, BOOL bDirect);
BOOL GetTabIndents(BOOL bDirect);
void SetBackSpaceUnIndents(BOOL bsUnIndents, BOOL bDirect);
BOOL GetBackSpaceUnIndents(BOOL bDirect);
void SetMouseDwellTime(int periodMilliseconds, BOOL bDirect);
int GetMouseDwellTime(BOOL bDirect);
int WordStartPosition(long pos, BOOL onlyWordCharacters, BOOL bDirect);
int WordEndPosition(long pos, BOOL onlyWordCharacters, BOOL bDirect);
void SetWrapMode(int mode, BOOL bDirect);
int GetWrapMode(BOOL bDirect);
void SetWrapVisualFlags(int wrapVisualFlags, BOOL bDirect);
int GetWrapVisualFlags(BOOL bDirect);
void SetWrapVisualFlagsLocation(int wrapVisualFlagsLocation, BOOL bDirect);
int GetWrapVisualFlagsLocation(BOOL bDirect);
void SetWrapStartIndent(int indent, BOOL bDirect);
int GetWrapStartIndent(BOOL bDirect);
void SetWrapIndentMode(int mode, BOOL bDirect);
int GetWrapIndentMode(BOOL bDirect);
void SetLayoutCache(int mode, BOOL bDirect);
int GetLayoutCache(BOOL bDirect);
void SetScrollWidth(int pixelWidth, BOOL bDirect);
int GetScrollWidth(BOOL bDirect);
void SetScrollWidthTracking(BOOL tracking, BOOL bDirect);
BOOL GetScrollWidthTracking(BOOL bDirect);
int TextWidth(int style, const char* text, BOOL bDirect);
void SetEndAtLastLine(BOOL endAtLastLine, BOOL bDirect);
BOOL GetEndAtLastLine(BOOL bDirect);
int TextHeight(int line, BOOL bDirect);
void SetVScrollBar(BOOL show, BOOL bDirect);
BOOL GetVScrollBar(BOOL bDirect);
void AppendText(int length, const char* text, BOOL bDirect);
BOOL GetTwoPhaseDraw(BOOL bDirect);
void SetTwoPhaseDraw(BOOL twoPhase, BOOL bDirect);
void SetFontQuality(int fontQuality, BOOL bDirect);
int GetFontQuality(BOOL bDirect);
void SetFirstVisibleLine(int lineDisplay, BOOL bDirect);
void SetMultiPaste(int multiPaste, BOOL bDirect);
int GetMultiPaste(BOOL bDirect);
int GetTag(int tagNumber, char* tagValue, BOOL bDirect);
void TargetFromSelection(BOOL bDirect);
void LinesJoin(BOOL bDirect);
void LinesSplit(int pixelWidth, BOOL bDirect);
void SetFoldMarginColour(BOOL useSetting, COLORREF back, BOOL bDirect);
void SetFoldMarginHiColour(BOOL useSetting, COLORREF fore, BOOL bDirect);
void LineDown(BOOL bDirect);
void LineDownExtend(BOOL bDirect);
void LineUp(BOOL bDirect);
void LineUpExtend(BOOL bDirect);
void CharLeft(BOOL bDirect);
void CharLeftExtend(BOOL bDirect);
void CharRight(BOOL bDirect);
void CharRightExtend(BOOL bDirect);
void WordLeft(BOOL bDirect);
void WordLeftExtend(BOOL bDirect);
void WordRight(BOOL bDirect);
void WordRightExtend(BOOL bDirect);
void Home(BOOL bDirect);
void HomeExtend(BOOL bDirect);
void LineEnd(BOOL bDirect);
void LineEndExtend(BOOL bDirect);
void DocumentStart(BOOL bDirect);
void DocumentStartExtend(BOOL bDirect);
void DocumentEnd(BOOL bDirect);
void DocumentEndExtend(BOOL bDirect);
void PageUp(BOOL bDirect);
void PageUpExtend(BOOL bDirect);
void PageDown(BOOL bDirect);
void PageDownExtend(BOOL bDirect);
void EditToggleOvertype(BOOL bDirect);
void Cancel(BOOL bDirect);
void DeleteBack(BOOL bDirect);
void Tab(BOOL bDirect);
void BackTab(BOOL bDirect);
void NewLine(BOOL bDirect);
void FormFeed(BOOL bDirect);
void VCHome(BOOL bDirect);
void VCHomeExtend(BOOL bDirect);
void ZoomIn(BOOL bDirect);
void ZoomOut(BOOL bDirect);
void DelWordLeft(BOOL bDirect);
void DelWordRight(BOOL bDirect);
void DelWordRightEnd(BOOL bDirect);
void LineCut(BOOL bDirect);
void LineDelete(BOOL bDirect);
void LineTranspose(BOOL bDirect);
void LineDuplicate(BOOL bDirect);
void LowerCase(BOOL bDirect);
void UpperCase(BOOL bDirect);
void LineScrollDown(BOOL bDirect);
void LineScrollUp(BOOL bDirect);
void DeleteBackNotLine(BOOL bDirect);
void HomeDisplay(BOOL bDirect);
void HomeDisplayExtend(BOOL bDirect);
void LineEndDisplay(BOOL bDirect);
void LineEndDisplayExtend(BOOL bDirect);
void HomeWrap(BOOL bDirect);
void HomeWrapExtend(BOOL bDirect);
void LineEndWrap(BOOL bDirect);
void LineEndWrapExtend(BOOL bDirect);
void VCHomeWrap(BOOL bDirect);
void VCHomeWrapExtend(BOOL bDirect);
void LineCopy(BOOL bDirect);
void MoveCaretInsideView(BOOL bDirect);
int LineLength(int line, BOOL bDirect);
void BraceHighlight(long pos1, long pos2, BOOL bDirect);
void BraceHighlightIndicator(BOOL useBraceHighlightIndicator, int indicator, BOOL bDirect);
void BraceBadLight(long pos, BOOL bDirect);
void BraceBadLightIndicator(BOOL useBraceBadLightIndicator, int indicator, BOOL bDirect);
long BraceMatch(long pos, BOOL bDirect);
BOOL GetViewEOL(BOOL bDirect);
void SetViewEOL(BOOL visible, BOOL bDirect);
void* GetDocPointer(BOOL bDirect);
void SetDocPointer(void* pointer, BOOL bDirect);
void SetModEventMask(int mask, BOOL bDirect);
int GetEdgeColumn(BOOL bDirect);
void SetEdgeColumn(int column, BOOL bDirect);
int GetEdgeMode(BOOL bDirect);
void SetEdgeMode(int mode, BOOL bDirect);
COLORREF GetEdgeColour(BOOL bDirect);
void SetEdgeColour(COLORREF edgeColour, BOOL bDirect);
void SearchAnchor(BOOL bDirect);
int SearchNext(int flags, const char* text, BOOL bDirect);
int SearchPrev(int flags, const char* text, BOOL bDirect);
int LinesOnScreen(BOOL bDirect);
void UsePopUp(BOOL allowPopUp, BOOL bDirect);
BOOL SelectionIsRectangle(BOOL bDirect);
void SetZoom(int zoom, BOOL bDirect);
int GetZoom(BOOL bDirect);
int CreateDocument(BOOL bDirect);
void AddRefDocument(int doc, BOOL bDirect);
void ReleaseDocument(int doc, BOOL bDirect);
int GetModEventMask(BOOL bDirect);
void SCISetFocus(BOOL focus, BOOL bDirect);
BOOL GetFocus(BOOL bDirect);
void SetStatus(int statusCode, BOOL bDirect);
int GetStatus(BOOL bDirect);
void SetMouseDownCaptures(BOOL captures, BOOL bDirect);
BOOL GetMouseDownCaptures(BOOL bDirect);
void SetCursor(int cursorType, BOOL bDirect);
int GetCursor(BOOL bDirect);
void SetControlCharSymbol(int symbol, BOOL bDirect);
int GetControlCharSymbol(BOOL bDirect);
void WordPartLeft(BOOL bDirect);
void WordPartLeftExtend(BOOL bDirect);
void WordPartRight(BOOL bDirect);
void WordPartRightExtend(BOOL bDirect);
void SetVisiblePolicy(int visiblePolicy, int visibleSlop, BOOL bDirect);
void DelLineLeft(BOOL bDirect);
void DelLineRight(BOOL bDirect);
void SetXOffset(int newOffset, BOOL bDirect);
int GetXOffset(BOOL bDirect);
void ChooseCaretX(BOOL bDirect);
void GrabFocus(BOOL bDirect);
void SetXCaretPolicy(int caretPolicy, int caretSlop, BOOL bDirect);
void SetYCaretPolicy(int caretPolicy, int caretSlop, BOOL bDirect);
void SetPrintWrapMode(int mode, BOOL bDirect);
int GetPrintWrapMode(BOOL bDirect);
void SetHotspotActiveFore(BOOL useSetting, COLORREF fore, BOOL bDirect);
COLORREF GetHotspotActiveFore(BOOL bDirect);
void SetHotspotActiveBack(BOOL useSetting, COLORREF back, BOOL bDirect);
COLORREF GetHotspotActiveBack(BOOL bDirect);
void SetHotspotActiveUnderline(BOOL underline, BOOL bDirect);
BOOL GetHotspotActiveUnderline(BOOL bDirect);
void SetHotspotSingleLine(BOOL singleLine, BOOL bDirect);
BOOL GetHotspotSingleLine(BOOL bDirect);
void ParaDown(BOOL bDirect);
void ParaDownExtend(BOOL bDirect);
void ParaUp(BOOL bDirect);
void ParaUpExtend(BOOL bDirect);
long PositionBefore(long pos, BOOL bDirect);
long PositionAfter(long pos, BOOL bDirect);
void CopyRange(long start, long end, BOOL bDirect);
void CopyText(int length, const char* text, BOOL bDirect);
void SetSelectionMode(int mode, BOOL bDirect);
int GetSelectionMode(BOOL bDirect);
long GetLineSelStartPosition(int line, BOOL bDirect);
long GetLineSelEndPosition(int line, BOOL bDirect);
void LineDownRectExtend(BOOL bDirect);
void LineUpRectExtend(BOOL bDirect);
void CharLeftRectExtend(BOOL bDirect);
void CharRightRectExtend(BOOL bDirect);
void HomeRectExtend(BOOL bDirect);
void VCHomeRectExtend(BOOL bDirect);
void LineEndRectExtend(BOOL bDirect);
void PageUpRectExtend(BOOL bDirect);
void PageDownRectExtend(BOOL bDirect);
void StutteredPageUp(BOOL bDirect);
void StutteredPageUpExtend(BOOL bDirect);
void StutteredPageDown(BOOL bDirect);
void StutteredPageDownExtend(BOOL bDirect);
void WordLeftEnd(BOOL bDirect);
void WordLeftEndExtend(BOOL bDirect);
void WordRightEnd(BOOL bDirect);
void WordRightEndExtend(BOOL bDirect);
void SetWhitespaceChars(const char* characters, BOOL bDirect);
int GetWhitespaceChars(char* characters, BOOL bDirect);
void SetPunctuationChars(const char* characters, BOOL bDirect);
int GetPunctuationChars(char* characters, BOOL bDirect);
void SetCharsDefault(BOOL bDirect);
int AutoCGetCurrent(BOOL bDirect);
int AutoCGetCurrentText(char* s, BOOL bDirect);
void AutoCSetCaseInsensitiveBehaviour(int behaviour, BOOL bDirect);
int AutoCGetCaseInsensitiveBehaviour(BOOL bDirect);
void AutoCSetOrder(int order, BOOL bDirect);
int AutoCGetOrder(BOOL bDirect);
void Allocate(int bytes, BOOL bDirect);
int TargetAsUTF8(char* s, BOOL bDirect);
void SetLengthForEncode(int bytes, BOOL bDirect);
int EncodedFromUTF8(const char* utf8, char* encoded, BOOL bDirect);
int FindColumn(int line, int column, BOOL bDirect);
int GetCaretSticky(BOOL bDirect);
void SetCaretSticky(int useCaretStickyBehaviour, BOOL bDirect);
void ToggleCaretSticky(BOOL bDirect);
void SetPasteConvertEndings(BOOL convert, BOOL bDirect);
BOOL GetPasteConvertEndings(BOOL bDirect);
void SelectionDuplicate(BOOL bDirect);
void SetCaretLineBackAlpha(int alpha, BOOL bDirect);
int GetCaretLineBackAlpha(BOOL bDirect);
void SetCaretStyle(int caretStyle, BOOL bDirect);
int GetCaretStyle(BOOL bDirect);
void SetIndicatorCurrent(int indicator, BOOL bDirect);
int GetIndicatorCurrent(BOOL bDirect);
void SetIndicatorValue(int value, BOOL bDirect);
int GetIndicatorValue(BOOL bDirect);
void IndicatorFillRange(int position, int fillLength, BOOL bDirect);
void IndicatorClearRange(int position, int clearLength, BOOL bDirect);
int IndicatorAllOnFor(int position, BOOL bDirect);
int IndicatorValueAt(int indicator, int position, BOOL bDirect);
int IndicatorStart(int indicator, int position, BOOL bDirect);
int IndicatorEnd(int indicator, int position, BOOL bDirect);
void SetPositionCache(int size, BOOL bDirect);
int GetPositionCache(BOOL bDirect);
void CopyAllowLine(BOOL bDirect);
const char* GetCharacterPointer(BOOL bDirect);
void* GetRangePointer(int position, int rangeLength, BOOL bDirect);
long GetGapPosition(BOOL bDirect);
void SetKeysUnicode(BOOL keysUnicode, BOOL bDirect);
BOOL GetKeysUnicode(BOOL bDirect);
void IndicSetAlpha(int indicator, int alpha, BOOL bDirect);
int IndicGetAlpha(int indicator, BOOL bDirect);
void IndicSetOutlineAlpha(int indicator, int alpha, BOOL bDirect);
int IndicGetOutlineAlpha(int indicator, BOOL bDirect);
void SetExtraAscent(int extraAscent, BOOL bDirect);
int GetExtraAscent(BOOL bDirect);
void SetExtraDescent(int extraDescent, BOOL bDirect);
int GetExtraDescent(BOOL bDirect);
int MarkerSymbolDefined(int markerNumber, BOOL bDirect);
void MarginSetText(int line, const char* text, BOOL bDirect);
int MarginGetText(int line, char* text, BOOL bDirect);
void MarginSetStyle(int line, int style, BOOL bDirect);
int MarginGetStyle(int line, BOOL bDirect);
void MarginSetStyles(int line, const char* styles, BOOL bDirect);
int MarginGetStyles(int line, char* styles, BOOL bDirect);
void MarginTextClearAll(BOOL bDirect);
void MarginSetStyleOffset(int style, BOOL bDirect);
int MarginGetStyleOffset(BOOL bDirect);
void SetMarginOptions(int marginOptions, BOOL bDirect);
int GetMarginOptions(BOOL bDirect);
void AnnotationSetText(int line, const char* text, BOOL bDirect);
int AnnotationGetText(int line, char* text, BOOL bDirect);
void AnnotationSetStyle(int line, int style, BOOL bDirect);
int AnnotationGetStyle(int line, BOOL bDirect);
void AnnotationSetStyles(int line, const char* styles, BOOL bDirect);
int AnnotationGetStyles(int line, char* styles, BOOL bDirect);
int AnnotationGetLines(int line, BOOL bDirect);
void AnnotationClearAll(BOOL bDirect);
void AnnotationSetVisible(int visible, BOOL bDirect);
int AnnotationGetVisible(BOOL bDirect);
void AnnotationSetStyleOffset(int style, BOOL bDirect);
int AnnotationGetStyleOffset(BOOL bDirect);
void ReleaseAllExtendedStyles(BOOL bDirect);
int AllocateExtendedStyles(int numberStyles, BOOL bDirect);
void AddUndoAction(int token, int flags, BOOL bDirect);
long CharPositionFromPoint(int x, int y, BOOL bDirect);
long CharPositionFromPointClose(int x, int y, BOOL bDirect);
void SetMultipleSelection(BOOL multipleSelection, BOOL bDirect);
BOOL GetMultipleSelection(BOOL bDirect);
void SetAdditionalSelectionTyping(BOOL additionalSelectionTyping, BOOL bDirect);
BOOL GetAdditionalSelectionTyping(BOOL bDirect);
void SetAdditionalCaretsBlink(BOOL additionalCaretsBlink, BOOL bDirect);
BOOL GetAdditionalCaretsBlink(BOOL bDirect);
void SetAdditionalCaretsVisible(BOOL additionalCaretsBlink, BOOL bDirect);
BOOL GetAdditionalCaretsVisible(BOOL bDirect);
int GetSelections(BOOL bDirect);
BOOL GetSelectionEmpty(BOOL bDirect);
void ClearSelections(BOOL bDirect);
int SetSelection(int caret, int anchor, BOOL bDirect);
int AddSelection(int caret, int anchor, BOOL bDirect);
void SetMainSelection(int selection, BOOL bDirect);
int GetMainSelection(BOOL bDirect);
void SetSelectionNCaret(int selection, long pos, BOOL bDirect);
long GetSelectionNCaret(int selection, BOOL bDirect);
void SetSelectionNAnchor(int selection, long posAnchor, BOOL bDirect);
long GetSelectionNAnchor(int selection, BOOL bDirect);
void SetSelectionNCaretVirtualSpace(int selection, int space, BOOL bDirect);
int GetSelectionNCaretVirtualSpace(int selection, BOOL bDirect);
void SetSelectionNAnchorVirtualSpace(int selection, int space, BOOL bDirect);
int GetSelectionNAnchorVirtualSpace(int selection, BOOL bDirect);
void SetSelectionNStart(int selection, long pos, BOOL bDirect);
long GetSelectionNStart(int selection, BOOL bDirect);
void SetSelectionNEnd(int selection, long pos, BOOL bDirect);
long GetSelectionNEnd(int selection, BOOL bDirect);
void SetRectangularSelectionCaret(long pos, BOOL bDirect);
long GetRectangularSelectionCaret(BOOL bDirect);
void SetRectangularSelectionAnchor(long posAnchor, BOOL bDirect);
long GetRectangularSelectionAnchor(BOOL bDirect);
void SetRectangularSelectionCaretVirtualSpace(int space, BOOL bDirect);
int GetRectangularSelectionCaretVirtualSpace(BOOL bDirect);
void SetRectangularSelectionAnchorVirtualSpace(int space, BOOL bDirect);
int GetRectangularSelectionAnchorVirtualSpace(BOOL bDirect);
void SetVirtualSpaceOptions(int virtualSpaceOptions, BOOL bDirect);
int GetVirtualSpaceOptions(BOOL bDirect);
void SetRectangularSelectionModifier(int modifier, BOOL bDirect);
int GetRectangularSelectionModifier(BOOL bDirect);
void SetAdditionalSelFore(COLORREF fore, BOOL bDirect);
void SetAdditionalSelBack(COLORREF back, BOOL bDirect);
void SetAdditionalSelAlpha(int alpha, BOOL bDirect);
int GetAdditionalSelAlpha(BOOL bDirect);
void SetAdditionalCaretFore(COLORREF fore, BOOL bDirect);
COLORREF GetAdditionalCaretFore(BOOL bDirect);
void RotateSelection(BOOL bDirect);
void SwapMainAnchorCaret(BOOL bDirect);
int ChangeLexerState(long start, long end, BOOL bDirect);
int ContractedFoldNext(int lineStart, BOOL bDirect);
void VerticalCentreCaret(BOOL bDirect);
void MoveSelectedLinesUp(BOOL bDirect);
void MoveSelectedLinesDown(BOOL bDirect);
void SetIdentifier(int identifier, BOOL bDirect);
int GetIdentifier(BOOL bDirect);
void RGBAImageSetWidth(int width, BOOL bDirect);
void RGBAImageSetHeight(int height, BOOL bDirect);
void RGBAImageSetScale(int scalePercent, BOOL bDirect);
void MarkerDefineRGBAImage(int markerNumber, const char* pixels, BOOL bDirect);
void RegisterRGBAImage(int type, const char* pixels, BOOL bDirect);
void ScrollToStart(BOOL bDirect);
void ScrollToEnd(BOOL bDirect);
void SetTechnology(int technology, BOOL bDirect);
int GetTechnology(BOOL bDirect);
int CreateLoader(int bytes, BOOL bDirect);
void FindIndicatorShow(long start, long end, BOOL bDirect);
void FindIndicatorFlash(long start, long end, BOOL bDirect);
void FindIndicatorHide(BOOL bDirect);
void VCHomeDisplay(BOOL bDirect);
void VCHomeDisplayExtend(BOOL bDirect);
BOOL GetCaretLineVisibleAlways(BOOL bDirect);
void SetCaretLineVisibleAlways(BOOL bAlwaysVisible, BOOL bDirect);
void StartRecord(BOOL bDirect);
void StopRecord(BOOL bDirect);
void SetLexer(int lexer, BOOL bDirect);
int GetLexer(BOOL bDirect);
void Colourise(long start, long end, BOOL bDirect);
void SetProperty(const char* key, const char* value, BOOL bDirect);
void SetKeyWords(int keywordSet, const char* keyWords, BOOL bDirect);
void SetLexerLanguage(const char* language, BOOL bDirect);
void LoadLexerLibrary(const char* path, BOOL bDirect);
int GetProperty(const char* key, char* buf, BOOL bDirect);
int GetPropertyExpanded(const char* key, char* buf, BOOL bDirect);
int GetPropertyInt(const char* key, BOOL bDirect);
int GetStyleBitsNeeded(BOOL bDirect);
int GetLexerLanguage(char* text, BOOL bDirect);
void* PrivateLexerCall(int operation, void* pointer, BOOL bDirect);
int PropertyNames(char* names, BOOL bDirect);
int PropertyType(const char* name, BOOL bDirect);
int DescribeProperty(const char* name, char* description, BOOL bDirect);
int DescribeKeyWordSets(char* descriptions, BOOL bDirect);
void SetLineEndTypesAllowed(int lineEndBitSet, BOOL bDirect);
int GetLineEndTypesAllowed(BOOL bDirect);
int GetLineEndTypesActive(BOOL bDirect);
int GetLineEndTypesSupported(BOOL bDirect);
int AllocateSubStyles(int styleBase, int numberStyles, BOOL bDirect);
int GetSubStylesStart(int styleBase, BOOL bDirect);
int GetSubStylesLength(int styleBase, BOOL bDirect);
void FreeSubStyles(BOOL bDirect);
void SetIdentifiers(int style, const char* identifiers, BOOL bDirect);
int DistanceToSecondaryStyles(BOOL bDirect);
int GetSubStyleBases(char* styles, BOOL bDirect);
CStringA GetSelText(BOOL bDirect);
CStringA GetCurLine(BOOL bDirect);
CStringA GetLine(int line, BOOL bDirect);
CStringA GetProperty(const char* key, BOOL bDirect);
CStringA GetText(int length, BOOL bDirect);
CStringA GetPropertyExpanded(const char* key, BOOL bDirect);
CStringA StyleGetFont(int style, BOOL bDirect);
CStringA AutoCGetCurrentText(BOOL bDirect);
CStringA GetLexerLanguage(BOOL bDirect);
CStringA PropertyNames(BOOL bDirect);
CStringA DescribeProperty(const char* name, BOOL bDirect);
CStringA DescribeKeyWordSets(BOOL bDirect);
CStringA GetTag(int tagNumber, BOOL bDirect);
CStringA GetWordChars(BOOL bDirect);
CStringA GetWhitespaceChars(BOOL bDirect);
CStringA GetPunctuationChars(BOOL bDirect);