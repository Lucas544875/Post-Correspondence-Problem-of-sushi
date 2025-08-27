import React from 'react';
import { GameIcon } from '../components/GameIcon';

// 文字列を画像アイコンの配列に変換
export const renderGameString = (str: string): React.ReactNode[] => {
  return Array.from(str).map((char, index) => {
    if (char === 'S') {
      return React.createElement(GameIcon, { 
        key: index, 
        type: 'sashimi', 
        size: 'medium', 
        className: 'mx-1' 
      });
    } else if (char === 'T') {
      return React.createElement(GameIcon, { 
        key: index, 
        type: 'tampopo', 
        size: 'medium', 
        className: 'mx-1' 
      });
    }
    return React.createElement('span', { key: index }, char);
  });
};

// 文字を画像タイプに変換
export const getIconType = (char: string): 'sashimi' | 'tampopo' | null => {
  if (char === 'S') return 'sashimi';
  if (char === 'T') return 'tampopo';
  return null;
};