import type { Problem } from '../types';

// 画像識別用の文字を使用
const SASHIMI = 'S';    // 刺身を表す文字
const DANDELION = 'T';  // タンポポ（Tampopo）を表す文字

export const sampleProblems: Problem[] = [
  {
    id: '1',
    difficulty: 'np-hard',
    solvable: true,
    solution: [0, 1, 0],
    tiles: [
      { id: 'tile-1', top: DANDELION, bottom: DANDELION + SASHIMI },
      { id: 'tile-2', top: SASHIMI, bottom: "" },
    ]
  },
  {
    id: '2',
    difficulty: 'np-hard',
    solvable: true,
    solution: [1, 0, 1, 0],
    tiles: [
      { id: 'tile-1', top: DANDELION + SASHIMI, bottom: DANDELION + SASHIMI + DANDELION },
      { id: 'tile-2', top: SASHIMI, bottom: DANDELION },
      { id: 'tile-3', top: DANDELION, bottom: SASHIMI },
    ]
  },
  {
    id: '3',
    difficulty: 'undecidable',
    solvable: false,
    tiles: [
      { id: 'tile-1', top: DANDELION, bottom: DANDELION + SASHIMI },
      { id: 'tile-2', top: DANDELION + SASHIMI, bottom: DANDELION },
    ]
  },
];