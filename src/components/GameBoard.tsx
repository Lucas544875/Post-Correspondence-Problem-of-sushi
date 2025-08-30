import { useState, useEffect } from 'react';
import type { Problem, Screen } from '../types';
import { renderGameString } from '../utils/gameUtils';
import { removePairs, isCleared } from '../utils/pairLogic';

interface GameBoardProps {
  problem: Problem;
  onNavigate: (screen: Screen) => void;
  onClear: () => void;
}

export const GameBoard = ({ problem, onNavigate, onClear }: GameBoardProps) => {
  const [selectedTiles, setSelectedTiles] = useState<number[]>([]);
  const [topBelt, setTopBelt] = useState(problem.initialState.topBelt);
  const [bottomBelt, setBottomBelt] = useState(problem.initialState.bottomBelt);
  const [isShipping, setIsShipping] = useState(false);

  const handleTileClick = (tileIndex: number) => {
    if (isShipping) return; // 出荷中は操作を無効化

    const newSelected = [...selectedTiles, tileIndex];
    const newTop = topBelt + problem.tiles[tileIndex].top;
    const newBottom = bottomBelt + problem.tiles[tileIndex].bottom;
    
    setSelectedTiles(newSelected);
    setTopBelt(newTop);
    setBottomBelt(newBottom);
  };

  // ペア消去とクリア判定のuseEffect
  useEffect(() => {
    if (topBelt.length > 0 && bottomBelt.length > 0) {
      const result = removePairs(topBelt, bottomBelt);
      
      if (result.hasRemovals) {
        // 出荷アニメーション開始
        setIsShipping(true);
        
        setTimeout(() => {
          setTopBelt(result.newTopBelt);
          setBottomBelt(result.newBottomBelt);
          setIsShipping(false);
          
          // 再帰的にペアチェック（連続ペア消去のため）
          // 次のフレームで再度useEffectが発火する
          
        }, 800); // アニメーション時間
      } else {
        // ペアがない場合、クリア判定
        if (isCleared(topBelt, bottomBelt)) {
          setTimeout(() => {
            onClear();
            onNavigate('clear');
          }, 500);
        }
      }
    } else {
      // どちらかが空の場合もクリア判定
      if (isCleared(topBelt, bottomBelt)) {
        setTimeout(() => {
          onClear();
          onNavigate('clear');
        }, 500);
      }
    }
  }, [topBelt, bottomBelt, onClear, onNavigate]);

  const handleClearAll = () => {
    setSelectedTiles([]);
    setTopBelt(problem.initialState.topBelt);
    setBottomBelt(problem.initialState.bottomBelt);
  };

  const handleImpossible = () => {
    alert('この問題は解けません！');
    onNavigate('clear');
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-100 to-gray-200 pt-8 px-8">
      <div className="max-w-6xl mx-auto ">
        {/* ヘッダー */}
        <div className="flex items-center justify-between">
          <button
            onClick={() => onNavigate('problem-select')}
            className="bg-gray-500 hover:bg-gray-600 text-white font-bold py-2 px-4 rounded"
          >
            ← 戻る
          </button>
          <h1 className="text-3xl font-bold text-gray-800">
            問題 {problem.id}
          </h1>
          <button
            onClick={handleClearAll}
            className="bg-yellow-500 hover:bg-yellow-600 text-white font-bold py-2 px-4 rounded"
          >
            リセット
          </button>
        </div>

        {/* ベルトコンベア表示エリア */}
        <div className="mb-4 space-y-6 relative"> {/* 画面サイズ依存 */}
          <img 
            src="/src/assets/conveyors.png" 
            alt="conveyor belt"
            className="w-full object-cover z-10 mb-0"
          />
          {/* 上のベルト */}
          <div
            className="conveyor-content flex items-center z-20 absolute mb-0 w-[52%] min-h-12"
            style={{ transformOrigin: "left", transform: 'rotate(-22.5deg)', top: "69%", left: "11%" }}
          >
            {renderGameString(topBelt, isShipping, "relative")}
          </div>
          
          {/* 下のベルト */}
          <div 
            className="conveyor-content flex items-center z-20 absolute mb-0 w-[52%] min-h-12"
            style={{ transformOrigin: "left", transform: 'rotate(-22.5deg)', top: "80%", left: "26.5%" }}
          >
            {renderGameString(bottomBelt, isShipping, "relative")}
          </div>
        </div>

        {/* タイルボタン */}
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4 max-w-2xl mx-auto m-12">
          {problem.tiles.map((tile, index) => (
            <button
              key={tile.id}
              onClick={() => handleTileClick(index)}
              className="tile-button bg-white hover:bg-gray-50 border-4 border-orange-300 hover:border-orange-500 rounded-lg p-4"
            >
              <div className="text-center">
                <div className="text-lg font-bold text-yellow-600 mb-2 flex items-center justify-center">
                  上: <div className="ml-2 flex">{renderGameString(tile.top)}</div>
                </div>
                <div className="text-lg font-bold text-red-600 flex items-center justify-center">
                  下: <div className="ml-2 flex">{renderGameString(tile.bottom)}</div>
                </div>
              </div>
            </button>
          ))}
        </div>

        {/* 決定不能モード用の不可能ボタン */}
        {problem.difficulty === 'undecidable' && (
          <div className="text-center">
            <button
              onClick={handleImpossible}
              className="bg-red-500 hover:bg-red-600 text-white font-bold py-3 px-6 rounded-lg text-lg"
            >
              ❌ この問題は解けない
            </button>
          </div>
        )}
      </div>
    </div>
  );
};