#!/usr/bin/env python3
"""
初期文字列付きPCP問題の探索スクリプト

このスクリプトは制約条件を満たすPCP問題インスタンスを系統的に探索し、
解の存在を確認して高品質な問題セットを生成します。
"""

import itertools
import json
import time
import random
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass, asdict

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
        return len(set(self.sequence)) / len(self.sequence)
    
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

# PCPソルバーの基本クラスを直接定義
class SimplePCPSolver:
    """シンプルなPCPソルバー（初期文字列対応）"""
    
    def __init__(self, dominoes: List[Tuple[str, str]], max_depth: int = 20, 
                 initial_top: str = "", initial_bottom: str = ""):
        self.dominoes = dominoes
        self.max_depth = max_depth
        self.initial_top = initial_top
        self.initial_bottom = initial_bottom
        
    def solve(self) -> Optional[List[int]]:
        """問題を解いて解のシーケンスを返す"""
        # 初期文字列が既に一致している場合
        if self.initial_top == self.initial_bottom and len(self.initial_top) > 0:
            return []
        
        # 初期文字列から探索開始
        visited = set()
        return self._dfs([], self.initial_top, self.initial_bottom, 0, visited)
    
    def _dfs(self, sequence: List[int], top: str, bottom: str, depth: int, visited: set) -> Optional[List[int]]:
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
        for i, (dom_top, dom_bottom) in enumerate(self.dominoes):
            new_sequence = sequence + [i]
            new_top = top + dom_top
            new_bottom = bottom + dom_bottom
            
            result = self._dfs(new_sequence, new_top, new_bottom, depth + 1, visited)
            if result is not None:
                return result
        
        visited.remove(state)
        return None

