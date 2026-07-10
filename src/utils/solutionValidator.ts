import type { ClearProof, Problem } from '../types';
import { removeAllPairs } from './pairLogic';

const MAX_SELECTED_TILES = 10_000;

export const isClearProof = (value: unknown): value is ClearProof => {
  if (typeof value !== 'object' || value === null) return false;

  const proof = value as Record<string, unknown>;

  return proof.version === 2
    && typeof proof.problemId === 'string'
    && typeof proof.clearedAt === 'string'
    && !Number.isNaN(Date.parse(proof.clearedAt))
    && (proof.gameMode === 'np-hard' || proof.gameMode === 'undecidable')
    && Array.isArray(proof.selectedTiles)
    && proof.selectedTiles.length <= MAX_SELECTED_TILES
    && proof.selectedTiles.every(tileIndex => Number.isInteger(tileIndex));
};

export const validateSolution = (problem: Problem, selectedTiles: number[]): boolean => {
  if (selectedTiles.length > MAX_SELECTED_TILES) return false;

  const initialResult = removeAllPairs(
    problem.initialState.topBelt,
    problem.initialState.bottomBelt
  );
  let topBelt = initialResult.newTopBelt;
  let bottomBelt = initialResult.newBottomBelt;

  for (const tileIndex of selectedTiles) {
    if (!Number.isInteger(tileIndex)) return false;

    const tile = problem.tiles[tileIndex];
    if (!tile || (topBelt.length > 0 && bottomBelt.length > 0)) return false;

    const result = removeAllPairs(
      topBelt + tile.top,
      bottomBelt + tile.bottom
    );
    topBelt = result.newTopBelt;
    bottomBelt = result.newBottomBelt;
  }

  return topBelt.length === 0 && bottomBelt.length === 0;
};

export const validateClearProof = (proof: ClearProof, problems: Problem[]): boolean => {
  const problem = problems.find(candidate => (
    candidate.id === proof.problemId && candidate.difficulty === proof.gameMode
  ));

  return problem !== undefined && validateSolution(problem, proof.selectedTiles);
};
