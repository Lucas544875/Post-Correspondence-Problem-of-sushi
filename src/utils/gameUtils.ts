import React from 'react';
import { GameIcon } from '../components/GameIcon';

// 文字列を画像アイコンの配列に変換（アニメーション用のクラスを指定可能）
export const renderGameString = (str: string, isShipping?: boolean): React.ReactNode[] => {
  return Array.from(str).map((char, index) => {
    const isHead = index === 0;
    const className = `mx-1 ${isShipping && isHead ? 'pair-shipping-head' : isShipping && !isHead ? 'slide-forward' : ''}`;
    
    if (char === 'S') {
      return React.createElement(GameIcon, { 
        key: index, 
        type: 'sashimi', 
        size: 'medium', 
        className 
      });
    } else if (char === 'T') {
      return React.createElement(GameIcon, { 
        key: index, 
        type: 'tampopo', 
        size: 'medium', 
        className 
      });
    }
    return React.createElement('span', { 
      key: index, 
      className: isShipping && !isHead ? 'slide-forward' : ''
    }, char);
  });
};

// 文字を画像タイプに変換
export const getIconType = (char: string): 'sashimi' | 'tampopo' | null => {
  if (char === 'S') return 'sashimi';
  if (char === 'T') return 'tampopo';
  return null;
};