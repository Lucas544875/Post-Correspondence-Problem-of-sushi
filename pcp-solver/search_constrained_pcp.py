#!/usr/bin/env python3
"""
初期文字列付きPCP問題の探索スクリプト

このスクリプトは制約条件を満たすPCP問題インスタンスを系統的に探索し、
解の存在を確認して高品質な問題セットを生成します。
"""

import json
from pcp_types import PCPInstance, PCPSolution
from pcp_solver import SimplePCPSolver, OptimizedPCPSolver
from pcp_generator import ConstrainedPCPGenerator

def main():
    """メイン実行関数"""
    print("初期文字列付きPCP問題探索ツール")
    print("=" * 50)
    
    generator = ConstrainedPCPGenerator(max_depth=100, time_limit=2.0)

    # ゲーム用問題セット生成
    problem_set = generator.generate_game_problem_set(10000)
    
    print(f"\n=== 生成結果 ===")
    stats = problem_set['statistics']
    print(f"発見総数: {stats['total_found']}")
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


if __name__ == "__main__":
    main()