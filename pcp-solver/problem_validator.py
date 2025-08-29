#!/usr/bin/env python3
"""
PCP問題検証専用システム

このモジュールは以下の機能を提供します:
1. 問題の解の検証
2. 問題の品質評価
3. 大量問題のバッチ検証
4. 問題の統計分析
"""

import time
import json
from typing import List, Tuple, Dict, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from pcp_solver import PCPSolver

class ProblemQualityAnalyzer:
    """問題の品質分析器"""
    
    def __init__(self):
        self.quality_metrics = {
            "solution_exists": 0,
            "solution_length": 0,
            "search_time": 0,
            "domino_count": 0,
            "string_complexity": 0,
            "uniqueness": 0
        }
    
    def analyze_problem(self, dominoes: List[Tuple[str, str]], 
                       solution: Optional[List[int]] = None, 
                       search_time: float = 0.0) -> Dict:
        """単一問題の品質分析"""
        analysis = {
            "dominoes": dominoes,
            "domino_count": len(dominoes),
            "has_solution": solution is not None,
            "solution": solution,
            "search_time": search_time
        }
        
        # 文字列複雑度の計算
        total_chars = sum(len(top) + len(bottom) for top, bottom in dominoes)
        unique_chars = len(set(''.join(top + bottom for top, bottom in dominoes)))
        analysis["total_characters"] = total_chars
        analysis["unique_characters"] = unique_chars
        analysis["complexity_ratio"] = unique_chars / total_chars if total_chars > 0 else 0
        
        # 解の品質評価
        if solution:
            analysis["solution_length"] = len(solution)
            analysis["solution_efficiency"] = len(set(solution)) / len(solution)  # 使用ドミノの多様性
            
            # 解の文字列を構築
            top_result = ""
            bottom_result = ""
            for idx in solution:
                top_result += dominoes[idx][0]
                bottom_result += dominoes[idx][1]
            
            analysis["result_string"] = {
                "top": top_result,
                "bottom": bottom_result,
                "length": len(top_result),
                "verified_match": top_result == bottom_result
            }
        
        # 品質スコアの計算
        analysis["quality_score"] = self._calculate_quality_score(analysis)
        
        return analysis
    
    def _calculate_quality_score(self, analysis: Dict) -> float:
        """品質スコア計算 (0.0-1.0)"""
        score = 0.0
        
        # 解の存在 (基本点)
        if analysis["has_solution"]:
            score += 0.3
        
        # 適度な複雑さ (0.2点)
        if 2 <= analysis["domino_count"] <= 5:
            score += 0.1
        if 3 <= analysis["total_characters"] <= 20:
            score += 0.1
        
        # 解の品質 (0.3点)
        if analysis["has_solution"]:
            sol_len = analysis["solution_length"]
            if 2 <= sol_len <= 10:  # 適度な解の長さ
                score += 0.1
            if analysis["solution_efficiency"] > 0.3:  # ドミノの多様性
                score += 0.1
            if analysis["result_string"]["length"] <= 30:  # 結果文字列が適度
                score += 0.1
        
        # 探索効率 (0.2点)
        if analysis["search_time"] < 1.0:
            score += 0.2
        elif analysis["search_time"] < 5.0:
            score += 0.1
        
        return min(score, 1.0)

