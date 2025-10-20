#!/usr/bin/env python3
"""
Script to extract utterances from CHILDES data
Extract utterances (lines starting with *) from all .cha files and combine into one txt file
"""

import pathlib
import argparse
import re
from typing import List, Tuple

def extract_utterances_from_cha(file_path: pathlib.Path) -> List[str]:
    """
    Extract utterances from .cha file
    
    Args:
        file_path: Path to .cha file
        
    Returns:
        List of utterances
    """
    utterances = []
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if line.startswith('*'):
                    parts = line.split(':', 1)
                    if len(parts) > 1:
                        utterance = parts[1].strip()
                        if utterance and utterance != '.':
                            utterances.append(utterance)
    except Exception as e:
        print(f"Error: Failed to read {file_path}: {e}")
    
    return utterances

def clean_utterance(utterance: str) -> str:
    """
    Clean utterance
    
    Args:
        utterance: Original utterance
        
    Returns:
        Cleaned utterance
    """
    utterance = re.sub(r'\[.*?\]', '', utterance)
    utterance = re.sub(r'@[a-z]+', '', utterance)
    utterance = re.sub(r'<[^>]*>', '', utterance)
    utterance = re.sub(r'\+\.\.\.', '', utterance)
    utterance = re.sub(r'[&~]', '', utterance)
    
    utterance = re.sub(r'\s+', ' ', utterance)
    utterance = utterance.strip()
    
    return utterance

def contains_alphabet(text: str) -> bool:
    """
    Check if text contains alphabet characters
    
    Args:
        text: Text to check
        
    Returns:
        True if alphabet is contained
    """
    return bool(re.search(r'[a-zA-Z]', text))

def extract_all_utterances(input_dir: str, output_file: str, include_speaker: bool = False) -> None:
    """
    Extract utterances from all .cha files in specified directory
    
    Args:
        input_dir: Input directory
        output_file: Output file
        include_speaker: Whether to include speaker information
    """
    input_path = pathlib.Path(input_dir)
    output_path = pathlib.Path(output_file)
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    all_utterances = []
    processed_files = 0
    total_utterances = 0
    alphabet_utterances_count = 0
    
    print(f"Input directory: {input_dir}")
    print(f"Output file: {output_file}")
    print(f"Include speaker info: {include_speaker}")
    print()
    
    cha_files = list(input_path.rglob("*.cha"))
    print(f"Found .cha files: {len(cha_files)}")
    print()
    
    for cha_file in cha_files:
        print(f"Processing: {cha_file.relative_to(input_path)}")
        
        try:
            with open(cha_file, 'r', encoding='utf-8', errors='ignore') as f:
                file_utterances = []
                file_alphabet_count = 0
                for line in f:
                    line = line.strip()
                    if line.startswith('*'):
                        parts = line.split(':', 1)
                        if len(parts) > 1:
                            speaker = parts[0].strip()
                            utterance = parts[1].strip()
                            
                            if utterance and utterance != '.':
                                clean_utterance_text = clean_utterance(utterance)
                                if clean_utterance_text:
                                    if contains_alphabet(clean_utterance_text):
                                        file_alphabet_count += 1
                                        print(f"  [Alphabet utterance] {clean_utterance_text}")
                                        continue
                                    
                                    if include_speaker:
                                        file_utterances.append(f"{speaker}: {clean_utterance_text}")
                                    else:
                                        file_utterances.append(clean_utterance_text)
                
                all_utterances.extend(file_utterances)
                print(f"  Extracted utterances: {len(file_utterances)}")
                if file_alphabet_count > 0:
                    print(f"  Alphabet utterances: {file_alphabet_count}")
                    print(f"Processing: {cha_file.relative_to(input_path)}")
                processed_files += 1
                total_utterances += len(file_utterances)
                alphabet_utterances_count += file_alphabet_count
                
        except Exception as e:
            print(f"  Error: {e}")
    
    print(f"\nWriting to output file...")
    with open(output_path, 'w', encoding='utf-8') as f:
        for utterance in all_utterances:
            f.write(utterance + '\n')
    
    print(f"\nProcessing completed!")
    print(f"Processed files: {processed_files}")
    print(f"Total extracted utterances: {total_utterances:,}")
    print(f"Total alphabet utterances: {alphabet_utterances_count:,}")
    print(f"Output file: {output_path}")
    print(f"File size: {output_path.stat().st_size:,} bytes")

def main():
    parser = argparse.ArgumentParser(description="Extract utterances from CHILDES data")
    parser.add_argument("input_dir", help="Input directory (containing .cha files)")
    parser.add_argument("output_file", help="Output file")
    parser.add_argument("--include-speaker", action="store_true", 
                       help="Include speaker information (e.g., *CHI: ア .)")
    
    args = parser.parse_args()
    
    extract_all_utterances(
        input_dir=args.input_dir,
        output_file=args.output_file,
        include_speaker=args.include_speaker
    )

if __name__ == "__main__":
    main()
