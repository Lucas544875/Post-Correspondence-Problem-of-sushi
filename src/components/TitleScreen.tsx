import type { Screen } from '../types';

interface TitleScreenProps {
  onNavigate: (screen: Screen, gameMode?: 'np-hard' | 'undecidable') => void;
}

export const TitleScreen = ({ onNavigate }: TitleScreenProps) => {
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-100 to-gray-200  flex items-center justify-center">
      <div className="text-center space-y-8">
        <h1 className="text-6xl font-bold text-orange-800 mb-20 hachi-maru-pop-regular">
          <img src="/sashimi.png" alt="刺身" className="inline-block w-12 h-12 mr-2" />
          刺身にタンポポ乗せるだけ
          <img src="/tampopo.png" alt="タンポポ" className="inline-block w-12 h-12 ml-2" />
        </h1>
        
        <div className="space-y-4">
          <button
            onClick={() => onNavigate('problem-select', 'np-hard')}
            className="block w-80 mx-auto bg-teal-500 hover:bg-teal-600 text-white pt-2 pb-5 px-8 rounded-lg text-5xl transition-colors hachi-maru-pop-regular"
          >
            はじめる
          </button>
          
          {/* <button
            onClick={() => onNavigate('problem-select', 'undecidable')}
            className="block w-80 mx-auto bg-red-500 hover:bg-red-600 text-white font-bold py-4 px-8 rounded-lg text-xl transition-colors"
          >
            決定不能モード
          </button> */}
        </div>
      </div>
    </div>
  );
};