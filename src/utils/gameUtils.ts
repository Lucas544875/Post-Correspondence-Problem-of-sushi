import React from 'react';
import { GameIcon } from '../components/GameIcon';

// 文字列を画像アイコンの配列に変換（アニメーション用のクラスを指定可能）
export const renderGameString = (str: string, isShipping?: boolean, size: 'small' | 'medium' | 'large' | 'relative' = 'medium', newItemsCount?: number, hidePairHead?: boolean): React.ReactNode[] => {
  const existingItemsCount = str.length - (newItemsCount || 0);
  // max-w-12 (48px) + mx-1 (8px margin) = 56px per item
  const itemWidthPx = 56;
  
  return Array.from(str).map((char, index) => {
    const isHead = index === 0;
    const isNewItem = newItemsCount && index >= str.length - newItemsCount;
    
    // ペアアニメーション中は先頭アイテムを非表示
    if (hidePairHead && isHead) {
      return null;
    }
    
    // 既存アイテムが占める幅を計算してスライド距離を決定
    const existingWidth = existingItemsCount * itemWidthPx;
    const slideDistance = `calc(max(${itemWidthPx}px, calc(100cqw - ${existingWidth}px)))`;
    
    const className = `mx-1 ${
      isShipping && isHead ? 'pair-shipping-head' : 
      isShipping && !isHead ? 'slide-forward' : 
      isNewItem ? 'belt-item-enter' : ''
    }`;
    
    const style = isNewItem ? {
      '--slide-distance': slideDistance
    } as React.CSSProperties : {};
    
    if (char === 'S' || char === 'T') {
      const iconType = getIconType(char, isShipping && isHead);
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
      className: isShipping && !isHead ? 'slide-forward' : isNewItem ? 'belt-item-enter' : '',
      style
    }, char);
  }).filter(Boolean);
};

// 文字を画像タイプに変換
export const getIconType = (char: string, isShippingHead?: boolean): 'sashimi' | 'tampopo' | 'tampopo_on_sashimi' | null => {
  if (isShippingHead) return 'tampopo_on_sashimi';
  if (char === 'S') return 'sashimi';
  if (char === 'T') return 'tampopo';
  return null;
};