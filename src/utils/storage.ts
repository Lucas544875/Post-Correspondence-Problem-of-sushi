import { sampleProblems } from '../data/problems';
import type { ClearProof } from '../types';
import { isClearProof, validateClearProof } from './solutionValidator';

const CLEAR_DATA_KEY = 'sushi-post-problem-clear-data-v2';

const saveClearData = (clearData: ClearProof[]): boolean => {
  try {
    localStorage.setItem(CLEAR_DATA_KEY, JSON.stringify(clearData));
    return true;
  } catch (error) {
    console.error('Failed to save clear data:', error);
    return false;
  }
};

export const getClearData = (): ClearProof[] => {
  try {
    const storedData = localStorage.getItem(CLEAR_DATA_KEY);
    if (storedData === null) return [];

    const parsedData: unknown = JSON.parse(storedData);
    if (!Array.isArray(parsedData)) {
      saveClearData([]);
      return [];
    }

    const verifiedData: ClearProof[] = [];
    const verifiedProblems = new Set<string>();
    let needsRewrite = false;

    for (const value of parsedData) {
      if (!isClearProof(value) || !validateClearProof(value, sampleProblems)) {
        needsRewrite = true;
        continue;
      }

      const problemKey = `${value.gameMode}:${value.problemId}`;
      if (verifiedProblems.has(problemKey)) {
        needsRewrite = true;
        continue;
      }

      verifiedProblems.add(problemKey);
      verifiedData.push(value);
    }

    if (needsRewrite) {
      saveClearData(verifiedData);
    }

    return verifiedData;
  } catch (error) {
    console.error('Failed to load clear data:', error);
    saveClearData([]);
    return [];
  }
};

export const isProblemCleared = (problemId: string, gameMode: 'np-hard' | 'undecidable'): boolean => {
  return getClearData().some(data => (
    data.problemId === problemId && data.gameMode === gameMode
  ));
};

export const markProblemCleared = (
  problemId: string,
  gameMode: 'np-hard' | 'undecidable',
  selectedTiles: number[]
): boolean => {
  const clearData = getClearData();

  if (clearData.some(data => data.problemId === problemId && data.gameMode === gameMode)) {
    return true;
  }

  const newClearProof: ClearProof = {
    version: 2,
    problemId,
    clearedAt: new Date().toISOString(),
    gameMode,
    selectedTiles: [...selectedTiles]
  };

  if (!validateClearProof(newClearProof, sampleProblems)) {
    return false;
  }

  return saveClearData([...clearData, newClearProof]);
};

export const getClearedProblemCount = (gameMode: 'np-hard' | 'undecidable'): number => {
  return getClearData().filter(data => data.gameMode === gameMode).length;
};

export const getClearProgress = (totalProblems: number, gameMode: 'np-hard' | 'undecidable'): number => {
  const clearedCount = getClearedProblemCount(gameMode);
  return totalProblems > 0 ? Math.round((clearedCount / totalProblems) * 100) : 0;
};
