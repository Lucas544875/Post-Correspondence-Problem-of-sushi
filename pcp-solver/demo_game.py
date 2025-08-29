#!/usr/bin/env python3
"""
PCPゲームのシンプルなデモ版
文字化け問題を回避した簡易版
"""

from game_problem_generator import PCPGameProblemGenerator
from problem_validator import BatchProblemValidator

def demo_simple_game():
    """シンプルなゲームデモ"""
    print("=== PCP問題デモ ===\n")
    
    generator = PCPGameProblemGenerator()
    validator = BatchProblemValidator()
    
    # 簡単な問題を生成
    print("簡単な問題を生成中...")
    dominoes = generator.generate_simple_problem()
    
    # 問題を検証
    validation = validator.validate_single_problem(1, dominoes)
    
    if validation["status"] != "completed":
        print("問題の生成に失敗しました")
        return
    
    if not validation.get("has_solution", False):
        print("解のない問題が生成されました。再実行してください。")
        return
    
    print(f"ドミノ: {dominoes}")
    print(f"品質スコア: {validation.get('quality_score', 0):.2f}")
    print(f"解の長さ: {validation.get('solution_length', '不明')}")
    
    # 解を表示（デモ用）
    if "solution" in validation:
        solution = validation["solution"]
        print(f"\n解: {[x+1 for x in solution]}")  # 1ベースで表示
        
        # 解の構築過程を表示
        top_result = ""
        bottom_result = ""
        
        print("\n解の構築:")
        for i, domino_idx in enumerate(solution):
            domino = dominoes[domino_idx]
            top_result += domino[0]
            bottom_result += domino[1]
            
            print(f"ステップ {i+1}: ドミノ{domino_idx+1} {domino}")
            print(f"  上部: {top_result}")
            print(f"  下部: {bottom_result}")
        
        print(f"\n最終結果:")
        print(f"上部: {top_result}")
        print(f"下部: {bottom_result}")
        print(f"一致: {'OK' if top_result == bottom_result else 'NG'}")

def demo_problem_generation():
    """問題生成のデモ"""
    print("\n=== 問題生成デモ ===\n")
    
    generator = PCPGameProblemGenerator()
    validator = BatchProblemValidator()
    
    difficulties = ["easy", "medium", "hard"]
    themes = ["alphabet", "sushi", "numbers"]
    
    for difficulty in difficulties:
        for theme in themes:
            print(f"\n--- {difficulty} + {theme} ---")
            
            try:
                dominoes = generator.generate_custom_problem(difficulty, theme)
                validation = validator.validate_single_problem(1, dominoes)
                
                has_solution = validation.get("has_solution", False)
                quality = validation.get("quality_score", 0)
                
                print(f"ドミノ: {dominoes}")
                print(f"解: {'あり' if has_solution else 'なし'}")
                print(f"品質: {quality:.2f}")
                
            except Exception as e:
                print(f"エラー: {e}")

def demo_batch_validation():
    """バッチ検証のデモ"""
    print("\n=== バッチ検証デモ ===\n")
    
    generator = PCPGameProblemGenerator()
    validator = BatchProblemValidator()
    
    # 複数問題を生成
    problems = []
    for _ in range(10):
        difficulty = "easy"
        theme = "alphabet"
        dominoes = generator.generate_custom_problem(difficulty, theme)
        problems.append(dominoes)
    
    print(f"{len(problems)}問題を検証中...")
    
    # バッチ検証
    results = validator.validate_problem_batch(problems, show_progress=False)
    
    # 結果表示
    stats = results["statistics"]
    print(f"\n結果:")
    print(f"総問題数: {stats['total_problems']}")
    print(f"解答可能: {stats['problems_with_solution']}")
    print(f"成功率: {stats['success_rate']*100:.1f}%")
    print(f"処理時間: {stats['processing_time']:.2f}秒")
    
    if "solution_statistics" in stats:
        sol_stats = stats["solution_statistics"]
        print(f"平均解長: {sol_stats['avg_solution_length']:.1f}")
        print(f"高品質問題: {sol_stats['high_quality_problems']}")

if __name__ == "__main__":
    try:
        demo_simple_game()
        demo_problem_generation()
        demo_batch_validation()
        
        print("\n=== デモ完了 ===")
        print("実際にゲームをプレイするには pcp_game.py を実行してください")
        
    except Exception as e:
        print(f"デモ中にエラーが発生しました: {e}")
        import traceback
        traceback.print_exc()