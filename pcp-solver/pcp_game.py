#!/usr/bin/env python3
"""
PCPゲーム - 対話的なポスト対応問題ゲーム

ゲームモード:
1. 練習モード - 簡単な問題から始める
2. チャレンジモード - 制限時間付き
3. エンドレスモード - 連続で問題を解く
4. カスタムモード - 自作問題をプレイ
"""

import time
import random
import json
import os
from typing import List, Tuple, Dict, Optional
from game_problem_generator import PCPGameInterface, PCPGameProblemGenerator
from problem_validator import BatchProblemValidator

class PCPGameSession:
    """PCPゲームセッション管理"""
    
    def __init__(self):
        self.interface = PCPGameInterface()
        self.generator = PCPGameProblemGenerator()
        self.validator = BatchProblemValidator()
        self.session_stats = {
            "problems_attempted": 0,
            "problems_solved": 0,
            "total_time": 0,
            "hints_used": 0,
            "current_streak": 0,
            "best_streak": 0
        }
        self.current_problem = None
        self.start_time = None
    
    def start_practice_mode(self):
        """練習モード - 段階的な難易度上昇"""
        print("=== 練習モード ===")
        print("簡単な問題から始めて、徐々に難しくなります\n")
        
        difficulties = ["easy", "easy", "medium", "medium", "hard"]
        themes = ["alphabet", "sushi", "numbers"]
        
        for level, difficulty in enumerate(difficulties, 1):
            print(f"\n--- レベル {level} ({difficulty}) ---")
            theme = random.choice(themes)
            
            # 問題生成
            dominoes = self.generator.generate_custom_problem(difficulty, theme)
            validation = self.validator.validate_single_problem(0, dominoes)
            
            if not validation.get("has_solution", False):
                print("解のない問題が生成されました。別の問題を生成します...")
                continue
            
            # 問題をプレイ
            success = self._play_single_problem(validation, f"レベル {level}")
            
            if not success:
                print("練習モードを終了します")
                break
            
            if level < len(difficulties):
                continue_play = input("\n次のレベルに進みますか？ (y/n): ").strip().lower()
                if continue_play != 'y':
                    break
        
        print("\n練習モード完了！")
        self._show_session_stats()
    
    def start_challenge_mode(self, time_limit: int = 300):
        """チャレンジモード - 制限時間内にできるだけ多く解く"""
        print(f"=== チャレンジモード ===")
        print(f"制限時間: {time_limit}秒")
        print("できるだけ多くの問題を解いてください！\n")
        
        session_start = time.time()
        problem_count = 0
        
        while time.time() - session_start < time_limit:
            remaining_time = time_limit - (time.time() - session_start)
            print(f"\n残り時間: {remaining_time:.0f}秒")
            
            # ランダム問題生成
            difficulty = random.choice(["easy", "medium", "hard"])
            theme = random.choice(["alphabet", "sushi", "numbers"])
            
            dominoes = self.generator.generate_custom_problem(difficulty, theme)
            validation = self.validator.validate_single_problem(problem_count, dominoes)
            
            if not validation.get("has_solution", False):
                continue
            
            problem_count += 1
            success = self._play_single_problem(validation, f"問題 {problem_count}", 
                                             time_limit=remaining_time)
            
            if not success:  # ユーザーが中断
                break
                
            if time.time() - session_start >= time_limit:
                print("\n時間切れ！")
                break
        
        print(f"\nチャレンジモード終了！")
        print(f"解いた問題数: {self.session_stats['problems_solved']}/{problem_count}")
        self._show_session_stats()
    
    def start_endless_mode(self):
        """エンドレスモード - 連続で問題を解く"""
        print("=== エンドレスモード ===")
        print("連続で問題を解いてストリークを稼ごう！")
        print("間違えるとストリークがリセットされます\n")
        
        problem_count = 0
        
        while True:
            problem_count += 1
            
            # 動的難易度調整
            if self.session_stats["current_streak"] < 3:
                difficulty = "easy"
            elif self.session_stats["current_streak"] < 8:
                difficulty = "medium"
            else:
                difficulty = "hard"
            
            theme = random.choice(["alphabet", "sushi", "numbers"])
            
            # 問題生成
            dominoes = self.generator.generate_custom_problem(difficulty, theme)
            validation = self.validator.validate_single_problem(problem_count, dominoes)
            
            if not validation.get("has_solution", False):
                continue
            
            print(f"\n--- 問題 {problem_count} ({difficulty}) ---")
            print(f"現在のストリーク: {self.session_stats['current_streak']}")
            print(f"ベストストリーク: {self.session_stats['best_streak']}")
            
            success = self._play_single_problem(validation, f"問題 {problem_count}")
            
            if not success:  # ユーザーが中断または失敗
                if self.session_stats["problems_attempted"] > 0:
                    last_correct = (self.session_stats["problems_solved"] == 
                                  self.session_stats["problems_attempted"])
                    if not last_correct:
                        print("ストリークがリセットされました！")
                        self.session_stats["current_streak"] = 0
                break
                
            continue_play = input("\n続けますか？ (y/n): ").strip().lower()
            if continue_play != 'y':
                break
        
        print("\nエンドレスモード終了！")
        self._show_session_stats()
    
    def start_custom_mode(self):
        """カスタムモード - ユーザー作成問題"""
        print("=== カスタムモード ===")
        print("自分で問題を作成してプレイできます\n")
        
        while True:
            print("1. 新しい問題を作成")
            print("2. 問題セットから選択")
            print("3. 問題ファイルを読み込み")
            print("0. メインメニューに戻る")
            
            choice = input("\n選択: ").strip()
            
            if choice == "0":
                break
            elif choice == "1":
                self._create_custom_problem()
            elif choice == "2":
                self._select_from_problem_sets()
            elif choice == "3":
                self._load_problem_file()
            else:
                print("無効な選択です")
    
    def _play_single_problem(self, problem_data: Dict, problem_title: str = "", 
                           time_limit: Optional[float] = None) -> bool:
        """単一問題をプレイ"""
        dominoes = problem_data["dominoes"]
        self.current_problem = problem_data
        self.start_time = time.time()
        
        print(f"\n=== {problem_title} ===")
        print(f"難易度スコア: {problem_data.get('quality_score', 0):.2f}")
        print(f"ドミノ:")
        for i, (top, bottom) in enumerate(dominoes, 1):
            print(f"  {i}. {top}")
            print(f"     {bottom}")
        
        print(f"\n目標: ドミノを組み合わせて上部と下部の文字列を一致させてください")
        print(f"コマンド:")
        print(f"  - ドミノ番号をスペース区切りで入力 (例: 1 2 1 3)")
        print(f"  - 'hint' でヒントを表示")
        print(f"  - 'q' で終了")
        
        attempts = 0
        self.session_stats["problems_attempted"] += 1
        
        while True:
            try:
                # 制限時間チェック
                if time_limit:
                    elapsed = time.time() - self.start_time
                    if elapsed >= time_limit:
                        print(f"\n時間切れ！ ({time_limit:.0f}秒)")
                        return False
                    print(f"残り時間: {time_limit - elapsed:.0f}秒")
                
                user_input = input(f"\n試行 {attempts + 1}: ").strip()
                
                if user_input.lower() == 'q':
                    return False
                elif user_input.lower() == 'hint':
                    self._show_hint(dominoes, problem_data)
                    continue
                
                # ユーザー入力をパース
                try:
                    domino_sequence = [int(x) - 1 for x in user_input.split()]
                except ValueError:
                    print("エラー: 数字をスペース区切りで入力してください")
                    continue
                
                # 範囲チェック
                if any(idx < 0 or idx >= len(dominoes) for idx in domino_sequence):
                    print(f"エラー: ドミノ番号は1-{len(dominoes)}の範囲で入力してください")
                    continue
                
                attempts += 1
                
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
                    solve_time = time.time() - self.start_time
                    print(f"🎉 正解！ (試行回数: {attempts}, 時間: {solve_time:.1f}秒)")
                    
                    # 統計更新
                    self._update_success_stats(solve_time, attempts)
                    return True
                else:
                    print(f"❌ 不正解。文字列が一致しません。")
                    
                    # 3回失敗でヒント提供
                    if attempts >= 3:
                        print("3回失敗しました。ヒントを見ますか？ (hint と入力)")
                    
            except KeyboardInterrupt:
                print("\n\n中断されました")
                return False
    
    def _show_hint(self, dominoes: List[Tuple[str, str]], problem_data: Dict):
        """ヒントを表示"""
        self.session_stats["hints_used"] += 1
        
        print(f"\n=== ヒント ===")
        
        # ヒント1: 文字列の長さ分析
        print("1. 文字列長の分析:")
        for i, (top, bottom) in enumerate(dominoes, 1):
            print(f"   ドミノ{i}: 上部{len(top)}文字, 下部{len(bottom)}文字")
        
        # ヒント2: 使用文字の分析
        all_chars = set()
        for top, bottom in dominoes:
            all_chars.update(top + bottom)
        print(f"2. 使用されている文字: {sorted(all_chars)}")
        
        # ヒント3: 解が存在することを確認
        if problem_data.get("has_solution"):
            solution_length = problem_data.get("solution_length", "不明")
            print(f"3. この問題には解が存在します")
            print(f"   解の長さ: {solution_length}ドミノ")
            
            # より具体的なヒント（解の最初の一手）
            if "solution" in problem_data and problem_data["solution"]:
                first_domino = problem_data["solution"][0] + 1
                print(f"4. ヒント: 最初に使うドミノは {first_domino}番です")
        else:
            print(f"3. 注意: この問題は解が存在しない可能性があります")
    
    def _update_success_stats(self, solve_time: float, attempts: int):
        """成功時の統計更新"""
        self.session_stats["problems_solved"] += 1
        self.session_stats["total_time"] += solve_time
        self.session_stats["current_streak"] += 1
        
        if self.session_stats["current_streak"] > self.session_stats["best_streak"]:
            self.session_stats["best_streak"] = self.session_stats["current_streak"]
    
    def _create_custom_problem(self):
        """カスタム問題作成"""
        print("\n=== カスタム問題作成 ===")
        print("ドミノを作成してください。形式: 上部文字列,下部文字列")
        print("例: abc,ab")
        print("終了するには空行を入力")
        
        dominoes = []
        while True:
            domino_input = input(f"ドミノ {len(dominoes) + 1}: ").strip()
            if not domino_input:
                break
                
            try:
                top, bottom = domino_input.split(',')
                dominoes.append((top.strip(), bottom.strip()))
                print(f"追加されました: ({top.strip()}, {bottom.strip()})")
            except ValueError:
                print("形式が正しくありません。'上部,下部'の形式で入力してください")
        
        if dominoes:
            print(f"\n作成された問題: {dominoes}")
            
            # 問題を検証
            print("問題を検証中...")
            validation = self.validator.validate_single_problem(0, dominoes)
            
            if validation["status"] == "completed":
                has_solution = validation.get("has_solution", False)
                quality = validation.get("quality_score", 0)
                
                print(f"検証結果: {'解あり' if has_solution else '解なし'}")
                print(f"品質スコア: {quality:.2f}")
                
                if has_solution:
                    play = input("この問題をプレイしますか？ (y/n): ").strip().lower()
                    if play == 'y':
                        self._play_single_problem(validation, "カスタム問題")
                else:
                    print("この問題には解が存在しません")
            else:
                print(f"検証中にエラーが発生しました: {validation.get('error', '不明')}")
    
    def _select_from_problem_sets(self):
        """問題セットから選択"""
        data_dir = "game_data"
        if not os.path.exists(data_dir):
            print("問題セットが見つかりません")
            return
        
        json_files = [f for f in os.listdir(data_dir) if f.endswith('.json')]
        if not json_files:
            print("問題セットファイルが見つかりません")
            return
        
        print("\n利用可能な問題セット:")
        for i, filename in enumerate(json_files, 1):
            print(f"  {i}. {filename[:-5]}")  # .json拡張子を除く
        
        try:
            choice = int(input("選択 (番号): ")) - 1
            if 0 <= choice < len(json_files):
                filename = os.path.join(data_dir, json_files[choice])
                problem_set = self.interface.load_problem_set(filename)
                
                if problem_set:
                    solvable_problems = [p for p in problem_set["problems"] 
                                       if p.get("has_solution", False)]
                    
                    if solvable_problems:
                        problem = random.choice(solvable_problems)
                        self._play_single_problem(problem, 
                                                f"{problem_set['name']} - ランダム問題")
                    else:
                        print("解答可能な問題がありません")
            else:
                print("無効な選択です")
        except (ValueError, IndexError):
            print("無効な入力です")
    
    def _load_problem_file(self):
        """問題ファイルを読み込み"""
        filename = input("問題ファイル名: ").strip()
        try:
            problem_set = self.interface.load_problem_set(filename)
            if problem_set:
                print(f"問題セット '{problem_set['name']}' が読み込まれました")
        except Exception as e:
            print(f"ファイル読み込みエラー: {e}")
    
    def _show_session_stats(self):
        """セッション統計表示"""
        stats = self.session_stats
        print(f"\n=== セッション統計 ===")
        print(f"挑戦した問題: {stats['problems_attempted']}")
        print(f"解けた問題: {stats['problems_solved']}")
        
        if stats['problems_attempted'] > 0:
            success_rate = stats['problems_solved'] / stats['problems_attempted'] * 100
            print(f"成功率: {success_rate:.1f}%")
        
        if stats['problems_solved'] > 0:
            avg_time = stats['total_time'] / stats['problems_solved']
            print(f"平均解答時間: {avg_time:.1f}秒")
        
        print(f"使用したヒント: {stats['hints_used']}")
        print(f"現在のストリーク: {stats['current_streak']}")
        print(f"ベストストリーク: {stats['best_streak']}")

def main():
    """メインゲームループ"""
    print("=" * 50)
    print("    ポスト対応問題 (PCP) ゲーム")
    print("=" * 50)
    print("ドミノを組み合わせて上部と下部の文字列を一致させよう！")
    
    game = PCPGameSession()
    
    while True:
        print(f"\n=== メインメニュー ===")
        print("1. 練習モード")
        print("2. チャレンジモード（5分制限）")
        print("3. エンドレスモード")
        print("4. カスタムモード")
        print("5. セッション統計を表示")
        print("0. 終了")
        
        choice = input("\n選択: ").strip()
        
        try:
            if choice == "0":
                print("ゲームを終了します。お疲れさまでした！")
                break
            elif choice == "1":
                game.start_practice_mode()
            elif choice == "2":
                game.start_challenge_mode(300)  # 5分
            elif choice == "3":
                game.start_endless_mode()
            elif choice == "4":
                game.start_custom_mode()
            elif choice == "5":
                game._show_session_stats()
            else:
                print("無効な選択です")
        except KeyboardInterrupt:
            print("\n\n中断されました")
        except Exception as e:
            print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    main()