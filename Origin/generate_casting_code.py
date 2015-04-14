data = [
'TrMark',
'TrTraceCount',
'TrData',
'TrDataPoints',
'TrInternalSolution',
'TrAverageCount',
'TrLeakCount',
'TrLeakTraces',
'TrDataKind',
'TrFiller1',
'TrDataScaler',
'TrTimeOffset',
'TrZeroData',
'TrXInterval',
'TrXStart',
'TrYRange',
'TrYOffset',
'TrBandwidth',
'TrPipetteResistance',
'TrCellPotential',
'TrSealResistance',
'TrCSlow',
'TrGSeries',
'TrRsValue',
'TrGLeak',
'TrMConductance',
'TrLinkDAChannel',
'TrAdcChannel',
'TrYmin',
'TrYmax',
'TrSourceChannel',
'TrExternalSolution',
'TrCM',
'TrGM',
'TrPhase',
'TrDataCRC',
'TrCRC',
'TrGS',
'TrSelfChannel',
'TrInterleaveSize',
'TrInterleaveSkip',
'TrFiller2',
]

with open('a.cpp', 'w') as fw:
    for d in data:
        print('_check_reverse_order_struct_one(ptr, &PulTraceRecord9::{}, true);'.format(d), file=fw)