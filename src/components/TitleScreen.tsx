import type { Screen } from '../types';

interface TitleScreenProps {
  onNavigate: (screen: Screen, gameMode?: 'np-hard' | 'undecidable') => void;
}

export const TitleScreen = ({ onNavigate }: TitleScreenProps) => {
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-100 to-gray-200  flex items-center justify-center">
      <div className="text-center space-y-8">
        <h1 className="text-6xl font-bold text-orange-800 mb-20 hachi-maru-pop-regular">
          刺身にタンポポ乗せるだけ
        </h1>
        
        <div className="space-y-4">
          <button
            onClick={() => onNavigate('problem-select', 'np-hard')}
            className="block w-80 mx-auto bg-green-500 hover:bg-green-600 text-white font-bold py-4 px-8 rounded-lg text-xl transition-colors"
          >
            NP-ハードモード
          </button>
          
          <button
            onClick={() => onNavigate('problem-select', 'undecidable')}
            className="block w-80 mx-auto bg-red-500 hover:bg-red-600 text-white font-bold py-4 px-8 rounded-lg text-xl transition-colors"
          >
            決定不能モード
          </button>
        </div>
      </div>
    </div>
  );
};