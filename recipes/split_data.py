#!/usr/bin/env python3
"""
データ分割スクリプト
wiki_hiragana.txtをtrain/valid/testに分割する
"""

import pathlib
import random
import argparse
from typing import Tuple

def split_data(
    input_file: str,
    output_dir: str,
    train_ratio: float = 0.8,
    valid_ratio: float = 0.1,
    test_ratio: float = 0.1,
    seed: int = 42
) -> None:
    """
    データファイルをtrain/valid/testに分割する
    
    Args:
        input_file: 入力ファイルパス
        output_dir: 出力ディレクトリ
        train_ratio: 訓練データの割合
        valid_ratio: 検証データの割合
        test_ratio: テストデータの割合
        seed: ランダムシード
    """
    
    # 比率の検証
    if abs(train_ratio + valid_ratio + test_ratio - 1.0) > 1e-6:
        raise ValueError("train_ratio + valid_ratio + test_ratio は 1.0 である必要があります")
    
    # 出力ディレクトリの作成
    output_path = pathlib.Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # ランダムシードの設定
    random.seed(seed)
    
    print(f"入力ファイル: {input_file}")
    print(f"出力ディレクトリ: {output_dir}")
    print(f"分割比率 - Train: {train_ratio:.1%}, Valid: {valid_ratio:.1%}, Test: {test_ratio:.1%}")
    
    # ファイルを読み込んで行をシャッフル
    print("ファイルを読み込み中...")
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    
    total_lines = len(lines)
    print(f"総行数: {total_lines:,}")
    
    # 行をシャッフル
    print("データをシャッフル中...")
    random.shuffle(lines)
    
    # 分割点を計算
    train_end = int(total_lines * train_ratio)
    valid_end = int(total_lines * (train_ratio + valid_ratio))
    
    print(f"分割点 - Train: {train_end:,}, Valid: {valid_end:,}, Test: {total_lines:,}")
    
    # ファイルに書き込み
    print("訓練データを書き込み中...")
    with open(output_path / "train.txt.original", 'w', encoding='utf-8') as f:
        f.writelines(lines[:train_end])
    
    print("検証データを書き込み中...")
    with open(output_path / "valid.txt.original", 'w', encoding='utf-8') as f:
        f.writelines(lines[train_end:valid_end])
    
    print("テストデータを書き込み中...")
    with open(output_path / "test.txt.original", 'w', encoding='utf-8') as f:
        f.writelines(lines[valid_end:])
    
    # 結果の表示
    print("\n分割完了!")
    print(f"訓練データ: {train_end:,} 行 ({train_end/total_lines:.1%})")
    print(f"検証データ: {valid_end - train_end:,} 行 ({(valid_end - train_end)/total_lines:.1%})")
    print(f"テストデータ: {total_lines - valid_end:,} 行 ({(total_lines - valid_end)/total_lines:.1%})")
    
    print(f"\n出力ファイル:")
    print(f"  - {output_path / 'train.txt.original'}")
    print(f"  - {output_path / 'valid.txt.original'}")
    print(f"  - {output_path / 'test.txt.original'}")

def main():
    parser = argparse.ArgumentParser(description="データファイルをtrain/valid/testに分割")
    parser.add_argument("input_file", help="入力ファイルパス")
    parser.add_argument("output_dir", help="出力ディレクトリ")
    parser.add_argument("--train-ratio", type=float, default=0.8, help="訓練データの割合 (デフォルト: 0.8)")
    parser.add_argument("--valid-ratio", type=float, default=0.1, help="検証データの割合 (デフォルト: 0.1)")
    parser.add_argument("--test-ratio", type=float, default=0.1, help="テストデータの割合 (デフォルト: 0.1)")
    parser.add_argument("--seed", type=int, default=42, help="ランダムシード (デフォルト: 42)")
    
    args = parser.parse_args()
    
    split_data(
        input_file=args.input_file,
        output_dir=args.output_dir,
        train_ratio=args.train_ratio,
        valid_ratio=args.valid_ratio,
        test_ratio=args.test_ratio,
        seed=args.seed
    )

if __name__ == "__main__":
    main()
