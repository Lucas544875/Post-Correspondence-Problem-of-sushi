import React from 'react';
import { GameIcon } from '../components/GameIcon';

// 文字列を画像アイコンの配列に変換（アニメーション用のクラスを指定可能）
export const renderGameString = (str: string, isShipping?: boolean, size: 'small' | 'medium' | 'large' | 'relative' = 'medium', newItemsCount?: number): React.ReactNode[] => {
  const existingItemsCount = str.length - (newItemsCount || 0);
  // max-w-12 (48px) + mx-1 (8px margin) = 56px per item
  const itemWidthPx = 56;
  
  return Array.from(str).map((char, index) => {
    const isHead = index === 0;
    const isNewItem = newItemsCount && index >= str.length - newItemsCount;
    
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
    
    if (char === 'S') {
      return React.createElement(GameIcon, { 
        key: `${index}-${char}`, 
        type: 'sashimi', 
        size: size, 
        className,
        style
      });
    } else if (char === 'T') {
      return React.createElement(GameIcon, { 
        key: `${index}-${char}`, 
        type: 'tampopo', 
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
  });
};

// 文字を画像タイプに変換
export const getIconType = (char: string): 'sashimi' | 'tampopo' | null => {
  if (char === 'S') return 'sashimi';
  if (char === 'T') return 'tampopo';
  return null;
};