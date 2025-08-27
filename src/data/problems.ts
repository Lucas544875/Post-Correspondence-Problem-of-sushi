import type { Problem } from '../types';

export const sampleProblems: Problem[] = [
  {
    id: '1',
    difficulty: 'np-hard',
    solvable: true,
    solution: [0, 1, 0],
    tiles: [
      { id: 'tile-1', top: '1', bottom: '10' },
      { id: 'tile-2', top: '0', bottom: '1' },
    ]
  },
  {
    id: '2',
    difficulty: 'np-hard',
    solvable: true,
    solution: [1, 0, 1, 0],
    tiles: [
      { id: 'tile-1', top: '10', bottom: '101' },
      { id: 'tile-2', top: '0', bottom: '1' },
      { id: 'tile-3', top: '1', bottom: '0' },
    ]
  },
  {
    id: '3',
    difficulty: 'undecidable',
    solvable: false,
    tiles: [
      { id: 'tile-1', top: '1', bottom: '10' },
      { id: 'tile-2', top: '10', bottom: '1' },
    ]
  },
];