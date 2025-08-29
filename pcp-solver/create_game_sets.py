#!/usr/bin/env python3
"""
PCPゲーム用の標準問題セットを作成するスクリプト
"""

from game_problem_generator import PCPGameInterface
import os

def create_standard_problem_sets():
    """標準的な問題セットを作成"""
    game = PCPGameInterface()
    
    print("=== PCPゲーム標準問題セット作成 ===\n")
    
    # 問題セットの定義
    problem_sets = [
        # 初心者向け
        {"name": "beginner_alphabet", "count": 5, "difficulty": "easy", "theme": "alphabet"},
        {"name": "beginner_sushi", "count": 5, "difficulty": "easy", "theme": "sushi"},
        {"name": "beginner_numbers", "count": 5, "difficulty": "easy", "theme": "numbers"},
        
        # 中級者向け
        {"name": "intermediate_alphabet", "count": 8, "difficulty": "medium", "theme": "alphabet"},
        {"name": "intermediate_sushi", "count": 8, "difficulty": "medium", "theme": "sushi"},
        {"name": "intermediate_numbers", "count": 8, "difficulty": "medium", "theme": "numbers"},
        
        # 上級者向け
        {"name": "advanced_alphabet", "count": 10, "difficulty": "hard", "theme": "alphabet"},
        {"name": "advanced_mixed", "count": 12, "difficulty": "hard", "theme": "alphabet"},
        
        # 特別セット
        {"name": "challenge_set", "count": 15, "difficulty": "hard", "theme": "sushi"},
    ]
    
    # データディレクトリ作成
    data_dir = "game_data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # 各問題セットを作成
    for set_config in problem_sets:
        print(f"作成中: {set_config['name']}")
        problem_set = game.create_problem_set(
            set_config["name"],
            set_config["count"],
            set_config["difficulty"],
            set_config["theme"]
        )
        
        # ファイルに保存
        filename = os.path.join(data_dir, f"{set_config['name']}.json")
        game.save_problem_set(set_config["name"], filename)
        
        print(f"[OK] {set_config['name']}: {problem_set['solvable_problems']}/{problem_set['total_problems']} 問題が解答可能\n")
    
    # 統計表示
    print("=== 作成完了 ===")
    game.show_statistics()
    
    print(f"\n問題セットは '{data_dir}' ディレクトリに保存されました。")

if __name__ == "__main__":
    create_standard_problem_sets()