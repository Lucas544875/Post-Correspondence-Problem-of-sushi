import type { Problem } from '../types';

// 画像識別用の文字を使用

export const sampleProblems: Problem[] = [
  {
    id: '1',
    difficulty: 'np-hard',
    solvable: true,
    solution: [0],
    initialState: {
      topBelt: 'S',
      bottomBelt: ""
    },
    tiles: [
      { id: 'tile-1', top: "", bottom: 'T' }
    ]
  },
  {
    id: '2',
    difficulty: 'np-hard',
    solvable: true,
    solution: [0,1],
    initialState: {
      topBelt: 'S',
      bottomBelt: ""
    },
    tiles: [
      { id: 'tile-1', top: 'T', bottom: 'T' },
      { id: 'tile-2', top: '', bottom: 'S' },
    ]
  },
  {
    id: '103',
    difficulty: 'undecidable',
    solvable: false,
    initialState: {
      topBelt: 'STS',        // STS
      bottomBelt: 'TST'    // TST
    },
    tiles: [
      { id: 'tile-1', top: 'S', bottom: 'T' },      // 上:刺身、下:タンポポ
      { id: 'tile-2', top: 'T', bottom: 'S' },      // 上:タンポポ、下:刺身
    ]
  },
];