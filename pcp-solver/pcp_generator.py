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
    
    def search_sushi_problems(self, max_samples: int = 100, sreshold: int = 3) -> List[Dict]:
        """寿司テーマの問題を探索"""
        print("=== 寿司テーマPCP問題探索 ===")
        
        chars = ['S', 'T']  # 刺身とタンポポ
        found_problems = []
        samples_tested = 0
        
        # ドミノ数2-3での探索
        for num_dominoes in [3]:
            print(f"\nドミノ数 {num_dominoes} での探索...")
            
            # ドミノの組み合わせを生成
            for dominoes in self._generate_domino_combinations(chars, num_dominoes, 3):
                if samples_tested >= max_samples:
                    break
                
                # 初期文字列の組み合わせ
                for initial_top in self._generate_initial_pairs(chars, 4):
                    if samples_tested >= max_samples:
                        break
                    
                    samples_tested += 1
                    
                    # 問題インスタンス作成
                    try:
                        instance = PCPInstance(dominoes, initial_top, "")
                        
                        # ソルバーで解を探索
                        solver = OptimizedPCPSolver(instance, self.max_depth, self.time_limit)
                        solution = solver.solve()
                        
                        if solution is not None and solution.solve_time < self.time_limit:
                            # 品質評価
                            quality = self._evaluate_quality(solution)
                            
                            problem = {
                                'dominoes': dominoes,
                                'initial_top': initial_top,
                                'initial_bottom': "",
                                'solution': solution.sequence,
                                'solution_length': solution.length,
                                'solve_time': solution.solve_time,
                                'quality_score': quality,
                                'difficulty': self._classify_difficulty(solution),
                                'final_string': solution.final_string,
                                'diversity_score': solution.diversity_score
                            }
                            
                            if solution.length < sreshold:
                                continue
                            elif len(set(solution.sequence)) != len(dominoes):
                                continue
                            found_problems.append(problem)
                        
                    except (ValueError, Exception) as e:
                        # 無効な問題インスタンスはスキップ
                        continue
                    
                    if (20 * samples_tested) % max_samples == 0:
                        print(f"進捗: {samples_tested}/{max_samples}")
        
        print(f"\n探索完了: {len(found_problems)} 問題発見")
        return found_problems
    
    def _generate_domino_combinations(self, chars: List[str], num_dominoes: int, max_len: int) -> Iterator[List[Tuple[str, str]]]:
        """ドミノの組み合わせ生成"""
        # 可能な文字列
        strings = []
        for length in range(1, max_len + 1):
            for combo in itertools.product(chars, repeat=length):
                strings.append(''.join(combo))
        
        # ドミノの組み合わせ
        for domino_combo in itertools.combinations_with_replacement(
                itertools.product(strings, strings), num_dominoes):
            domino_list = list(domino_combo)

            # 文字を一種類しか含まない場合はスキップ
            if len(set(''.join(domino[0] + domino[1] for domino in domino_list))) == 1:
                continue

            yield domino_list
    
    def _generate_initial_pairs(self, chars: List[str], max_len: int) -> Iterator[str]:
        """初期文字列ペアの生成"""
        for length in range(1, max_len + 1):
            for combo in itertools.product(chars, repeat=length):
                yield(''.join(combo))
        
    
    def _evaluate_quality(self, solution: PCPSolution) -> float:
        return len(solution.final_string)
    
    def _classify_difficulty(self, solution: PCPSolution) -> str:
        """難易度分類"""
        if solution.length <= 5 and solution.solve_time < 0.1:
            return "easy"
        elif solution.length <= 10 and solution.solve_time < 0.5:
            return "medium"
        else:
            return "hard"
    
    def generate_game_problem_set(self, max_samples: int = 100) -> Dict:
        """ゲーム用問題セットを生成"""
        print(f"=== ゲーム用問題セット生成 ===")
        
        # 大規模探索
        all_problems = self.search_sushi_problems(max_samples, sreshold=3)
        
        if not all_problems:
            print("問題が見つかりませんでした。")
            return {'problems': [], 'statistics': {'total_found': 0}}
        
        # 品質順にソート
        all_problems.sort(key=lambda p: p['quality_score'], reverse=True)
        
        problem_set = {
            'name': 'sushi_constrained_pcp_problems',
            'description': '制約付き探索で生成された寿司テーマPCP問題セット',
            'generated_at': time.strftime('%Y-%m-%d %H:%M:%S'),
            'problems': all_problems,
            'statistics': {
                'total_found': len(all_problems),
                'selected_total': len(all_problems),
                'avg_quality': sum(p['quality_score'] for p in all_problems) / len(all_problems) if all_problems else 0
            }
        }
        
        return problem_set
    