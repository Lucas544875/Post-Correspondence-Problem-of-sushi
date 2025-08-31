import { useState, useEffect } from 'react';
import type { Problem, Screen } from '../types';
import { renderGameString, type ElementAnimation } from '../utils/gameUtils';
import { removeAllPairs, isCleared, type MergedElement } from '../utils/pairLogic';
import { GameIcon } from './GameIcon';

interface GameBoardProps {
  problem: Problem;
  onNavigate: (screen: Screen) => void;
  onClear: () => void;
}

// ベルトの状態履歴を管理するインターフェース
interface BeltState {
  topBelt: string;
  bottomBelt: string;
}

export const GameBoard = ({ problem, onNavigate, onClear }: GameBoardProps) => {
  const [beltHistory, setBeltHistory] = useState<BeltState[]>([{
    topBelt: problem.initialState.topBelt,
    bottomBelt: problem.initialState.bottomBelt
  }]);
  const [currentHistoryIndex, setCurrentHistoryIndex] = useState(0);
  const [topBelt, setTopBelt] = useState(problem.initialState.topBelt);
  const [bottomBelt, setBottomBelt] = useState(problem.initialState.bottomBelt);
  const [isShipping, setIsShipping] = useState(false);
  const [newTopItemsCount, setNewTopItemsCount] = useState(0);
  const [newBottomItemsCount, setNewBottomItemsCount] = useState(0);
  const [topAnimations, setTopAnimations] = useState<ElementAnimation[]>([]);
  const [bottomAnimations, setBottomAnimations] = useState<ElementAnimation[]>([]);
  const [animationPhase, setAnimationPhase] = useState<'idle' | 'merging' | 'shipping'>('idle');
  const [mergedElements, setMergedElements] = useState<MergedElement[]>([]);
  const [animationTimeouts, setAnimationTimeouts] = useState<number[]>([]);
  const [pendingFinalState, setPendingFinalState] = useState<{
    topBelt: string;
    bottomBelt: string;
    newTopItemsCount: number;
    newBottomItemsCount: number;
  } | null>(null);

  // アニメーションをキャンセルして最終状態を適用
  const cancelAnimationsAndApplyFinalState = () => {
    // 全てのタイムアウトをキャンセル
    animationTimeouts.forEach(timeout => clearTimeout(timeout));
    setAnimationTimeouts([]);
    
    // アニメーション状態をリセット
    setTopAnimations([]);
    setBottomAnimations([]);
    setMergedElements([]);
    setAnimationPhase('idle');
    setIsShipping(false);
    
    // 保留中の最終状態があれば適用
    if (pendingFinalState) {
      setTopBelt(pendingFinalState.topBelt);
      setBottomBelt(pendingFinalState.bottomBelt);
      setNewTopItemsCount(pendingFinalState.newTopItemsCount);
      setNewBottomItemsCount(pendingFinalState.newBottomItemsCount);
      setPendingFinalState(null);
      
      // 新規アイテムアニメーション用のタイマーをリセット
      setTimeout(() => {
        setNewTopItemsCount(0);
        setNewBottomItemsCount(0);
      }, 300);
    }
  };

  const handleTileClick = (tileIndex: number) => {
    // アニメーション中は入力をブロック
    const hasNewItems = newTopItemsCount > 0 || newBottomItemsCount > 0;
    if (animationPhase !== 'idle' || hasNewItems) {
      return;
    }

    const newTop = topBelt + problem.tiles[tileIndex].top;
    const newBottom = bottomBelt + problem.tiles[tileIndex].bottom;
    
    // 新しい状態を履歴に追加
    const _newState = removeAllPairs(newTop, newBottom);
    const newState = { topBelt: _newState.newTopBelt, bottomBelt: _newState.newBottomBelt};
    const newHistory = beltHistory.slice(0, currentHistoryIndex + 1);
    newHistory.push(newState);
    setBeltHistory(newHistory);
    setCurrentHistoryIndex(newHistory.length - 1);
    
    setTopBelt(newTop);
    setBottomBelt(newBottom);
    
    // 新しく追加されたアイテムの数を設定
    setNewTopItemsCount(problem.tiles[tileIndex].top.length);
    setNewBottomItemsCount(problem.tiles[tileIndex].bottom.length);
    
    // アニメーション後にリセット
    setTimeout(() => {
      setNewTopItemsCount(0);
      setNewBottomItemsCount(0);
    }, 300);

    console.log(newHistory)
  };

  // 一手戻る機能
  const handleUndo = () => {
    if (currentHistoryIndex > 0 && animationPhase === 'idle') {
      const newIndex = currentHistoryIndex - 1;
      const previousState = beltHistory[newIndex];
      setCurrentHistoryIndex(newIndex);
      setTopBelt(previousState.topBelt);
      setBottomBelt(previousState.bottomBelt);
    }
  };

  // ペア消去とクリア判定のuseEffect
  useEffect(() => {
    // アニメーション実行中は処理をスキップ
    if (animationPhase !== 'idle') return;
    
    // 新しいアイテム追加アニメーションの完了を待つ
    const hasNewItems = newTopItemsCount > 0 || newBottomItemsCount > 0;
    const animationDelay = hasNewItems ? 300 : 0;
    
    setTimeout(() => {
      if (animationPhase !== 'idle') return;
      
      if (topBelt.length > 0 && bottomBelt.length > 0) {
        const result = removeAllPairs(topBelt, bottomBelt);
        
        if (result.hasRemovals) {
          // 複数ペア同時消去アニメーション開始
          setIsShipping(true);
          setAnimationPhase('merging');
          
          setTopAnimations(result.topAnimations);
          setBottomAnimations(result.bottomAnimations);
          setMergedElements(result.mergedElements);
          
          // タイムアウトを管理するための配列
          const timeouts: number[] = [];

          // Phase 2: 合体表示から出荷フェーズへ (400ms後)
          const timeout1 = setTimeout(() => {
            // フェードアウト + スライドフォワードフェーズ
            setAnimationPhase('shipping');
          }, 400);
          timeouts.push(timeout1);
          
          // アニメーション完了、状態更新 (400ms後 + merged-item-fadeの時間)
          const timeout2 = setTimeout(() => {
            setTopAnimations([]);
            setBottomAnimations([]);
            setMergedElements([]);
            setIsShipping(false);
            setAnimationPhase('idle');
            setTopBelt(result.newTopBelt);
            setBottomBelt(result.newBottomBelt);
            setPendingFinalState(null);
            setAnimationTimeouts([]);
          }, 800);
          timeouts.push(timeout2);

          // タイムアウトを状態に保存
          setAnimationTimeouts(timeouts);
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
    }, animationDelay);
  }, [topBelt, bottomBelt, newTopItemsCount, newBottomItemsCount, animationPhase, onClear, onNavigate]);

  const handleClearAll = () => {
    // アニメーション中でもリセットは許可
    if (animationPhase !== 'idle') {
      cancelAnimationsAndApplyFinalState();
    }
    // 履歴を初期状態にリセット
    setBeltHistory([{
      topBelt: problem.initialState.topBelt,
      bottomBelt: problem.initialState.bottomBelt
    }]);
    setCurrentHistoryIndex(0);
    setTopBelt(problem.initialState.topBelt);
    setBottomBelt(problem.initialState.bottomBelt);
    setNewTopItemsCount(0);
    setNewBottomItemsCount(0);
    setPendingFinalState(null);
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
          <div className="flex gap-2">
            <button
              onClick={handleUndo}
              disabled={currentHistoryIndex === 0 || animationPhase !== 'idle'}
              className={`font-bold py-2 px-4 rounded ${
                currentHistoryIndex === 0 || animationPhase !== 'idle'
                  ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                  : 'bg-blue-500 hover:bg-blue-600 text-white'
              }`}
            >
              ↶ 戻る
            </button>
            <button
              onClick={handleClearAll}
              className="bg-yellow-500 hover:bg-yellow-600 text-white font-bold py-2 px-4 rounded"
            >
              リセット
            </button>
          </div>
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
            style={{ transformOrigin: "left", transform: 'rotate(-22.5deg)', top: "69%", left: "11%", containerType: "inline-size"}}
          >
            {renderGameString(topBelt, isShipping, "relative", newTopItemsCount, false, topAnimations)}
          </div>
          
          {/* 下のベルト */}
          <div 
            className="conveyor-content flex items-center z-20 absolute mb-0 w-[52%] min-h-12"
            style={{ transformOrigin: "left", transform: 'rotate(-22.5deg)', top: "80%", left: "26.5%", containerType: "inline-size" }}
          >
            {renderGameString(bottomBelt,isShipping, "relative", newBottomItemsCount, false, bottomAnimations)}
          </div>
          
          {/* 合体要素の表示 */}
          {mergedElements.map((element) => {
            // console.log(56 * element.pairIndex);
            return <div
              key={element.id}
              className={`absolute w-12 h-12 z-30 ${
                animationPhase === 'merging' ? 'merged-element-appear' : 
                animationPhase === 'shipping' ? 'merged-element-fade' : ''
              }`}
              style={{
                left: `${element.position.x}%`,
                top: `${element.position.y}%`,
                rotate: '-22.5deg',
                transform: `translateX(${56 * element.pairIndex}px)`,
              }}
            >
              <GameIcon
                type="tampopo_on_sashimi"
                size="relative"
                className="w-full h-full"
              />
            </div>
          })}
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