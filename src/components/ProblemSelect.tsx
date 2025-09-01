import type { Screen, Problem } from '../types';
import { isProblemCleared } from '../utils/storage';

interface ProblemSelectProps {
  problems: Problem[];
  gameMode: 'np-hard' | 'undecidable';
  onNavigate: (screen: Screen) => void;
  onSelectProblem: (problem: Problem) => void;
}

export const ProblemSelect = ({ problems, gameMode, onNavigate, onSelectProblem }: ProblemSelectProps) => {
  const filteredProblems = problems.filter(p => p.difficulty === gameMode);
  
  const modeTitle = "問題選択"//gameMode === 'np-hard' ? 'NP-ハードモード' : '決定不能モード';
  const modeColor = gameMode === 'np-hard' ? 'green' : 'red';

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-100 to-gray-200  p-8">
      <div className="max-w-4xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <button
            onClick={() => onNavigate('title')}
            className="bg-gray-500 hover:bg-gray-600 text-white font-bold py-2 px-4 rounded"
          >
            ← ホームに戻る
          </button>
          <h1 className={`text-4xl font-bold text-${modeColor}-800`}>
            {modeTitle}
          </h1>
          <div></div>
        </div>

        <div className="grid grid-cols-4 gap-6">
          {filteredProblems.map((problem, index) => {
            const isCleared = isProblemCleared(problem.id, gameMode);
            return (
              <button
                key={problem.id}
                onClick={() => {
                  onSelectProblem(problem);
                  onNavigate('game');
                }}
                className={`
                  aspect-square rounded-lg shadow-lg 
                  border-4 transition-all transform hover:scale-105
                  flex flex-col items-center justify-center text-3xl font-bold
                  relative border-${modeColor}-300 hover:border-${modeColor}-500 
                  ${isCleared 
                    ? 'bg-green-100 text-green-800'
                    : `bg-white text-${modeColor}-800 hover:bg-gray-50`
                  }
                `}
              >
                {isCleared && (
                  <div className="absolute top-2 right-2 text-green-600 text-lg">
                    ✓
                  </div>
                )}
                <div className="text-3xl font-bold">
                  {index + 1}
                </div>
                {isCleared && (
                  <div className="text-xs text-green-600 mt-1">
                    クリア済み
                  </div>
                )}
              </button>
            );
          })}
        </div>

        <div className="mt-8 text-center text-gray-600">
          {/* <p>問題を選択してください</p> */}
          {/* <p className="text-sm">
            {gameMode === 'np-hard' 
              ? '※ すべての問題に解答が存在します' 
              : '※ 解けない問題も含まれています'}
          </p> */}
        </div>
      </div>
    </div>
  );
};