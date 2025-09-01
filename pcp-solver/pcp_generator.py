#!/usr/bin/env python3
"""
PCP問題インスタンス生成器

このモジュールは制約付きPCP問題のインスタンスを系統的に生成・探索し、
解の存在を確認して高品質な問題セットを生成します。
"""

import itertools
import json
import time
from typing import List, Tuple, Dict, Iterator
from pcp_types import PCPInstance, PCPSolution
from pcp_solver import SimplePCPSolver, OptimizedPCPSolver


class ConstrainedPCPGenerator:
    """制約付きPCP問題の生成・探索クラス"""
    
    def __init__(self, max_depth: int = 15, time_limit: float = 2.0):
        """
        Args:
            max_depth: ソルバーの最大探索深度
            time_limit: 1問題あたりの制限時間
        """
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
                for initial_top, initial_bottom in self._generate_initial_pairs(chars, 3):
                    if samples_tested >= max_samples:
                        break
                    
                    samples_tested += 1
                    
                    # 問題インスタンス作成
                    try:
                        instance = PCPInstance(dominoes, initial_top, initial_bottom)
                        
                        # ソルバーで解を探索
                        solver = OptimizedPCPSolver(instance, self.max_depth, self.time_limit)
                        solution = solver.solve()
                        
                        if solution is not None and solution.solve_time < self.time_limit:
                            # 品質評価
                            quality = self._evaluate_quality(solution)
                            
                            problem = {
                                'dominoes': dominoes,
                                'initial_top': initial_top,
                                'initial_bottom': initial_bottom,
                                'solution': solution.sequence,
                                'solution_length': solution.length,
                                'solve_time': solution.solve_time,
                                'quality_score': quality,
                                'difficulty': self._classify_difficulty(solution),
                                'final_string': solution.final_string,
                                'diversity_score': solution.diversity_score
                            }
                            
                            found_problems.append(problem)
                            print(f"発見 #{len(found_problems)}: 品質={quality:.2f}, "
                                  f"解長={solution.length}, 初期='{initial_top}'/'{initial_bottom}'")
                        
                    except (ValueError, Exception) as e:
                        # 無効な問題インスタンスはスキップ
                        continue
                    
                    if samples_tested % 20 == 0:
                        print(f"進捗: {samples_tested}/{max_samples}")
        
        print(f"\n探索完了: {len(found_problems)} 問題発見")
        return found_problems
    
    def _generate_domino_combinations(self, chars: List[str], num_dominoes: int, max_len: int) -> Iterator[List[Tuple[str, str]]]:
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
    
    def _generate_initial_pairs(self, chars: List[str], max_len: int) -> Iterator[Tuple[str, str]]:
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
    
    def _evaluate_quality(self, solution: PCPSolution) -> float:
        """問題の品質を評価（0-1スコア）"""
        score = 0.0
        
        # 解の長さ評価（2-5が理想的）
        solution_length = solution.length
        if 2 <= solution_length <= 5:
            length_score = 1.0 - abs(solution_length - 3.5) / 3.5
        else:
            length_score = max(0, 1.0 - abs(solution_length - 3.5) / 10)
        score += length_score * 0.4
        
        # 解答時間評価（0.1-1.0秒が理想）
        solve_time = solution.solve_time
        if 0.01 <= solve_time <= 1.0:
            time_score = min(1.0, solve_time / 0.5)
        else:
            time_score = 0.2
        score += time_score * 0.3
        
        # ドミノの多様性
        if solution.sequence:
            score += solution.diversity_score * 0.2
        
        # 初期文字列の複雑さ
        initial_complexity = min(1.0, (len(solution.instance.initial_top) + len(solution.instance.initial_bottom)) / 4)
        score += initial_complexity * 0.1
        
        return min(1.0, score)
    
    def _classify_difficulty(self, solution: PCPSolution) -> str:
        """難易度分類"""
        if solution.length <= 2 and solution.solve_time < 0.1:
            return "easy"
        elif solution.length <= 4 and solution.solve_time < 0.5:
            return "medium"
        else:
            return "hard"
    
    def generate_game_problem_set(self, target_count: int = 15, sreshold: int = 3) -> Dict:
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
    
    def generate_custom_problems(self, chars: List[str], domino_count_range: Tuple[int, int], 
                                max_string_length: int, sample_limit: int = 50) -> List[Dict]:
        """カスタム問題生成"""
        print(f"=== カスタム問題生成 ===")
        print(f"文字: {chars}")
        print(f"ドミノ数範囲: {domino_count_range}")
        print(f"最大文字列長: {max_string_length}")
        
        found_problems = []
        samples_tested = 0
        
        min_dominoes, max_dominoes = domino_count_range
        
        for num_dominoes in range(min_dominoes, max_dominoes + 1):
            print(f"\nドミノ数 {num_dominoes} での探索...")
            
            for dominoes in self._generate_domino_combinations(chars, num_dominoes, max_string_length):
                if samples_tested >= sample_limit:
                    break
                
                for initial_top, initial_bottom in self._generate_initial_pairs(chars, max_string_length):
                    if samples_tested >= sample_limit:
                        break
                    
                    samples_tested += 1
                    
                    try:
                        instance = PCPInstance(dominoes, initial_top, initial_bottom)
                        solver = OptimizedPCPSolver(instance, self.max_depth, self.time_limit)
                        solution = solver.solve()
                        
                        if solution is not None:
                            quality = self._evaluate_quality(solution)
                            
                            problem = {
                                'dominoes': dominoes,
                                'initial_top': initial_top,
                                'initial_bottom': initial_bottom,
                                'solution': solution.sequence,
                                'solution_length': solution.length,
                                'solve_time': solution.solve_time,
                                'quality_score': quality,
                                'difficulty': self._classify_difficulty(solution),
                                'final_string': solution.final_string,
                                'diversity_score': solution.diversity_score
                            }
                            
                            found_problems.append(problem)
                            
                    except (ValueError, Exception):
                        continue
                    
                    if samples_tested % 10 == 0:
                        print(f"進捗: {samples_tested}/{sample_limit}")
        
        print(f"\n生成完了: {len(found_problems)} 問題発見")
        return found_problems