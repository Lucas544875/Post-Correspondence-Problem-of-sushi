import assert from 'node:assert/strict';
import { build } from 'esbuild';

// Run the real game validator against every imported witness, without a browser.
const { outputFiles } = await build({
  stdin: {
    contents: `export { sampleProblems } from './src/data/problems';
      export { discoveredProblems } from './src/data/discoveredProblems';
      export { validateSolution, validateClearProof } from './src/utils/solutionValidator';`,
    resolveDir: process.cwd(),
    loader: 'ts',
  },
  bundle: true,
  write: false,
  platform: 'node',
  format: 'esm',
});
const { sampleProblems, discoveredProblems, validateSolution, validateClearProof } =
  await import(`data:text/javascript;base64,${Buffer.from(outputFiles[0].text).toString('base64')}`);
assert.equal(new Set(sampleProblems.map(problem => problem.id)).size, sampleProblems.length);
assert.deepEqual(discoveredProblems.map(problem => problem.id), ['13', '14', '15', '16', '17']);
assert.deepEqual(discoveredProblems.map(problem => problem.solution.length), [152, 174, 451, 1583, 2711]);
for (const problem of discoveredProblems) {
  assert.ok(sampleProblems.includes(problem));
  assert.equal(validateSolution(problem, []), false);
  assert.equal(validateSolution(problem, problem.solution.slice(0, -1)), false);
  assert.equal(validateSolution(problem, problem.solution), true, `Problem ${problem.id}`);
  assert.equal(validateClearProof({
    version: 2,
    problemId: problem.id,
    gameMode: 'np-hard',
    clearedAt: new Date().toISOString(),
    selectedTiles: problem.solution,
  }, sampleProblems), true);
  console.log(`Problem ${problem.id}: ${problem.solution.length} moves, clear and saved proof verified`);
}
