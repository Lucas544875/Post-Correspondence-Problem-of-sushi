#!/usr/bin/env python3
"""
PCP問題ソルバー

このモジュールはPCP（ポスト対応問題）を解くためのソルバーを提供します。
深さ優先探索を用いて初期文字列付きPCP問題の解を探索します。
"""

from typing import List, Tuple, Optional, Set
from pcp_types import PCPInstance, PCPSolution
import time


class SimplePCPSolver:
    """シンプルなPCPソルバー（初期文字列対応）"""
    
    def __init__(self, instance: PCPInstance, max_depth: int = 20):
        """
        Args:
            instance: 解くPCP問題インスタンス
            max_depth: 最大探索深度
        """
        self.instance = instance
        self.max_depth = max_depth
        
    def solve(self) -> Optional[PCPSolution]:
        """問題を解いて解を返す"""
        start_time = time.time()
        
        # 初期文字列が既に一致している場合
        if (self.instance.initial_top == self.instance.initial_bottom and 
            len(self.instance.initial_top) > 0):
            solve_time = time.time() - start_time
            return PCPSolution(self.instance, [], solve_time)
        
        # 初期文字列から探索開始
        visited: Set[Tuple[str, str]] = set()
        sequence = self._dfs([], self.instance.initial_top, self.instance.initial_bottom, 0, visited)
        
        solve_time = time.time() - start_time
        
        if sequence is not None:
            return PCPSolution(self.instance, sequence, solve_time)
        else:
            return None
    
    def _dfs(self, sequence: List[int], top: str, bottom: str, depth: int, visited: Set[Tuple[str, str]]) -> Optional[List[int]]:
        """深さ優先探索"""
        # 文字列が一致した場合
        if top == bottom and len(top) > 0:
            return sequence.copy()
        
        # 最大深度到達
        if depth >= self.max_depth:
            return None
        
        # プルーニング
        if not (top.startswith(bottom) or bottom.startswith(top)):
            return None
        
        # 重複チェック
        state = (top, bottom)
        if state in visited:
            return None
        visited.add(state)
        
        # 各ドミノを試す
        for i, (dom_top, dom_bottom) in enumerate(self.instance.dominoes):
            new_sequence = sequence + [i]
            new_top = top + dom_top
            new_bottom = bottom + dom_bottom
            
            result = self._dfs(new_sequence, new_top, new_bottom, depth + 1, visited)
            if result is not None:
                return result
        
        visited.remove(state)
        return None


class OptimizedPCPSolver:
    """最適化されたPCPソルバー"""
    
    def __init__(self, instance: PCPInstance, max_depth: int = 20, time_limit: float = 5.0):
        """
        Args:
            instance: 解くPCP問題インスタンス
            max_depth: 最大探索深度
            time_limit: 制限時間（秒）
        """
        self.instance = instance
        self.max_depth = max_depth
        self.time_limit = time_limit
        self.start_time = 0.0
        
    def solve(self) -> Optional[PCPSolution]:
        """問題を解いて解を返す（時間制限付き）"""
        self.start_time = time.time()
        
        # 初期文字列が既に一致している場合
        if (self.instance.initial_top == self.instance.initial_bottom and 
            len(self.instance.initial_top) > 0):
            solve_time = time.time() - self.start_time
            return PCPSolution(self.instance, [], solve_time)
        
        # 初期文字列から探索開始
        visited: Set[Tuple[str, str]] = set()
        sequence = self._dfs_with_timeout([], self.instance.initial_top, self.instance.initial_bottom, 0, visited)
        
        solve_time = time.time() - self.start_time
        
        if sequence is not None:
            return PCPSolution(self.instance, sequence, solve_time)
        else:
            return None
    
    def _dfs_with_timeout(self, sequence: List[int], top: str, bottom: str, depth: int, visited: Set[Tuple[str, str]]) -> Optional[List[int]]:
        """時間制限付き深さ優先探索"""
        # 時間制限チェック
        if time.time() - self.start_time > self.time_limit:
            return None
        
        # 文字列が一致した場合
        if top == bottom and len(top) > 0:
            return sequence.copy()
        
        # 最大深度到達
        if depth >= self.max_depth:
            return None
        
        # 効果的なプルーニング
        if not self._can_match(top, bottom):
            return None
        
        # 重複チェック
        state = (top, bottom)
        if state in visited:
            return None
        visited.add(state)
        
        # 各ドミノを試す（ヒューリスティック順序）
        domino_indices = self._get_domino_order(top, bottom)
        for i in domino_indices:
            dom_top, dom_bottom = self.instance.dominoes[i]
            new_sequence = sequence + [i]
            new_top = top + dom_top
            new_bottom = bottom + dom_bottom
            
            result = self._dfs_with_timeout(new_sequence, new_top, new_bottom, depth + 1, visited)
            if result is not None:
                return result
        
        visited.remove(state)
        return None
    
    def _can_match(self, top: str, bottom: str) -> bool:
        """文字列が一致する可能性があるかチェック"""
        if not top and not bottom:
            return True
        if not top or not bottom:
            return True  # 一方が空の場合は可能性あり
        
        # 接頭辞チェック
        min_len = min(len(top), len(bottom))
        return top[:min_len] == bottom[:min_len]
    
    def _get_domino_order(self, top: str, bottom: str) -> List[int]:
        """ドミノの探索順序を決定（ヒューリスティック）"""
        indices = list(range(len(self.instance.dominoes)))
        
        # 文字列長の差を小さくするドミノを優先
        def priority(i: int) -> float:
            dom_top, dom_bottom = self.instance.dominoes[i]
            new_top = top + dom_top
            new_bottom = bottom + dom_bottom
            length_diff = abs(len(new_top) - len(new_bottom))
            
            # 長さの差が小さいほど優先度が高い
            return length_diff
        
        indices.sort(key=priority)
        return indices