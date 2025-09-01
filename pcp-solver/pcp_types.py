#!/usr/bin/env python3
"""
PCP問題のデータ型定義

このモジュールはPCP（ポスト対応問題）の基本データ型を定義します。
- PCPInstance: 問題インスタンスを表現
- PCPSolution: 解を表現
"""

from dataclasses import dataclass, asdict
from typing import List, Tuple, Dict


@dataclass
class PCPInstance:
    """PCP問題インスタンスを表すクラス"""
    
    dominoes: List[Tuple[str, str]]
    initial_top: str = ""
    initial_bottom: str = ""
    
    def __post_init__(self):
        """初期化後の検証"""
        if not self.dominoes:
            raise ValueError("ドミノセットが空です")
        
        for i, (top, bottom) in enumerate(self.dominoes):
            if not isinstance(top, str) or not isinstance(bottom, str):
                raise ValueError(f"ドミノ {i} の文字列が無効です")
    
    @property
    def domino_count(self) -> int:
        """ドミノの数"""
        return len(self.dominoes)
    
    @property
    def alphabet(self) -> set:
        """使用されている文字の集合"""
        chars = set()
        for top, bottom in self.dominoes:
            chars.update(top)
            chars.update(bottom)
        chars.update(self.initial_top)
        chars.update(self.initial_bottom)
        return chars
    
    @property
    def max_domino_length(self) -> int:
        """最大ドミノ文字列長"""
        if not self.dominoes:
            return 0
        return max(max(len(top), len(bottom)) for top, bottom in self.dominoes)
    
    def get_domino(self, index: int) -> Tuple[str, str]:
        """指定インデックスのドミノを取得"""
        if not 0 <= index < len(self.dominoes):
            raise IndexError(f"ドミノインデックス {index} が範囲外です")
        return self.dominoes[index]
    
    def has_initial_strings(self) -> bool:
        """初期文字列が設定されているかチェック"""
        return bool(self.initial_top or self.initial_bottom)
    
    def to_dict(self) -> Dict:
        """辞書形式に変換"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'PCPInstance':
        """辞書から生成"""
        return cls(**data)
    
    def __str__(self) -> str:
        """文字列表現"""
        lines = [f"PCP問題インスタンス ({self.domino_count}ドミノ)"]
        
        if self.has_initial_strings():
            lines.append(f"初期文字列: '{self.initial_top}' / '{self.initial_bottom}'")
        
        lines.append("ドミノ:")
        for i, (top, bottom) in enumerate(self.dominoes):
            lines.append(f"  {i}: '{top}' / '{bottom}'")
        
        return "\n".join(lines)
    
    def validate_solution(self, solution: List[int]) -> Tuple[bool, str]:
        """解の妥当性をチェック"""
        if not solution and not self.has_initial_strings():
            return False, "解が空で初期文字列も設定されていません"
        
        # インデックスの範囲チェック
        for i, domino_idx in enumerate(solution):
            if not 0 <= domino_idx < len(self.dominoes):
                return False, f"解の位置 {i} のドミノインデックス {domino_idx} が無効です"
        
        # 文字列構築と一致チェック
        top_str = self.initial_top
        bottom_str = self.initial_bottom
        
        for domino_idx in solution:
            dom_top, dom_bottom = self.dominoes[domino_idx]
            top_str += dom_top
            bottom_str += dom_bottom
        
        if top_str == bottom_str and len(top_str) > 0:
            return True, f"有効な解: '{top_str}'"
        else:
            return False, f"文字列が一致しません: '{top_str}' != '{bottom_str}'"


@dataclass
class PCPSolution:
    """PCP問題の解を表すクラス"""
    
    instance: PCPInstance
    sequence: List[int]
    solve_time: float = 0.0
    
    def __post_init__(self):
        """解の妥当性チェック"""
        is_valid, message = self.instance.validate_solution(self.sequence)
        if not is_valid:
            raise ValueError(f"無効な解: {message}")
    
    @property
    def length(self) -> int:
        """解の長さ"""
        return len(self.sequence)
    
    @property
    def final_string(self) -> str:
        """最終的に生成される文字列"""
        top_str = self.instance.initial_top
        for domino_idx in self.sequence:
            dom_top, _ = self.instance.dominoes[domino_idx]
            top_str += dom_top
        return top_str
    
    @property
    def domino_usage(self) -> Dict[int, int]:
        """各ドミノの使用回数"""
        usage = {}
        for domino_idx in self.sequence:
            usage[domino_idx] = usage.get(domino_idx, 0) + 1
        return usage
    
    @property
    def diversity_score(self) -> float:
        """解の多様性スコア（異なるドミノ数/総ドミノ使用数）"""
        if not self.sequence:
            return 0.0
        if len(set(self.sequence)) != len(self.sequence):
            return 0.0
        domino_length_sum = sum(len(top) + len(bottom) for top, bottom in self.instance.dominoes)
        return min(1.0, domino_length_sum / 8)
    
    def to_dict(self) -> Dict:
        """辞書形式に変換"""
        return {
            'instance': self.instance.to_dict(),
            'sequence': self.sequence,
            'solve_time': self.solve_time,
            'length': self.length,
            'final_string': self.final_string,
            'diversity_score': self.diversity_score
        }
    
    def __str__(self) -> str:
        """文字列表現"""
        lines = [f"PCP解 (長さ: {self.length})"]
        lines.append(f"シーケンス: {self.sequence}")
        lines.append(f"最終文字列: '{self.final_string}'")
        lines.append(f"解答時間: {self.solve_time:.4f}秒")
        lines.append(f"多様性: {self.diversity_score:.2f}")
        return "\n".join(lines)