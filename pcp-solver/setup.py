#!/usr/bin/env python3

import subprocess
import sys
import os

def setup_virtual_environment():
    """仮想環境の作成とパッケージのインストール"""
    print("仮想環境を作成中...")
    
    # 仮想環境作成
    if not os.path.exists("venv"):
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("仮想環境を作成しました。")
    else:
        print("仮想環境は既に存在します。")
    
    # アクティベーションスクリプトのパス
    if os.name == 'nt':  # Windows
        activate_script = os.path.join("venv", "Scripts", "activate.bat")
        pip_path = os.path.join("venv", "Scripts", "pip")
    else:  # Unix/Linux/Mac
        activate_script = os.path.join("venv", "bin", "activate")
        pip_path = os.path.join("venv", "bin", "pip")
    
    # requirements.txtからパッケージをインストール
    if os.path.exists("requirements.txt"):
        print("パッケージをインストール中...")
        subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)
        print("パッケージのインストールが完了しました。")
    
    print("\n仮想環境の準備が完了しました。")
    print(f"アクティベート: {activate_script}")

if __name__ == "__main__":
    setup_virtual_environment()