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

def main():
    """メイン実行関数 - 対話的にPCP問題を解く"""
    print("PCP問題ソルバー")
    print("=" * 30)
    
    while True:
        print("\n=== PCP問題入力 ===")
        
        # ドミノ数の入力
        try:
            num_dominoes = int(input("ドミノ数を入力してください: "))
            if num_dominoes <= 0:
                print("ドミノ数は1以上である必要があります。")
                continue
        except ValueError:
            print("有効な数値を入力してください。")
            continue
        
        # ドミノの入力
        dominoes = []
        print(f"\n{num_dominoes}個のドミノを入力してください:")
        for i in range(num_dominoes):
            print(f"ドミノ {i+1}:")
            top = input("  上部文字列: ").strip()
            bottom = input("  下部文字列: ").strip()
            dominoes.append((top, bottom))
        
        # 初期文字列の入力
        print("\n初期文字列を入力してください:")
        initial_top = input("上部初期文字列: ").strip()
        initial_bottom = input("下部初期文字列: ").strip()
        
        # 設定
        max_depth = int(input("\n最大探索深度 (デフォルト: 20): ") or "20")
        time_limit = float(input("制限時間（秒） (デフォルト: 5.0): ") or "5.0")
        
        try:
            # 問題インスタンス作成
            instance = PCPInstance(dominoes, initial_top, initial_bottom)
            print(f"\n{instance}")
            
            # ソルバー選択
            print("\nソルバーを選択してください:")
            print("1. シンプルソルバー")
            print("2. 最適化ソルバー")
            solver_choice = input("選択 (デフォルト: 2): ") or "2"
            
            if solver_choice == "1":
                solver = SimplePCPSolver(instance, max_depth)
            else:
                solver = OptimizedPCPSolver(instance, max_depth, time_limit)
            
            # 解探索実行
            print("\n=== 解探索中... ===")
            solution = solver.solve()
            
            # 結果表示
            if solution:
                print("\n=== 解が見つかりました！ ===")
                print(solution)
                print(f"\n使用ドミノの詳細:")
                for i, domino_idx in enumerate(solution.sequence):
                    top, bottom = instance.dominoes[domino_idx]
                    print(f"  {i+1}. ドミノ{domino_idx}: '{top}' / '{bottom}'")
            else:
                print("\n=== 解が見つかりませんでした ===")
                print("制限時間内または最大深度内で解は存在しないようです。")
                print("パラメータを調整してみてください。")
            
        except ValueError as e:
            print(f"エラー: {e}")
        except Exception as e:
            print(f"予期しないエラーが発生しました: {e}")
        
        # 継続確認
        if input("\n別の問題を解きますか？ (y/n): ").strip().lower() != 'y':
            break
    
    print("ソルバーを終了します。")


if __name__ == "__main__":
    main()
    