class BatchProblemValidator:
    """大量問題のバッチ検証システム"""
    
    def __init__(self, max_depth: int = 20, time_limit: float = 10.0, max_workers: int = 4):
        self.max_depth = max_depth
        self.time_limit = time_limit
        self.max_workers = max_workers
        self.analyzer = ProblemQualityAnalyzer()
    
    def validate_single_problem(self, problem_id: int, dominoes: List[Tuple[str, str]]) -> Dict:
        """単一問題の検証"""
        start_time = time.time()
        
        try:
            solver = PCPSolver(dominoes, self.max_depth)
            solution = solver.solve()
            end_time = time.time()
            
            # タイムアウトチェック
            if end_time - start_time > self.time_limit:
                return {
                    "problem_id": problem_id,
                    "status": "timeout",
                    "dominoes": dominoes,
                    "search_time": end_time - start_time
                }
            
            # 品質分析
            analysis = self.analyzer.analyze_problem(dominoes, solution, end_time - start_time)
            analysis["problem_id"] = problem_id
            analysis["status"] = "completed"
            
            return analysis
            
        except Exception as e:
            return {
                "problem_id": problem_id,
                "status": "error",
                "dominoes": dominoes,
                "error": str(e)
            }
    
    def validate_problem_batch(self, problems: List[List[Tuple[str, str]]], 
                             show_progress: bool = True) -> Dict:
        """問題のバッチ検証"""
        results = []
        start_time = time.time()
        
        if show_progress:
            print(f"バッチ検証開始: {len(problems)}問題を{self.max_workers}スレッドで処理中...")
        
        # 並列処理で検証
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # タスクを送信
            future_to_id = {
                executor.submit(self.validate_single_problem, i, problem): i 
                for i, problem in enumerate(problems)
            }
            
            # 結果を収集
            completed = 0
            for future in as_completed(future_to_id):
                result = future.result()
                results.append(result)
                completed += 1
                
                if show_progress and completed % 10 == 0:
                    print(f"  進捗: {completed}/{len(problems)} ({completed/len(problems)*100:.1f}%)")
        
        end_time = time.time()
        
        # 統計情報を計算
        stats = self._calculate_batch_statistics(results, end_time - start_time)
        
        return {
            "total_problems": len(problems),
            "results": results,
            "statistics": stats,
            "processing_time": end_time - start_time
        }
    
    def _calculate_batch_statistics(self, results: List[Dict], processing_time: float) -> Dict:
        """バッチ検証の統計情報計算"""
        completed = [r for r in results if r["status"] == "completed"]
        with_solution = [r for r in completed if r["has_solution"]]
        timeouts = [r for r in results if r["status"] == "timeout"]
        errors = [r for r in results if r["status"] == "error"]
        
        stats = {
            "total_problems": len(results),
            "completed_problems": len(completed),
            "problems_with_solution": len(with_solution),
            "timeout_problems": len(timeouts),
            "error_problems": len(errors),
            "success_rate": len(with_solution) / len(results) if results else 0,
            "completion_rate": len(completed) / len(results) if results else 0,
            "processing_time": processing_time,
            "problems_per_second": len(results) / processing_time if processing_time > 0 else 0
        }
        
        if with_solution:
            # 解のある問題の詳細統計
            solution_lengths = [r["solution_length"] for r in with_solution]
            search_times = [r["search_time"] for r in with_solution]
            quality_scores = [r["quality_score"] for r in with_solution]
            
            stats["solution_statistics"] = {
                "avg_solution_length": sum(solution_lengths) / len(solution_lengths),
                "min_solution_length": min(solution_lengths),
                "max_solution_length": max(solution_lengths),
                "avg_search_time": sum(search_times) / len(search_times),
                "avg_quality_score": sum(quality_scores) / len(quality_scores),
                "high_quality_problems": len([s for s in quality_scores if s >= 0.7])
            }
        
        return stats
    
    def export_results(self, validation_results: Dict, filename: str):
        """検証結果をJSONファイルにエクスポート"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(validation_results, f, ensure_ascii=False, indent=2)
        print(f"検証結果を {filename} にエクスポートしました")
    
    def filter_quality_problems(self, validation_results: Dict, 
                              min_quality: float = 0.6) -> List[Dict]:
        """品質基準を満たす問題をフィルタリング"""
        quality_problems = []
        
        for result in validation_results["results"]:
            if (result["status"] == "completed" and 
                result["has_solution"] and 
                result["quality_score"] >= min_quality):
                quality_problems.append(result)
        
        return quality_problems

def demo_validation():
    """検証システムのデモ"""
    print("=== PCP問題検証システム デモ ===\n")
    
    # テスト問題セット
    test_problems = [
        [("a", "aa"), ("aa", "a")],  # 簡単
        [("ab", "aba"), ("baa", "aa"), ("aba", "bab")],  # 中程度
        [("abc", "ab"), ("ca", "a"), ("acc", "ba")],  # 難しい（解なし？）
        [("x", "xx"), ("xx", "x")],  # 簡単（別パターン）
        [("pq", "pqr"), ("qr", "q"), ("r", "rr")],  # 中程度
    ]
    
    # バッチ検証実行
    validator = BatchProblemValidator(max_depth=15, time_limit=5.0)
    results = validator.validate_problem_batch(test_problems)
    
    # 結果表示
    print("\n=== 検証結果 ===")
    print(f"総問題数: {results['statistics']['total_problems']}")
    print(f"解答可能問題: {results['statistics']['problems_with_solution']}")
    print(f"成功率: {results['statistics']['success_rate']*100:.1f}%")
    print(f"処理時間: {results['statistics']['processing_time']:.2f}秒")
    
    if "solution_statistics" in results["statistics"]:
        sol_stats = results["statistics"]["solution_statistics"]
        print(f"平均解長: {sol_stats['avg_solution_length']:.1f}")
        print(f"平均品質スコア: {sol_stats['avg_quality_score']:.2f}")
        print(f"高品質問題数: {sol_stats['high_quality_problems']}")
    
    # 詳細結果
    print(f"\n=== 問題別詳細 ===")
    for i, result in enumerate(results["results"]):
        if result["status"] == "completed":
            status = "解あり" if result["has_solution"] else "解なし"
            quality = result.get("quality_score", 0)
            print(f"問題{i+1}: {status} (品質: {quality:.2f})")
        else:
            print(f"問題{i+1}: {result['status']}")

if __name__ == "__main__":
    demo_validation()