export interface Problem {
  id: string;
  tiles: Tile[];
  initialState: {
    topBelt: string;
    bottomBelt: string;
  };
  solution?: number[];
  solvable: boolean;
  difficulty: 'np-hard' | 'undecidable';
}

export interface Tile {
  id: string;
  top: string;    // 上のベルト（🌼 = 1）
  bottom: string; // 下のベルト（🍣 = 0）
}

export interface GameState {
  currentProblem: Problem | null;
  selectedTiles: number[];
  topBelt: string;
  bottomBelt: string;
  gameMode: 'np-hard' | 'undecidable';
  isCompleted: boolean;
}

export interface ClearProof {
  version: 2;
  problemId: string;
  clearedAt: string;
  gameMode: 'np-hard' | 'undecidable';
  selectedTiles: number[];
}

export type Screen = 'title' | 'problem-select' | 'game' | 'clear';
