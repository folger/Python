data = [
    #'BinAlign, bCharBinAlign, FALSE',
    #'Intervals, dBinWidth, TRUE',
    #'BoxRange, bBoxType, FALSE',
    #'WhiskerRange, bWhiskerType, FALSE',
    #'SymbolEdgeColor, lSymbolColor, FALSE',
    #'SymbolFillColor, lSymbolFill, FALSE',
    #'CharIndex1, bSymbolStyle1, FALSE',
    #'CharIndex99, bSymbolStyle99, FALSE',
    #'CharIndexMean, bSymbolStyleMean, FALSE',
    #'CharIndexMin, bSymbolStyleMin, FALSE',
    #'CharIndexMax, bSymbolStyleMax, FALSE',
    #'CharFont1, bCharFont1, FALSE',
    #'CharFont99, bCharFont99, FALSE',
    #'CharFontMean, bCharFontMean, FALSE',
    #'CharFontMin, bCharFontMin, FALSE',
    #'CharFontMax, bCharFontMax, FALSE',
    #'CharStyle1, bCharStyle1, FALSE',
    #'CharStyle99, bCharStyle99, FALSE',
    #'CharStyleMean, bCharStyleMean, FALSE',
    #'CharStyleMin, bCharStyleMin, FALSE',
    #'CharStyleMax, bCharStyleMax, FALSE',
    #'BoxChartLabelsShow, bBoxChartLabelsShow, FALSE',
    #'BinomialTrialsNum, lBinomialTrialsNum, FALSE',
    'SymbolShape1, bSymbol1, FALSE',
    'SymbolShape99, bSymbol99, FALSE',
    'SymbolShapeMean, bSymbolMean, FALSE',
    'SymbolShapeMin, bSymbolMin, FALSE',
    'SymbolShapeMax, bSymbolMax, FALSE',
    'SymbolInterior1, bSymbolFill1, FALSE',
    'SymbolInterior99, bSymbolFill99, FALSE',
    'SymbolInteriorMean, bSymbolFillMean, FALSE',
    'SymbolInteriorMin, bSymbolFillMin, FALSE',
    'SymbolInteriorMax, bSymbolFillMax, FALSE',
]

#template = '''BOOL	COKGraphicLayer::SetBoxChartInfo{name}(int value, BOOL bUndo)
#{{
	#OK_UNDO_INT_CLASS(bUndo, GetBoxChartInfo{name}, SetBoxChartInfo{name}, COKGraphicLayer);
	#return GeneralSetBoxChartInfo(&BOXCHARTINFO::{field}, value, bUndo);
#}}
#BOOL	COKGraphicLayer::GetBoxChartInfo{name}(int& value)
#{{
	#return GeneralGetBoxChartInfo(&BOXCHARTINFO::{field}, value);
#}}
#'''
template = '''BOOL	COKGraphicLayer::SetBoxChartInfo{name}(int value, BOOL bUndo)
{{
	OK_UNDO_INT_CLASS(bUndo, GetBoxChartInfo{name}, SetBoxChartInfo{name}, COKGraphicLayer);
	return GeneralSetBoxChartInfo(&BOXCHARTINFO::{field}, value, bUndo, (BOOL (COKGraphicLayer::*)(int&))nullptr, 0, &SYMBOL_UNIT_2_SIZE);
}}
BOOL	COKGraphicLayer::GetBoxChartInfo{name}(int& value)
{{
	return GeneralGetBoxChartInfo(&BOXCHARTINFO::{field}, value, &SYMBOL_SIZE_2_UNIT);
}}
'''

with open('q.cpp', 'w') as fw:
    for d in data:
        name, field, _ = d.split(', ')
        print(template.format(name=name, field=field), file=fw, end='')

