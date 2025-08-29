#!/usr/bin/env python3
"""
PCPゲーム用問題生成・探索プログラム

このプログラムは以下の機能を提供します:
1. 難易度別の問題セット生成
2. 問題の解の検証
3. ゲーム用のインターフェース
4. 問題の自動評価
"""

import random
import time
import json
from typing import List, Tuple, Dict, Optional, Set
from pcp_solver import PCPSolver

class PCPGameProblemGenerator:
    def __init__(self):
        """PCPゲーム用問題生成器を初期化"""
        self.alphabet = ['a', 'b', 'c', 'd', 'e']
        self.sushi_chars = ['s', 'u', 's', 'h', 'i']  # sushi characters
        self.number_chars = ['0', '1', '2', '3', '4']
        
    def generate_simple_problem(self) -> List[Tuple[str, str]]:
        """簡単な問題を生成 (解の長さが短い)"""
        patterns = [
            # パターン1: 倍増/半減型
            [("a", "aa"), ("aa", "a")],
            [("b", "bb"), ("bb", "b")],
            
            # パターン2: 対称型
            [("ab", "ba"), ("ba", "ab")],
            [("abc", "cba"), ("cba", "abc")],
            
            # パターン3: 交互型
            [("a", "ab"), ("b", "a")],
            [("x", "xy"), ("y", "x")],
        ]
        return random.choice(patterns)
    
    def generate_medium_problem(self) -> List[Tuple[str, str]]:
        """中程度の問題を生成"""
        patterns = [
            # 複数文字の複雑な組み合わせ
            [("ab", "aba"), ("baa", "aa"), ("aba", "bab")],
            [("abc", "cab"), ("bca", "abc"), ("cab", "bca")],
            [("aa", "aaa"), ("bb", "bb"), ("aaa", "aa")],
            [("xy", "xyx"), ("yx", "yxy"), ("xyx", "yx")],
            
            # 数字パターン
            [("01", "010"), ("10", "101"), ("010", "10")],
            [("12", "121"), ("21", "212"), ("121", "21")],
        ]
        return random.choice(patterns)
    
    def generate_hard_problem(self) -> List[Tuple[str, str]]:
        """難しい問題を生成 (解が存在しない可能性もある)"""
        patterns = [
            # 解が存在しない問題
            [("abc", "ab"), ("ca", "a"), ("acc", "ba")],
            [("xyz", "xy"), ("zx", "x"), ("xzz", "zy")],
            
            # 解が存在するが複雑な問題
            [("abcd", "abc"), ("cd", "d"), ("d", "dd")],
            [("pqr", "pq"), ("qr", "q"), ("r", "rr")],
            
            # 長い解が必要な問題
            [("a", "aaa"), ("aa", "a"), ("aaa", "aaaa")],
            [("x", "xxx"), ("xx", "x"), ("xxx", "xxxx")],
        ]
        return random.choice(patterns)
    
    def generate_sushi_problem(self) -> List[Tuple[str, str]]:
        """寿司テーマの問題を生成"""
        sushi_patterns = [
            # 基本パターン
            [("s", "ss"), ("ss", "s"), ("u", "uu"), ("uu", "u")],
            
            # 複雑なパターン
            [("su", "sus"), ("us", "usu"), ("sus", "us")],
            [("shi", "shis"), ("his", "hish"), ("shis", "his")],
            
            # 交互パターン
            [("s", "su"), ("u", "s"), ("su", "sus")],
            [("h", "hi"), ("i", "h"), ("hi", "hih")],
        ]
        return random.choice(sushi_patterns)
    
    def generate_custom_problem(self, difficulty: str, theme: str = "alphabet") -> List[Tuple[str, str]]:
        """カスタム問題生成"""
        if theme == "sushi":
            chars = self.sushi_chars[:3]  # s, u, s
        elif theme == "numbers":
            chars = self.number_chars[:3]  # 0, 1, 2
        else:
            chars = self.alphabet[:3]  # a, b, c
        
        if difficulty == "easy":
            # 2つのドミノで解ける問題
            c1, c2 = random.sample(chars, 2)
            return [(c1, c1+c2), (c1+c2, c1)]
        
        elif difficulty == "medium":
            # 3つのドミノを使う問題
            c1, c2, c3 = random.sample(chars, 3)
            return [
                (c1+c2, c1+c2+c3),
                (c2+c3+c1, c2+c3),
                (c1+c2+c3, c2+c1)
            ]
        
        else:  # hard
            # 解が存在するかわからない問題
            c1, c2, c3 = random.sample(chars, 3)
            return [
                (c1+c2+c3, c1+c2),
                (c3+c1, c1),
                (c1+c3+c3, c2+c1)
            ]

