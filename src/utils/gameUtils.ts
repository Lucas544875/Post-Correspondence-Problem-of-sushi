import React from 'react';
import { GameIcon } from '../components/GameIcon';

// アニメーション状態の型定義
export type AnimationState = 'normal' | 'move-from-top' | 'move-from-bottom' | 'merged-appear' | 'merged-fade' | 'slide-forward';

// 各要素のアニメーション情報
export interface ElementAnimation {
  state: AnimationState;
  pairIndex?: number; // ペア消去の場合のペア番号
  slideDistance?: number; // スライドアニメーションの距離
}

// 文字列を画像アイコンの配列に変換（アニメーション用のクラスを指定可能）
export const renderGameString = (
  str: string, 
  isShipping?: boolean, 
  size: 'small' | 'medium' | 'large' | 'relative' = 'medium', 
  newItemsCount?: number, 
  hidePairHead?: boolean,
  elementAnimations?: ElementAnimation[]
): React.ReactNode[] => {
  const existingItemsCount = str.length - (newItemsCount || 0);
  // max-w-12 (48px) + mx-1 (8px margin) = 56px per item
  const itemWidthPx = 56;
  
  return Array.from(str).map((char, index) => {
    // const isHead = index === 0;
    const isNewItem = newItemsCount && index >= str.length - newItemsCount;
    const animation = elementAnimations?.[index];
    
    // ペアアニメーション中は先頭アイテムを非表示
    // if (hidePairHead && isHead) {
    //   return null;
    // }
    
    // 既存アイテムが占める幅を計算してスライド距離を決定
    const existingWidth = existingItemsCount * itemWidthPx;
    const slideDistance = `calc(max(${itemWidthPx}px, calc(100cqw - ${existingWidth}px)))`;
    
    // アニメーション状態に応じたクラス名を生成
    const animationClass = animation ? getAnimationClass(animation) : '';
    
    const className = `mx-1 ${
      animationClass ||
      (isShipping ? 'slide-forward' : 
      isNewItem ? 'belt-item-enter' : '')
    }`;
    
    const style = {
      ...(isNewItem ? { '--slide-distance': slideDistance } : {}),
      ...(animation?.pairIndex !== undefined ? { '--pair-index': animation.pairIndex } : {}),
      ...(animation?.slideDistance !== undefined ? { '--empty-space': `-${animation.slideDistance}px` } : {})
    } as React.CSSProperties;
    
    if (char === 'S' || char === 'T') {
      const iconType = getIconType(char, animation);
      return React.createElement(GameIcon, { 
        key: `${index}-${char}`, 
        type: iconType!, 
        size: size, 
        className,
        style
      });
    }
    return React.createElement('span', { 
      key: `${index}-${char}`, 
      className: className,
      style
    }, char);
  }).filter(Boolean);
};

// アニメーション状態に応じたCSSクラス名を返す
const getAnimationClass = (animation: ElementAnimation): string => {
  switch (animation.state) {
    case 'move-from-top':
      return 'pair-item-top-moving';
    case 'move-from-bottom':
      return 'pair-item-bottom-moving';
    case 'merged-appear':
      return 'pair-merged-item';
    case 'merged-fade':
      return 'pair-merged-item-fade';
    case 'slide-forward':
      return 'slide-forward';
    default:
      return '';
  }
};

// 文字を画像タイプに変換
export const getIconType = (char: string,  animation?: ElementAnimation): 'sashimi' | 'tampopo' | 'tampopo_on_sashimi' | null => {
  // 合体アニメーション中は合体画像を表示
  // if (animation?.state === 'merged-appear' || animation?.state === 'merged-fade') {
  //   return 'tampopo_on_sashimi';
  // }
  // if (isShippingHead) return 'tampopo_on_sashimi';
  if (char === 'S') return 'sashimi';
  if (char === 'T') return 'tampopo';
  return null;
};