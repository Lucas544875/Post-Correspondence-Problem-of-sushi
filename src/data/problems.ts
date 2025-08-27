import type { Problem } from '../types';

// 絵文字の代わりに安全な文字を使用
const SASHIMI = '🍣';  // 刺身
const DANDELION = '🌼'; // タンポポ

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