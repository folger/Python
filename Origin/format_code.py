data = [
    'HasOutliers, bDotCntrl, DWORD, BSC_OUTLIERS, FALSE',
    'HasDiamondBox, bDotCntrl, DWORD, BSC_DIAMOND, FALSE',
    'HasBoxLabel, bDotCntrl, DWORD, BSC_BOX_LABELS, FALSE',
    'HasWhiskerLabel, bDotCntrl, DWORD, BSC_HISTO_LABELS, FALSE',
    'HasMeanLine, byFlags, BYTE, BCIF_SHOW_MEAN_LINE, FALSE',
    'HasOutliersInLine, bDotCntrl, DWORD, BSC_OUTLIERS_IN_LINE, FALSE',
    'HasDataOnTopOfBox, bDotCntrl, DWORD, BSC_DRAW_DATA_ON_TOP_OF_BOX, FALSE',
    'HasMeanValueLabel, bDotCntrl, DWORD, BSC_MEAN_VALUE_LABEL, FALSE',
    'EnablePercentileMax, bQuantilesCtrl, BYTE, BQC_ENABLE_MAX, FALSE',
    'EnablePercentile99Percent, bQuantilesCtrl, BYTE, BQC_ENABLE_99PCT, FALSE',
    'EnablePercentileMean, bQuantilesCtrl, BYTE, BQC_ENABLE_MEAN, FALSE',
    'EnablePercentile1Percent, bQuantilesCtrl, BYTE, BQC_ENABLE_1PCT, FALSE',
    'EnablePercentileMin, bQuantilesCtrl, BYTE, BQC_ENABLE_MIN, FALSE',
    'EnablePercentileCustom, bQuantilesCtrl, BYTE, BQC_ENABLE_CUSTOM, FALSE',
    'JitterPoints, byFlags, BYTE, BCIF_JITTER_POINTS, FALSE',
]

template = '''BOOL	COKGraphicLayer::SetBoxChartInfo{name}(BOOL value, BOOL bUndo)
{{
	OK_UNDO_BOOL_CLASS(bUndo, GetBoxChartInfo{name}, SetBoxChartInfo{name}, COKGraphicLayer);
	return GeneralSetBoxChartInfoBit(&BOXCHARTINFO::{field}, value, bUndo, {bit});
}}
BOOL	COKGraphicLayer::GetBoxChartInfo{name}(BOOL& value)
{{
	return GeneralGetBoxChartInfoBit(&BOXCHARTINFO::{field}, value, {bit});
}}
'''

with open('q.cpp', 'w') as fw:
    for d in data:
        name, field, _, bit, _ = d.split(', ')
        print(template.format(name=name, field=field, bit=bit), file=fw, end='')

