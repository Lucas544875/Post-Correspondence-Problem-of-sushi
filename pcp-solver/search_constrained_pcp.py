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
    
    generator = ConstrainedPCPGenerator(max_depth=12, time_limit=1.0)
    
    while True:
        print("\n選択してください:")
        print("1. 寿司問題の探索実行")
        print("2. ゲーム用問題セット生成")
        print("0. 終了")
        
        try:
            choice = input("\n選択: ").strip()
            
            if choice == "0":
                print("終了します。")
                break
            elif choice == "1":
                # 寿司問題探索
                problems = generator.search_sushi_problems(max_samples=50)
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
                problem_set = generator.generate_game_problem_set(target_count)
                
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
            else:
                print("無効な選択です。")
                
        except KeyboardInterrupt:
            print("\n\n処理が中断されました。")
            break
        except Exception as e:
            print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    main()