#!/usr/bin/env python3
"""
ポスト対応問題ソルバーのテスト実行スクリプト
"""

from pcp_solver import PCPSolver, create_sample_problems

def run_all_tests():
    """全ての問題を自動実行"""
    print("=== ポスト対応問題ソルバー 自動テスト ===\n")
    
    problems = create_sample_problems()
    
    for name, dominoes in problems.items():
        print(f"{'='*60}")
        print(f"問題: {name}")
        print(f"ドミノ: {dominoes}")
        print(f"{'='*60}")
        
        solver = PCPSolver(dominoes, max_depth=15)
        solution = solver.solve()
        
        if solution:
            print("[OK] 解が見つかりました！")
        else:
            print("[NG] この深度では解が見つかりませんでした")
        
        print("\n" + "-"*60 + "\n")

def run_specific_problem():
    """特定の問題を実行"""
    print("=== 簡単な問題の実行 ===\n")
    
    # 簡単な問題: [("a", "aa"), ("aa", "a")]
    dominoes = [("a", "aa"), ("aa", "a")]
    
    print(f"ドミノ: {dominoes}")
    solver = PCPSolver(dominoes, max_depth=10)
    solution = solver.solve()
    
    if solution:
        print("\n[OK] この問題は解けます！")
        return True
    else:
        print("\n[NG] 解が見つかりませんでした")
        return False

def run_sushi_problem():
    """寿司問題を実行"""
    print("=== 寿司問題の実行 ===\n")
    
    dominoes = [
        ("s", "ss"),
        ("ss", "s"),
        ("b", "bb"),
        ("bb", "b")
    ]
    
    print(f"ドミノ: {dominoes}")
    solver = PCPSolver(dominoes, max_depth=12)
    solution = solver.solve()
    
    if solution:
        print("\n[OK] 寿司問題は解けます！")
        return True
    else:
        print("\n[NG] 寿司問題の解が見つかりませんでした")
        return False

if __name__ == "__main__":
    print("1. 簡単な問題をテスト")
    success1 = run_specific_problem()
    
    print("\n" + "="*80 + "\n")
    
    print("2. 寿司問題をテスト")  
    success2 = run_sushi_problem()
    
    print("\n" + "="*80 + "\n")
    
    print("3. 全問題をテスト")
    run_all_tests()
    
    print(f"テスト結果:")
    print(f"- 簡単な問題: {'OK' if success1 else 'NG'}")
    print(f"- 寿司問題: {'OK' if success2 else 'NG'}")