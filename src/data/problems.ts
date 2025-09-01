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
    id: '3',
    difficulty: 'np-hard',
    solvable: true,
    solution: [0,0,1],
    initialState: {
      topBelt: 'TST',
      bottomBelt: ""
    },
    tiles: [
      { id: 'tile-1', top: 'S', bottom: 'ST' },
      { id: 'tile-2', top: 'T', bottom: 'TS' },
    ]
  },
  {
    id: '4',
    difficulty: 'np-hard',
    solvable: true,
    solution: [1,1,0,1],
    initialState: {
      topBelt: 'STSS',        // STS
      bottomBelt: ''    // TST
    },
    tiles: [
      { id: 'tile-1', top: 'SS', bottom: 'STT' },
      { id: 'tile-2', top: 'TS', bottom: 'TST' },
    ]
  },
  {
    id: '5',
    difficulty: 'np-hard',
    solvable: true,
    solution: [0,1,2],
    initialState: {
      topBelt: 'TT',
      bottomBelt: ''
    },
    tiles: [
      { id: 'tile-1', top: 'S', bottom: 'S' },
      { id: 'tile-2', top: 'S', bottom: 'ST' },
      { id: 'tile-3', top: 'T', bottom: 'TS' },
    ]
  },
  {
    id: '6',
    difficulty: 'np-hard',
    solvable: true,
    solution: [0,2,2,0,1],
    initialState: {
      topBelt: 'TSTT',
      bottomBelt: ''
    },
    tiles: [
      { id: 'tile-1', top: 'S', bottom: 'S' },
      { id: 'tile-2', top: 'S', bottom: 'STT' },
      { id: 'tile-3', top: 'TT', bottom: 'TSS' },
    ]
  },
  {
    id: '7',
    difficulty: 'np-hard',
    solvable: true,
    solution: [0,0,0,1,2,2,2,0,0,1,2,2,0,1,2,1],
    initialState: {
      topBelt: 'TTTT',
      bottomBelt: ''
    },
    tiles: [
      { id: 'tile-1', top: 'S', bottom: 'S' },
      { id: 'tile-2', top: 'T', bottom: 'T' },
      { id: 'tile-3', top: 'S', bottom: 'ST' },
    ]
  },
  {
    id: "8",
    difficulty: 'np-hard',
    solvable: true,
    solution: [2,2,2,2,0,2,0,2,0,2,1,1,1,1,2,2,2,0,2,0,2,1,1,1,2,2,0,2,1,1,2,1],
    initialState: {
      topBelt: 'SSSS',
      bottomBelt: ''
    },
    tiles: [
      { id: 'tile-1', top: 'S', bottom: 'S' },
      { id: 'tile-2', top: 'S', bottom: 'STT' },
      { id: 'tile-3', top: 'TS', bottom: 'T' },
    ]
  },
  {
    id: "9",
    difficulty: 'np-hard',
    solvable: true,
    solution: [],
    initialState: {
      topBelt: 'TT',
      bottomBelt: ''
    },
    tiles: [
      { id: 'tile-1', top: 'STT', bottom: 'T' },
      { id: 'tile-2', top: 'T', bottom: 'TSS' },
      { id: 'tile-3', top: 'S', bottom: 'S' },
    ]
  },
  {
    id: "10",
    difficulty: 'np-hard',
    solvable: true,
    solution: [],
    initialState: {
      topBelt: '',
      bottomBelt: 'ST'
    },
    tiles: [
      { id: 'tile-1', top: 'TTST', bottom: 'S' },
      { id: 'tile-2', top: 'STTS', bottom: 'SS' },
      { id: 'tile-3', top: 'T', bottom: 'SST' },
    ]
  },
    {
    id: '11',
    difficulty: 'np-hard',
    solvable: true,
    solution: [],
    initialState: {
      topBelt: '',
      bottomBelt: 'TS'
    },
    tiles: [
      { id: 'tile-1', top: 'TTST', bottom: 'TST' },
      { id: 'tile-2', top: 'ST', bottom: 'S' },
      { id: 'tile-3', top: 'T', bottom: 'STS' },
    ]
  },
  {
    id: "12",
    difficulty: 'np-hard',
    solvable: true,
    solution: [],
    initialState: {
      topBelt: '',
      bottomBelt: 'ST'
    },
    tiles: [
      { id: 'tile-1', top: 'STTS', bottom: 'T' },
      { id: 'tile-2', top: 'T', bottom: 'SST' },
      { id: 'tile-3', top: 'TS', bottom: 'S' },
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