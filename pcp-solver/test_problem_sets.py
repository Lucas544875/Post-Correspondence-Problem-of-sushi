#!/usr/bin/env python3
"""
作成した問題セットをテストするスクリプト
"""

import json
import os
from game_problem_generator import PCPGameInterface

def test_problem_sets():
    """問題セットの内容をテスト表示"""
    game = PCPGameInterface()
    data_dir = "game_data"
    
    if not os.path.exists(data_dir):
        print("game_data ディレクトリが見つかりません")
        return
    
    json_files = [f for f in os.listdir(data_dir) if f.endswith('.json')]
    
    print("=== 作成された問題セット一覧 ===\n")
    
    for filename in sorted(json_files):
        filepath = os.path.join(data_dir, filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                problem_set = json.load(f)
            
            name = problem_set.get("name", "不明")
            difficulty = problem_set.get("difficulty", "不明")
            theme = problem_set.get("theme", "不明")
            total = problem_set.get("total_problems", 0)
            solvable = problem_set.get("solvable_problems", 0)
            
            print(f"[FILE] {filename}")
            print(f"   名前: {name}")
            print(f"   難易度: {difficulty}")
            print(f"   テーマ: {theme}")
            print(f"   問題数: {total}")
            success_rate = solvable/total*100 if total > 0 else 0
            print(f"   解答可能: {solvable} ({success_rate:.1f}%)")
            
            # サンプル問題を1つ表示
            problems = problem_set.get("problems", [])
            if problems:
                sample = None
                for p in problems:
                    if p.get("has_solution", False):
                        sample = p
                        break
                
                if sample:
                    dominoes = sample["dominoes"]
                    solution = sample.get("solution", [])
                    quality = sample.get("difficulty_score", 0)
                    
                    print(f"   サンプル問題:")
                    print(f"     ドミノ: {dominoes}")
                    print(f"     解: {[x+1 for x in solution]} (品質: {quality}/10)")
                    
                    if "solution_string" in sample:
                        result = sample["solution_string"]
                        print(f"     結果: {result['top']} = {result['bottom']}")
            
            print()
            
        except Exception as e:
            print(f"[ERROR] {filename}: エラー - {e}")
    
    print(f"合計 {len(json_files)} 個の問題セットが作成されました")

def play_sample_from_set():
    """問題セットからサンプル問題をプレイ"""
    game = PCPGameInterface()
    data_dir = "game_data"
    
    json_files = [f for f in os.listdir(data_dir) if f.endswith('.json')]
    
    if not json_files:
        print("問題セットが見つかりません")
        return
    
    print("利用可能な問題セット:")
    for i, filename in enumerate(json_files, 1):
        set_name = filename[:-5]  # .json を除去
        print(f"  {i}. {set_name}")
    
    try:
        choice = int(input("選択 (番号): ")) - 1
        if 0 <= choice < len(json_files):
            filename = json_files[choice]
            filepath = os.path.join(data_dir, filename)
            
            problem_set = game.load_problem_set(filepath)
            
            if problem_set:
                solvable_problems = [p for p in problem_set["problems"] 
                                   if p.get("has_solution", False)]
                
                if solvable_problems:
                    import random
                    problem = random.choice(solvable_problems)
                    game.play_problem(problem, f"{problem_set['name']} - サンプル問題")
                else:
                    print("解答可能な問題がありません")
            else:
                print("問題セットの読み込みに失敗しました")
        else:
            print("無効な選択です")
    except (ValueError, IndexError):
        print("無効な入力です")

if __name__ == "__main__":
    print("1. 問題セット一覧表示")
    test_problem_sets()
    
    print("\n2. サンプル問題をプレイ")
    try:
        play_sample_from_set()
    except KeyboardInterrupt:
        print("\n終了しました")
    except Exception as e:
        print(f"エラー: {e}")