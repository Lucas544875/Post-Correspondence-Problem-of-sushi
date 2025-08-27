// 絵文字を正しく分割するユーティリティ関数
export const splitEmoji = (str: string): string[] => {
  // Array.from()はサロゲートペアを正しく処理する
  return Array.from(str);
};

// 文字列の正しい長さを取得
export const getEmojiLength = (str: string): number => {
  return Array.from(str).length;
};