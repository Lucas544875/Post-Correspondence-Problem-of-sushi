#!/usr/bin/env python3
"""
ポスト対応問題（Post Correspondence Problem）の探索スクリプト

ポスト対応問題とは：
- 有限個のドミノ（上部・下部に文字列が書かれたカード）が与えられる
- これらのドミノを任意の順序で任意回数使用して配列を作成
- 配列の上部文字列と下部文字列が一致する配列が存在するかを判定する問題

このスクリプトは深さ優先探索とブランチング技術を使用して解を探索します。
"""

from typing import List, Tuple, Set, Optional
from collections import deque
import time

class PCPSolver:
    def __init__(self, dominoes: List[Tuple[str, str]], max_depth: int = 20):
        """
        PCPソルバーを初期化
        
        Args:
            dominoes: ドミノのリスト [(上部文字列, 下部文字列), ...]
            max_depth: 最大探索深度
        """
        self.dominoes = dominoes
        self.max_depth = max_depth
        self.visited = set()  # 重複状態を避けるためのセット
        self.solution = None
        
    def solve(self) -> Optional[List[int]]:
        """
        ポスト対応問題を解く
        
        Returns:
            解が存在する場合はドミノのインデックスリスト、存在しない場合はNone
        """
        print(f"ドミノ: {self.dominoes}")
        print(f"最大探索深度: {self.max_depth}")
        print("探索開始...")
        
        start_time = time.time()
        
        # 各ドミノから探索開始
        for i, domino in enumerate(self.dominoes):
            self.visited.clear()
            result = self._dfs([i], domino[0], domino[1], 1)
            if result:
                self.solution = result
                break
                
        end_time = time.time()
        
        print(f"探索時間: {end_time - start_time:.4f}秒")
        
        if self.solution:
            print(f"解が見つかりました: {self.solution}")
            self._print_solution(self.solution)
            return self.solution
        else:
            print("解が見つかりませんでした")
            return None
    
    def _dfs(self, sequence: List[int], top: str, bottom: str, depth: int) -> Optional[List[int]]:
        """
        深さ優先探索
        
        Args:
            sequence: 現在のドミノ配列
            top: 現在の上部文字列
            bottom: 現在の下部文字列
            depth: 現在の探索深度
            
        Returns:
            解が見つかった場合はドミノのインデックスリスト、そうでなければNone
        """
        # 文字列が一致した場合
        if top == bottom and len(top) > 0:
            return sequence.copy()
        
        # 最大深度に達した場合
        if depth >= self.max_depth:
            return None
        
        # プルーニング: 一方の文字列が他方の接頭辞でない場合は探索を打ち切り
        if not (top.startswith(bottom) or bottom.startswith(top)):
            return None
        
        # 状態の重複チェック
        state = (top, bottom, tuple(sequence))
        if state in self.visited:
            return None
        self.visited.add(state)
        
        # 各ドミノを追加して再帰探索
        for i, (dom_top, dom_bottom) in enumerate(self.dominoes):
            new_sequence = sequence + [i]
            new_top = top + dom_top
            new_bottom = bottom + dom_bottom
            
            result = self._dfs(new_sequence, new_top, new_bottom, depth + 1)
            if result:
                return result
        
        return None
    
    def _print_solution(self, solution: List[int]):
        """解の詳細を出力"""
        print("\n=== 解の詳細 ===")
        top_string = ""
        bottom_string = ""
        
        for i, domino_idx in enumerate(solution):
            domino = self.dominoes[domino_idx]
            top_string += domino[0]
            bottom_string += domino[1]
            
            print(f"ステップ {i+1}: ドミノ{domino_idx+1} {domino}")
            print(f"  上部: {top_string}")
            print(f"  下部: {bottom_string}")
            print()
        
        print(f"最終結果:")
        print(f"上部: {top_string}")
        print(f"下部: {bottom_string}")
        print(f"一致: {'OK' if top_string == bottom_string else 'NG'}")

def create_sample_problems():
    """サンプル問題を作成"""
    problems = {
        "簡単な問題": [
            ("a", "aa"),
            ("aa", "a")
        ],
        "中程度の問題": [
            ("ab", "aba"),
            ("baa", "aa"),
            ("aba", "bab")
        ],
        "難しい問題": [
            ("abc", "ab"),
            ("ca", "a"),
            ("acc", "ba")
        ],
        "寿司問題": [
            ("s", "ss"),
            ("ss", "s"),
            ("b", "bb"),
            ("bb", "b")
        ]
    }
    return problems

def main():
    """メイン関数"""
    print("=== ポスト対応問題ソルバー ===\n")
    
    problems = create_sample_problems()
    
    while True:
        print("問題を選択してください:")
        problem_names = list(problems.keys())
        for i, name in enumerate(problem_names, 1):
            print(f"{i}. {name}")
        print(f"{len(problem_names) + 1}. カスタム問題を入力")
        print("0. 終了")
        
        try:
            choice = int(input("\n選択: "))
            
            if choice == 0:
                print("終了します。")
                break
            elif 1 <= choice <= len(problem_names):
                selected_problem = problems[problem_names[choice - 1]]
                print(f"\n選択された問題: {problem_names[choice - 1]}")
            elif choice == len(problem_names) + 1:
                selected_problem = input_custom_problem()
            else:
                print("無効な選択です。")
                continue
            
            # 最大探索深度の設定
            max_depth = int(input("最大探索深度を入力してください (デフォルト: 20): ") or "20")
            
            # 問題を解く
            solver = PCPSolver(selected_problem, max_depth)
            solution = solver.solve()
            
            print("\n" + "="*50 + "\n")
            
        except ValueError:
            print("有効な数値を入力してください。")
        except KeyboardInterrupt:
            print("\n\n処理が中断されました。")
            break

def input_custom_problem():
    """カスタム問題の入力"""
    print("\nカスタム問題を入力してください:")
    print("形式: 上部文字列,下部文字列")
    print("例: abc,ab")
    print("終了するには空行を入力してください")
    
    dominoes = []
    while True:
        line = input(f"ドミノ {len(dominoes) + 1}: ").strip()
        if not line:
            break
        
        try:
            top, bottom = line.split(',')
            dominoes.append((top.strip(), bottom.strip()))
        except ValueError:
            print("形式が正しくありません。'上部,下部'の形式で入力してください。")
    
    if not dominoes:
        print("ドミノが入力されませんでした。デフォルト問題を使用します。")
        return [("a", "aa"), ("aa", "a")]
    
    return dominoes

if __name__ == "__main__":
    main()