class PCPGameValidator:
    """PCP問題の検証システム"""
    
    def __init__(self, max_depth: int = 20, time_limit: float = 10.0):
        self.max_depth = max_depth
        self.time_limit = time_limit
    
    def validate_problem(self, dominoes: List[Tuple[str, str]]) -> Dict:
        """問題を検証し、解の情報を返す"""
        start_time = time.time()
        solver = PCPSolver(dominoes, self.max_depth)
        
        # 解を探索
        solution = solver.solve()
        end_time = time.time()
        
        result = {
            "dominoes": dominoes,
            "has_solution": solution is not None,
            "solution": solution,
            "search_time": end_time - start_time,
            "solution_length": len(solution) if solution else None,
            "difficulty_score": self._calculate_difficulty(dominoes, solution, end_time - start_time)
        }
        
        if solution:
            result["solution_string"] = self._get_solution_string(dominoes, solution)
        
        return result
    
    def _calculate_difficulty(self, dominoes: List[Tuple[str, str]], solution: Optional[List[int]], search_time: float) -> int:
        """問題の難易度スコアを計算 (1-10)"""
        score = 1
        
        # ドミノ数による加点
        score += min(len(dominoes) - 2, 3)
        
        # 解の長さによる加点
        if solution:
            score += min(len(solution) // 3, 3)
        else:
            score += 5  # 解が見つからない場合は高難易度
        
        # 探索時間による加点
        if search_time > 1.0:
            score += 2
        elif search_time > 0.1:
            score += 1
        
        # 文字列の複雑さによる加点
        total_length = sum(len(top) + len(bottom) for top, bottom in dominoes)
        score += min(total_length // 10, 2)
        
        return min(score, 10)
    
    def _get_solution_string(self, dominoes: List[Tuple[str, str]], solution: List[int]) -> Dict[str, str]:
        """解の文字列を取得"""
        top_string = ""
        bottom_string = ""
        
        for domino_idx in solution:
            domino = dominoes[domino_idx]
            top_string += domino[0]
            bottom_string += domino[1]
        
        return {
            "top": top_string,
            "bottom": bottom_string,
            "match": top_string == bottom_string
        }

class PCPGameInterface:
    """PCPゲーム用のインターフェース"""
    
    def __init__(self):
        self.generator = PCPGameProblemGenerator()
        self.validator = PCPGameValidator()
        self.problem_sets = {}
        
    def create_problem_set(self, name: str, count: int, difficulty: str, theme: str = "alphabet") -> Dict:
        """問題セットを作成"""
        problems = []
        valid_problems = []
        
        print(f"問題セット '{name}' を作成中... (難易度: {difficulty}, テーマ: {theme})")
        
        for i in range(count):
            if difficulty == "easy":
                if theme == "sushi":
                    dominoes = self.generator.generate_sushi_problem()
                else:
                    dominoes = self.generator.generate_simple_problem()
            elif difficulty == "medium":
                dominoes = self.generator.generate_medium_problem()
            elif difficulty == "hard":
                dominoes = self.generator.generate_hard_problem()
            else:
                dominoes = self.generator.generate_custom_problem(difficulty, theme)
            
            # 問題を検証
            validation = self.validator.validate_problem(dominoes)
            problems.append(validation)
            
            if validation["has_solution"]:
                valid_problems.append(validation)
            
            print(f"  問題 {i+1}/{count}: {'解あり' if validation['has_solution'] else '解なし'} "
                  f"(難易度: {validation['difficulty_score']}/10)")
        
        problem_set = {
            "name": name,
            "difficulty": difficulty,
            "theme": theme,
            "total_problems": len(problems),
            "solvable_problems": len(valid_problems),
            "problems": problems,
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.problem_sets[name] = problem_set
        return problem_set
    
    def save_problem_set(self, name: str, filename: str):
        """問題セットをJSONファイルに保存"""
        if name not in self.problem_sets:
            print(f"問題セット '{name}' が見つかりません")
            return
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.problem_sets[name], f, ensure_ascii=False, indent=2)
        print(f"問題セット '{name}' を {filename} に保存しました")
    
    def load_problem_set(self, filename: str) -> Dict:
        """問題セットをJSONファイルから読み込み"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                problem_set = json.load(f)
            
            name = problem_set["name"]
            self.problem_sets[name] = problem_set
            print(f"問題セット '{name}' を {filename} から読み込みました")
            return problem_set
        except FileNotFoundError:
            print(f"ファイル {filename} が見つかりません")
            return {}
    
    def play_problem(self, problem_data: Dict) -> bool:
        """単一の問題をプレイ"""
        dominoes = problem_data["dominoes"]
        
        print(f"\n=== PCP問題 ===")
        print(f"ドミノ:")
        for i, (top, bottom) in enumerate(dominoes, 1):
            print(f"  {i}. {top}")
            print(f"     {bottom}")
        
        print(f"\n目標: ドミノを組み合わせて上部と下部の文字列を一致させてください")
        print(f"使用方法: ドミノ番号をスペース区切りで入力 (例: 1 2 1 3)")
        print(f"ヒント: 最大{len(dominoes)}種類のドミノを何回でも使用できます")
        
        while True:
            try:
                user_input = input("\nドミノの組み合わせを入力 (qで終了): ").strip()
                if user_input.lower() == 'q':
                    return False
                
                # ユーザー入力をパース
                domino_sequence = [int(x) - 1 for x in user_input.split()]
                
                # 範囲チェック
                if any(idx < 0 or idx >= len(dominoes) for idx in domino_sequence):
                    print(f"エラー: ドミノ番号は1-{len(dominoes)}の範囲で入力してください")
                    continue
                
                # 結果を計算
                top_result = ""
                bottom_result = ""
                
                for idx in domino_sequence:
                    top_result += dominoes[idx][0]
                    bottom_result += dominoes[idx][1]
                
                print(f"\n結果:")
                print(f"上部: {top_result}")
                print(f"下部: {bottom_result}")
                
                if top_result == bottom_result:
                    print(f"🎉 正解！文字列が一致しました！")
                    return True
                else:
                    print(f"❌ 不正解。文字列が一致しません。")
                    
            except ValueError:
                print("エラー: 数字をスペース区切りで入力してください")
            except KeyboardInterrupt:
                print("\nゲームを終了します")
                return False
    
    def show_statistics(self):
        """統計情報を表示"""
        if not self.problem_sets:
            print("問題セットがありません")
            return
        
        print(f"\n=== 統計情報 ===")
        for name, problem_set in self.problem_sets.items():
            print(f"\n問題セット: {name}")
            print(f"  難易度: {problem_set['difficulty']}")
            print(f"  テーマ: {problem_set['theme']}")
            print(f"  総問題数: {problem_set['total_problems']}")
            print(f"  解答可能問題数: {problem_set['solvable_problems']}")
            print(f"  解答率: {problem_set['solvable_problems']/problem_set['total_problems']*100:.1f}%")
            
            # 難易度分布
            difficulties = [p["difficulty_score"] for p in problem_set["problems"]]
            avg_difficulty = sum(difficulties) / len(difficulties)
            print(f"  平均難易度: {avg_difficulty:.1f}/10")

def main():
    """メイン関数 - ゲームインターフェース"""
    game = PCPGameInterface()
    
    print("=== PCPゲーム問題生成・探索システム ===\n")
    
    while True:
        print("\n1. 問題セットを作成")
        print("2. 問題セットを保存")
        print("3. 問題セットを読み込み")
        print("4. 問題をプレイ")
        print("5. 統計情報を表示")
        print("6. ランダム問題を生成してプレイ")
        print("0. 終了")
        
        try:
            choice = int(input("\n選択: "))
            
            if choice == 0:
                print("終了します")
                break
                
            elif choice == 1:
                name = input("問題セット名: ")
                count = int(input("問題数: "))
                print("難易度を選択:")
                print("  1. easy   2. medium   3. hard")
                diff_choice = int(input("選択: "))
                difficulty = ["easy", "medium", "hard"][diff_choice - 1]
                
                print("テーマを選択:")
                print("  1. alphabet   2. sushi   3. numbers")
                theme_choice = int(input("選択: "))
                theme = ["alphabet", "sushi", "numbers"][theme_choice - 1]
                
                game.create_problem_set(name, count, difficulty, theme)
                
            elif choice == 2:
                if not game.problem_sets:
                    print("保存する問題セットがありません")
                    continue
                
                print("利用可能な問題セット:")
                for name in game.problem_sets.keys():
                    print(f"  - {name}")
                
                name = input("保存する問題セット名: ")
                filename = input("保存ファイル名 (.json): ")
                if not filename.endswith('.json'):
                    filename += '.json'
                game.save_problem_set(name, filename)
                
            elif choice == 3:
                filename = input("読み込みファイル名: ")
                game.load_problem_set(filename)
                
            elif choice == 4:
                if not game.problem_sets:
                    print("問題セットがありません")
                    continue
                
                print("利用可能な問題セット:")
                for name in game.problem_sets.keys():
                    print(f"  - {name}")
                
                set_name = input("プレイする問題セット名: ")
                if set_name not in game.problem_sets:
                    print("問題セットが見つかりません")
                    continue
                
                problems = game.problem_sets[set_name]["problems"]
                solvable = [p for p in problems if p["has_solution"]]
                
                if not solvable:
                    print("解答可能な問題がありません")
                    continue
                
                problem = random.choice(solvable)
                game.play_problem(problem)
                
            elif choice == 5:
                game.show_statistics()
                
            elif choice == 6:
                print("ランダム問題を生成中...")
                difficulty = random.choice(["easy", "medium"])
                theme = random.choice(["alphabet", "sushi", "numbers"])
                
                dominoes = game.generator.generate_custom_problem(difficulty, theme)
                validation = game.validator.validate_problem(dominoes)
                
                if validation["has_solution"]:
                    print(f"難易度: {difficulty}, テーマ: {theme}")
                    game.play_problem(validation)
                else:
                    print("解のない問題が生成されました。もう一度試してください。")
                    
        except (ValueError, IndexError, KeyboardInterrupt):
            print("無効な入力です")
        except Exception as e:
            print(f"エラー: {e}")

if __name__ == "__main__":
    main()