class ConstrainedPCPSearcher:
    """制約付きPCP問題の探索クラス"""
    
    def __init__(self, max_depth: int = 15, time_limit: float = 2.0):
        self.max_depth = max_depth
        self.time_limit = time_limit
    
    def search_sushi_problems(self, max_samples: int = 100) -> List[Dict]:
        """寿司テーマの問題を探索"""
        print("=== 寿司テーマPCP問題探索 ===")
        
        chars = ['S', 'T']  # 刺身とタンポポ
        found_problems = []
        samples_tested = 0
        
        # ドミノ数2-3での探索
        for num_dominoes in [2, 3]:
            print(f"\nドミノ数 {num_dominoes} での探索...")
            
            # ドミノの組み合わせを生成
            for dominoes in self._generate_domino_combinations(chars, num_dominoes, 2):
                if samples_tested >= max_samples:
                    break
                
                # 初期文字列の組み合わせ
                for initial_top, initial_bottom in self._generate_initial_pairs(chars, 2):
                    if samples_tested >= max_samples:
                        break
                    
                    samples_tested += 1
                    
                    # ソルバーで解を探索
                    start_time = time.time()
                    solver = SimplePCPSolver(dominoes, self.max_depth, initial_top, initial_bottom)
                    solution = solver.solve()
                    solve_time = time.time() - start_time
                    
                    if solution is not None and solve_time < self.time_limit:
                        # 品質評価
                        quality = self._evaluate_quality(solution, solve_time, dominoes, initial_top, initial_bottom)
                        
                        problem = {
                            'dominoes': dominoes,
                            'initial_top': initial_top,
                            'initial_bottom': initial_bottom,
                            'solution': solution,
                            'solution_length': len(solution),
                            'solve_time': solve_time,
                            'quality_score': quality,
                            'difficulty': self._classify_difficulty(solution, solve_time)
                        }
                        
                        found_problems.append(problem)
                        print(f"発見 #{len(found_problems)}: 品質={quality:.2f}, "
                              f"解長={len(solution)}, 初期='{initial_top}'/'{initial_bottom}'")
                    
                    if samples_tested % 20 == 0:
                        print(f"進捗: {samples_tested}/{max_samples}")
        
        print(f"\n探索完了: {len(found_problems)} 問題発見")
        return found_problems
    
    def _generate_domino_combinations(self, chars: List[str], num_dominoes: int, max_len: int):
        """ドミノの組み合わせ生成"""
        # 可能な文字列（空文字列含む）
        strings = ['']
        for length in range(1, max_len + 1):
            for combo in itertools.product(chars, repeat=length):
                strings.append(''.join(combo))
        
        # ドミノの組み合わせ
        for domino_combo in itertools.combinations_with_replacement(
                itertools.product(strings, strings), num_dominoes):
            yield list(domino_combo)
    
    def _generate_initial_pairs(self, chars: List[str], max_len: int):
        """初期文字列ペアの生成"""
        strings = ['']
        for length in range(1, max_len + 1):
            for combo in itertools.product(chars, repeat=length):
                strings.append(''.join(combo))
        
        for top in strings:
            for bottom in strings:
                # 興味深い組み合わせのみ選択
                if len(top) + len(bottom) <= 3:  # 合計長制限
                    yield (top, bottom)
    
    def _evaluate_quality(self, solution: List[int], solve_time: float, 
                         dominoes: List[Tuple[str, str]], initial_top: str, initial_bottom: str) -> float:
        """問題の品質を評価（0-1スコア）"""
        score = 0.0
        
        # 解の長さ評価（2-5が理想的）
        solution_length = len(solution)
        if 2 <= solution_length <= 5:
            length_score = 1.0 - abs(solution_length - 3.5) / 3.5
        else:
            length_score = max(0, 1.0 - abs(solution_length - 3.5) / 10)
        score += length_score * 0.4
        
        # 解答時間評価（0.1-1.0秒が理想）
        if 0.01 <= solve_time <= 1.0:
            time_score = min(1.0, solve_time / 0.5)
        else:
            time_score = 0.2
        score += time_score * 0.3
        
        # ドミノの多様性
        if solution:
            diversity = len(set(solution)) / len(solution)
            score += diversity * 0.2
        
        # 初期文字列の複雑さ
        initial_complexity = min(1.0, (len(initial_top) + len(initial_bottom)) / 4)
        score += initial_complexity * 0.1
        
        return min(1.0, score)
    
    def _classify_difficulty(self, solution: List[int], solve_time: float) -> str:
        """難易度分類"""
        if len(solution) <= 2 and solve_time < 0.1:
            return "easy"
        elif len(solution) <= 4 and solve_time < 0.5:
            return "medium"
        else:
            return "hard"
    
    def generate_game_problem_set(self, target_count: int = 15) -> Dict:
        """ゲーム用問題セットを生成"""
        print(f"=== ゲーム用問題セット生成 (目標: {target_count}問題) ===")
        
        # 大規模探索
        all_problems = self.search_sushi_problems(max_samples=200)
        
        if not all_problems:
            print("問題が見つかりませんでした。")
            return {'problems': [], 'statistics': {'total_found': 0}}
        
        # 品質順にソート
        all_problems.sort(key=lambda p: p['quality_score'], reverse=True)
        
        # 難易度別に分類
        easy_problems = [p for p in all_problems if p['difficulty'] == 'easy']
        medium_problems = [p for p in all_problems if p['difficulty'] == 'medium']
        hard_problems = [p for p in all_problems if p['difficulty'] == 'hard']
        
        # バランスよく選択
        easy_count = min(len(easy_problems), target_count // 3)
        medium_count = min(len(medium_problems), target_count // 3)
        hard_count = min(len(hard_problems), target_count - easy_count - medium_count)
        
        selected_problems = (
            easy_problems[:easy_count] + 
            medium_problems[:medium_count] + 
            hard_problems[:hard_count]
        )
        
        problem_set = {
            'name': 'sushi_constrained_pcp_problems',
            'description': '制約付き探索で生成された寿司テーマPCP問題セット',
            'generated_at': time.strftime('%Y-%m-%d %H:%M:%S'),
            'problems': selected_problems,
            'statistics': {
                'total_found': len(all_problems),
                'easy_found': len(easy_problems),
                'medium_found': len(medium_problems),
                'hard_found': len(hard_problems),
                'selected_total': len(selected_problems),
                'avg_quality': sum(p['quality_score'] for p in selected_problems) / len(selected_problems) if selected_problems else 0
            }
        }
        
        return problem_set

def main():
    """メイン実行関数"""
    print("初期文字列付きPCP問題探索ツール")
    print("=" * 50)
    
    searcher = ConstrainedPCPSearcher(max_depth=12, time_limit=1.0)
    
    while True:
        print("\n選択してください:")
        print("1. 寿司問題の探索実行")
        print("2. ゲーム用問題セット生成")
        print("3. カスタム探索")
        print("0. 終了")
        
        try:
            choice = input("\n選択: ").strip()
            
            if choice == "0":
                print("終了します。")
                break
            elif choice == "1":
                # 寿司問題探索
                problems = searcher.search_sushi_problems(max_samples=50)
                if problems:
                    print(f"\n=== 発見された上位5問題 ===")
                    for i, problem in enumerate(problems[:5]):
                        print(f"\n問題 {i+1}:")
                        print(f"  ドミノ: {problem['dominoes']}")
                        print(f"  初期: '{problem['initial_top']}' / '{problem['initial_bottom']}'")
                        print(f"  解: {problem['solution']}")
                        print(f"  品質: {problem['quality_score']:.2f}")
                        print(f"  難易度: {problem['difficulty']}")
                
            elif choice == "2":
                # ゲーム用問題セット生成
                target_count = int(input("生成する問題数 (デフォルト: 10): ") or "10")
                problem_set = searcher.generate_game_problem_set(target_count)
                
                print(f"\n=== 生成結果 ===")
                stats = problem_set['statistics']
                print(f"発見総数: {stats['total_found']}")
                print(f"Easy: {stats['easy_found']}, Medium: {stats['medium_found']}, Hard: {stats['hard_found']}")
                print(f"選択数: {stats['selected_total']}")
                print(f"平均品質: {stats['avg_quality']:.2f}")
                
                # 保存オプション
                save = input("\nJSONファイルに保存しますか？ (y/n): ").strip().lower()
                if save == 'y':
                    filename = input("ファイル名 (デフォルト: sushi_problems.json): ") or "sushi_problems.json"
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(problem_set, f, ensure_ascii=False, indent=2)
                    print(f"問題セットを {filename} に保存しました。")
                
                # サンプル表示
                if problem_set['problems']:
                    print(f"\n=== サンプル問題 ===")
                    sample = problem_set['problems'][0]
                    print(f"ドミノ: {sample['dominoes']}")
                    print(f"初期文字列: '{sample['initial_top']}' / '{sample['initial_bottom']}'")
                    print(f"解: {sample['solution']}")
                
            elif choice == "3":
                # カスタム探索
                print("\n=== カスタム探索 ===")
                max_samples = int(input("最大サンプル数 (デフォルト: 30): ") or "30")
                problems = searcher.search_sushi_problems(max_samples=max_samples)
                print(f"{len(problems)} 問題が見つかりました。")
            else:
                print("無効な選択です。")
                
        except KeyboardInterrupt:
            print("\n\n処理が中断されました。")
            break
        except Exception as e:
            print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    main()