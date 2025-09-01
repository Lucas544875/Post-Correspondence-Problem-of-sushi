// ローカルストレージを使ったクリア状態の管理

export interface ClearData {
  problemId: number;
  clearedAt: string; // クリア日時 ISO string
  gameMode: 'np-hard' | 'undecidable';
}

const CLEAR_DATA_KEY = 'sushi-post-problem-clear-data';

// クリア状態をローカルストレージから取得
export const getClearData = (): ClearData[] => {
  try {
    const data = localStorage.getItem(CLEAR_DATA_KEY);
    return data ? JSON.parse(data) : [];
  } catch (error) {
    console.error('Failed to load clear data:', error);
    return [];
  }
};

// クリア状態をローカルストレージに保存
export const saveClearData = (clearData: ClearData[]): void => {
  try {
    localStorage.setItem(CLEAR_DATA_KEY, JSON.stringify(clearData));
  } catch (error) {
    console.error('Failed to save clear data:', error);
  }
};

// 特定の問題がクリア済みかどうかを確認
export const isProblemCleared = (problemId: string, gameMode: 'np-hard' | 'undecidable'): boolean => {
  const clearData = getClearData();
  const numericId = parseInt(problemId, 10);
  return clearData.some(data => data.problemId === numericId && data.gameMode === gameMode);
};

// 問題をクリア済みとしてマーク
export const markProblemCleared = (problemId: string, gameMode: 'np-hard' | 'undecidable'): void => {
  const clearData = getClearData();
  const numericId = parseInt(problemId, 10);
  
  // 既にクリア済みの場合は更新しない
  if (isProblemCleared(problemId, gameMode)) {
    return;
  }
  
  const newClearData: ClearData = {
    problemId: numericId,
    clearedAt: new Date().toISOString(),
    gameMode
  };
  
  clearData.push(newClearData);
  saveClearData(clearData);
};

// 特定のゲームモードでのクリア済み問題数を取得
export const getClearedProblemCount = (gameMode: 'np-hard' | 'undecidable'): number => {
  const clearData = getClearData();
  return clearData.filter(data => data.gameMode === gameMode).length;
};

// 全体のクリア率を取得
export const getClearProgress = (totalProblems: number, gameMode: 'np-hard' | 'undecidable'): number => {
  const clearedCount = getClearedProblemCount(gameMode);
  return totalProblems > 0 ? Math.round((clearedCount / totalProblems) * 100) : 0;
};