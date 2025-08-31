// ペア消去ロジック
import type { ElementAnimation } from './gameUtils';

// 合体要素の情報
export interface MergedElement {
  id: string;
  pairIndex: number;
  topChar: string;
  bottomChar: string;
  position: { x: number; y: number }; // 表示位置（パーセント）
}

export interface PairRemovalResult {
  newTopBelt: string;
  newBottomBelt: string;
  removedPairs: Array<{ top: string; bottom: string; topIndex: number; bottomIndex: number }>;
  hasRemovals: boolean;
  topAnimations: ElementAnimation[];
  bottomAnimations: ElementAnimation[];
  mergedElements: MergedElement[]; // 追加: 合体要素の配列
}

// 先頭の一組だけをチェックして消去（一回につき1ペアのみ）
// export const removePairs = (topBelt: string, bottomBelt: string): PairRemovalResult => {
//   const removedPairs: Array<{ top: string; bottom: string; topIndex: number; bottomIndex: number }> = [];
  
//   // アニメーション配列を初期化
//   const topAnimations: ElementAnimation[] = Array.from(topBelt).map(() => ({ state: 'normal' }));
//   const bottomAnimations: ElementAnimation[] = Array.from(bottomBelt).map(() => ({ state: 'normal' }));
  
//   // 両方のレーンに文字がある場合のみチェック
//   if (topBelt.length > 0 && bottomBelt.length > 0) {
//     const topChar = topBelt[0];
//     const bottomChar = bottomBelt[0];
    
//     // 刺身（S）とタンポポ（T）のペアをチェック
//     if ((topChar === 'S' && bottomChar === 'T') || (topChar === 'T' && bottomChar === 'S')) {
//       // ペア発見！先頭の1文字ずつを消去
//       removedPairs.push({ top: topChar, bottom: bottomChar, topIndex: 0, bottomIndex: 0 });
      
//       // アニメーション状態を設定
//       topAnimations[0] = { state: 'move-from-top', pairIndex: 0 };
//       bottomAnimations[0] = { state: 'move-from-bottom', pairIndex: 0 };
      
//       // 残った要素に左詰めアニメーションを設定
//       for (let i = 1; i < topBelt.length; i++) {
//         topAnimations[i] = { state: 'slide-forward' };
//       }
//       for (let i = 1; i < bottomBelt.length; i++) {
//         bottomAnimations[i] = { state: 'slide-forward' };
//       }
      
//       // 合体要素を生成
//       const mergedElements: MergedElement[] = [{
//         id: `merged-${Date.now()}-0`,
//         pairIndex: 0,
//         topChar: topChar,
//         bottomChar: bottomChar,
//         position: { x: 50, y: 75 } // 中央付近に配置
//       }];

//       return {
//         newTopBelt: topBelt.slice(1),      // 先頭1文字を削除
//         newBottomBelt: bottomBelt.slice(1), // 先頭1文字を削除
//         removedPairs,
//         hasRemovals: true,
//         topAnimations,
//         bottomAnimations,
//         mergedElements
//       };
//     }
//   }
  
//   // ペアが見つからない場合はそのまま返す
//   return {
//     newTopBelt: topBelt,
//     newBottomBelt: bottomBelt,
//     removedPairs,
//     hasRemovals: false,
//     topAnimations,
//     bottomAnimations,
//     mergedElements: []
//   };
// };

// 全てのペアを順次消去（連続消去対応、アニメーション情報付き）
export const removeAllPairs = (topBelt: string, bottomBelt: string): PairRemovalResult => {
  const allRemovedPairs: Array<{ top: string; bottom: string; topIndex: number; bottomIndex: number }> = [];
  let currentTopBelt = topBelt;
  let currentBottomBelt = bottomBelt;
  let hasAnyRemovals = false;
  let pairIndex = 0;
  
  // 元の文字列の長さを記録
  const originalTopLength = topBelt.length;
  const originalBottomLength = bottomBelt.length;
  
  // アニメーション配列を初期化（全て normal 状態）
  const topAnimations: ElementAnimation[] = Array.from(topBelt).map(() => ({ state: 'normal' }));
  const bottomAnimations: ElementAnimation[] = Array.from(bottomBelt).map(() => ({ state: 'normal' }));
  
  // 先頭から順次チェックして消去可能なペアを全て処理
  let consumedTop = 0;
  let consumedBottom = 0;
  
  while (currentTopBelt.length > 0 && currentBottomBelt.length > 0) {
    const topChar = currentTopBelt[0];
    const bottomChar = currentBottomBelt[0];
    
    // 刺身（S）とタンポポ（T）のペアをチェック
    if ((topChar === 'S' && bottomChar === 'T') || (topChar === 'T' && bottomChar === 'S')) {
      // ペア発見！消去対象としてマーク
      allRemovedPairs.push({ 
        top: topChar, 
        bottom: bottomChar, 
        topIndex: consumedTop, 
        bottomIndex: consumedBottom 
      });
      
      // アニメーション状態を設定（消去対象）
      topAnimations[consumedTop] = { state: 'move-from-top', pairIndex };
      bottomAnimations[consumedBottom] = { state: 'move-from-bottom', pairIndex };
      
      currentTopBelt = currentTopBelt.slice(1);
      currentBottomBelt = currentBottomBelt.slice(1);
      consumedTop++;
      consumedBottom++;
      hasAnyRemovals = true;
      pairIndex++;
    } else {
      // ペアが見つからなければ終了
      break;
    }
  }
  
  // 残った要素に左詰めアニメーションを設定
  const slideDistance = consumedTop * 56; // 消去された要素数 × 56px
  
  for (let i = consumedTop; i < originalTopLength; i++) {
    if (consumedTop > 0) {
      topAnimations[i] = { state: 'slide-forward', slideDistance };
    }
  }
  
  for (let i = consumedBottom; i < originalBottomLength; i++) {
    if (consumedBottom > 0) {
      bottomAnimations[i] = { state: 'slide-forward', slideDistance };
    }
  }
  
  // 合体要素を生成（複数ペア対応）
  const mergedElements: MergedElement[] = allRemovedPairs.map((pair, index) => ({
    id: `merged-${Date.now()}-${index}`,
    pairIndex: index,
    topChar: pair.top,
    bottomChar: pair.bottom,
    position: { 
      x: (11 + 26.5)/2,
      y: (69 + 80)/2
    }
  }));

  return {
    newTopBelt: currentTopBelt,
    newBottomBelt: currentBottomBelt,
    removedPairs: allRemovedPairs,
    hasRemovals: hasAnyRemovals,
    topAnimations,
    bottomAnimations,
    mergedElements
  };
};

// クリア条件チェック（両レーンが空）
export const isCleared = (topBelt: string, bottomBelt: string): boolean => {
  return topBelt.length === 0 && bottomBelt.length === 0;
};