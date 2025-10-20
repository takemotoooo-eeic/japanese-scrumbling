#!/usr/bin/env python3
"""
Data splitting script
Split wiki_hiragana.txt into train/valid/test
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
    Split data file into train/valid/test
    
    Args:
        input_file: Input file path
        output_dir: Output directory
        train_ratio: Training data ratio
        valid_ratio: Validation data ratio
        test_ratio: Test data ratio
        seed: Random seed
    """
    
    if abs(train_ratio + valid_ratio + test_ratio - 1.0) > 1e-6:
        raise ValueError("train_ratio + valid_ratio + test_ratio must equal 1.0")
    
    output_path = pathlib.Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    random.seed(seed)
    
    print(f"Input file: {input_file}")
    print(f"Output directory: {output_dir}")
    print(f"Split ratios - Train: {train_ratio:.1%}, Valid: {valid_ratio:.1%}, Test: {test_ratio:.1%}")
    
    print("Loading file...")
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    
    total_lines = len(lines)
    print(f"Total lines: {total_lines:,}")
    
    print("Shuffling data...")
    random.shuffle(lines)
    
    train_end = int(total_lines * train_ratio)
    valid_end = int(total_lines * (train_ratio + valid_ratio))
    
    print(f"Split points - Train: {train_end:,}, Valid: {valid_end:,}, Test: {total_lines:,}")
    
    print("Writing training data...")
    with open(output_path / "train.txt.original", 'w', encoding='utf-8') as f:
        f.writelines(lines[:train_end])
    
    print("Writing validation data...")
    with open(output_path / "valid.txt.original", 'w', encoding='utf-8') as f:
        f.writelines(lines[train_end:valid_end])
    
    print("Writing test data...")
    with open(output_path / "test.txt.original", 'w', encoding='utf-8') as f:
        f.writelines(lines[valid_end:])
    
    print("\nSplit completed!")
    print(f"Training data: {train_end:,} lines ({train_end/total_lines:.1%})")
    print(f"Validation data: {valid_end - train_end:,} lines ({(valid_end - train_end)/total_lines:.1%})")
    print(f"Test data: {total_lines - valid_end:,} lines ({(total_lines - valid_end)/total_lines:.1%})")
    
    print(f"\nOutput files:")
    print(f"  - {output_path / 'train.txt.original'}")
    print(f"  - {output_path / 'valid.txt.original'}")
    print(f"  - {output_path / 'test.txt.original'}")

def main():
    parser = argparse.ArgumentParser(description="Split data file into train/valid/test")
    parser.add_argument("input_file", help="Input file path")
    parser.add_argument("output_dir", help="Output directory")
    parser.add_argument("--train-ratio", type=float, default=0.8, help="Training data ratio (default: 0.8)")
    parser.add_argument("--valid-ratio", type=float, default=0.1, help="Validation data ratio (default: 0.1)")
    parser.add_argument("--test-ratio", type=float, default=0.1, help="Test data ratio (default: 0.1)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed (default: 42)")
    
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
