// ペア消去ロジック

export interface PairRemovalResult {
  newTopBelt: string;
  newBottomBelt: string;
  removedPairs: Array<{ top: string; bottom: string }>;
  hasRemovals: boolean;
}

// 先頭の一組だけをチェックして消去（一回につき1ペアのみ）
export const removePairs = (topBelt: string, bottomBelt: string): PairRemovalResult => {
  const removedPairs: Array<{ top: string; bottom: string }> = [];
  
  // 両方のレーンに文字がある場合のみチェック
  if (topBelt.length > 0 && bottomBelt.length > 0) {
    const topChar = topBelt[0];
    const bottomChar = bottomBelt[0];
    
    // 刺身（S）とタンポポ（T）のペアをチェック
    if ((topChar === 'S' && bottomChar === 'T') || (topChar === 'T' && bottomChar === 'S')) {
      // ペア発見！先頭の1文字ずつを消去
      removedPairs.push({ top: topChar, bottom: bottomChar });
      
      return {
        newTopBelt: topBelt.slice(1),      // 先頭1文字を削除
        newBottomBelt: bottomBelt.slice(1), // 先頭1文字を削除
        removedPairs,
        hasRemovals: true
      };
    }
  }
  
  // ペアが見つからない場合はそのまま返す
  return {
    newTopBelt: topBelt,
    newBottomBelt: bottomBelt,
    removedPairs,
    hasRemovals: false
  };
};

// クリア条件チェック（両レーンが空）
export const isCleared = (topBelt: string, bottomBelt: string): boolean => {
  return topBelt.length === 0 && bottomBelt.length === 0;
};