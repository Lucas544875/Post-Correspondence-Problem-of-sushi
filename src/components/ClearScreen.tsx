import type { Screen } from '../types';

interface ClearScreenProps {
  onNavigate: (screen: Screen) => void;
  onNextProblem: () => void;
  hasNextProblem: boolean;
}

export const ClearScreen = ({ onNavigate, onNextProblem, hasNextProblem }: ClearScreenProps) => {
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-100 to-gray-200 flex items-center justify-center">
      <div className="text-center space-y-8">
        <div className="text-8xl mb-4">🎉</div>
        <h1 className="text-6xl font-bold text-green-800 mb-4">
          クリア！
        </h1>
        <p className="text-2xl text-gray-700 mb-8">
          すべての刺身パックを出荷しました！
        </p>
        
        <div className="space-y-4">
          {hasNextProblem && (
            <button
              onClick={onNextProblem}
              className="block w-64 mx-auto bg-blue-500 hover:bg-blue-600 text-white font-bold py-4 px-8 rounded-lg text-xl transition-colors"
            >
              ➡️ 次の問題へ
            </button>
          )}
          
          <button
            onClick={() => onNavigate('problem-select')}
            className="block w-64 mx-auto bg-orange-500 hover:bg-orange-600 text-white font-bold py-4 px-8 rounded-lg text-xl transition-colors"
          >
            📋 問題選択に戻る
          </button>
          
          <button
            onClick={() => onNavigate('title')}
            className="block w-64 mx-auto bg-gray-500 hover:bg-gray-600 text-white font-bold py-4 px-8 rounded-lg text-xl transition-colors"
          >
            🏠 ホームに戻る
          </button>
        </div>
      </div>
    </div>
  );
};