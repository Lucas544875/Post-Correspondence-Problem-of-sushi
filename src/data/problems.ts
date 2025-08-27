import type { Problem } from '../types';

// 画像識別用の文字を使用
const SASHIMI = 'S';    // 刺身を表す文字
const DANDELION = 'T';  // タンポポ（Tampopo）を表す文字

export const sampleProblems: Problem[] = [
  {
    id: '1',
    difficulty: 'np-hard',
    solvable: true,
    solution: [0, 1],
    initialState: {
      topBelt: SASHIMI + SASHIMI + DANDELION,      // SST
      bottomBelt: ""    // 
    },
    tiles: [
      { id: 'tile-1', top: "", bottom: SASHIMI },        // 上下共に刺身
      { id: 'tile-2', top: "", bottom: DANDELION },    // 上下共にタンポポ
    ]
  },
  {
    id: '2',
    difficulty: 'np-hard',
    solvable: true,
    solution: [0, 2, 1],
    initialState: {
      topBelt: SASHIMI + SASHIMI + DANDELION,        // SST
      bottomBelt: ""    // TTS
    },
    tiles: [
      { id: 'tile-1', top: SASHIMI, bottom: DANDELION },      // 上:刺身、下:タンポポ
      { id: 'tile-2', top: DANDELION, bottom: SASHIMI },      // 上:タンポポ、下:刺身
      { id: 'tile-3', top: SASHIMI + DANDELION, bottom: DANDELION + SASHIMI }, // 上:ST、下:TS
    ]
  },
  {
    id: '3',
    difficulty: 'undecidable',
    solvable: false,
    initialState: {
      topBelt: SASHIMI + DANDELION + SASHIMI,        // STS
      bottomBelt: DANDELION + SASHIMI + DANDELION    // TST
    },
    tiles: [
      { id: 'tile-1', top: SASHIMI, bottom: DANDELION },      // 上:刺身、下:タンポポ
      { id: 'tile-2', top: DANDELION, bottom: SASHIMI },      // 上:タンポポ、下:刺身
    ]
  },
];