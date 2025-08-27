import type { Screen } from '../types';

interface TitleScreenProps {
  onNavigate: (screen: Screen, gameMode?: 'np-hard' | 'undecidable') => void;
}

export const TitleScreen = ({ onNavigate }: TitleScreenProps) => {
  return (
    <div className="min-h-screen bg-gradient-to-b from-orange-100 to-yellow-100 flex items-center justify-center">
      <div className="text-center space-y-8">
        <h1 className="text-6xl font-bold text-orange-800 mb-4">
          🍣 寿司ポスト問題 🌼
        </h1>
        <p className="text-xl text-gray-700 mb-8">
          刺身パックとタンポポでポスト対応問題を解こう！
        </p>
        
        <div className="space-y-4">
          <button
            onClick={() => onNavigate('problem-select', 'np-hard')}
            className="block w-80 mx-auto bg-green-500 hover:bg-green-600 text-white font-bold py-4 px-8 rounded-lg text-xl transition-colors"
          >
            🟢 NP-ハードモード
            <div className="text-sm opacity-80">（解答が存在する問題）</div>
          </button>
          
          <button
            onClick={() => onNavigate('problem-select', 'undecidable')}
            className="block w-80 mx-auto bg-red-500 hover:bg-red-600 text-white font-bold py-4 px-8 rounded-lg text-xl transition-colors"
          >
            🔴 決定不能モード
            <div className="text-sm opacity-80">（解けない問題も含む）</div>
          </button>
        </div>
      </div>
    </div>
  );
};