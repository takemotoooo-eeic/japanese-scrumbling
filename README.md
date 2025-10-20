# Japanese Scrambling
Final Project for Linguistics I

## Environment Setup

### MeCab Installation

```bash
# Install MeCab (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install mecab mecab-ipadic-utf8

# Or (macOS)
# brew install mecab mecab-ipadic
```

### Python Dependencies Installation

```bash
# Install dependencies
uv sync
```

## Dataset Preparation

### Wikipedia Data Extraction

#### 1. Download and Extract Dump File

Download and extract the Japanese Wikipedia dump file:

```bash
# Download
curl -O https://dumps.wikimedia.org/jawiki/latest/jawiki-latest-pages-articles.xml.bz2

# Extract
bzip2 -d jawiki-latest-pages-articles.xml.bz2

# Move to data/wiki directory
mkdir data/wiki/
mv jawiki-latest-pages-articles.xml data/wiki/
```

#### 2. Text Extraction

Extract text from the Japanese Wikipedia dump file:

```bash
uv run python -m wikiextractor.WikiExtractor -o data/wiki/ data/wiki/jawiki-latest-pages-articles.xml
```

- `-o data/wiki/`: Specify output directory
- Input file: `data/wiki/jawiki-latest-pages-articles.xml`

#### 3. Text File Integration and Cleanup

Integrate extracted files into a single text file and remove unnecessary lines:

```bash
# Integrate extracted wiki files
find data/wiki/ -name "wiki_*" | awk '{system("cat "$0" >> data/wiki/wiki.txt")}'

# Remove lines containing only XML tags
sed -i '/^<[^>]*>$/d' data/wiki/wiki.txt

# Remove empty lines
sed -i '/^$/d' data/wiki/wiki.txt
```

#### 4. Tokenization with MeCab

Convert the integrated text file to space-separated tokens using MeCab:

```bash
# Tokenize with MeCab (space-separated)
mecab -Owakati data/wiki/wiki.txt > data/wiki/wiki_wakati.txt
```

- `-Owakati`: Output in tokenized format
- Output file: `data/wiki/wiki_wakati.txt`

#### 5. Hiragana Conversion

Convert tokenized text to hiragana:

```bash
# Convert to hiragana with MeCab
mecab -Oyomi data/wiki/wiki_wakati.txt > data/wiki/wiki_hiragana.txt
```

- `-Oyomi`: Output in reading (katakana) format
- Output file: `data/wiki/wiki_hiragana.txt`

#### 6. Data Splitting

Split the hiragana-converted text into training, validation, and test datasets:

```bash
# Split data into train/valid/test
uv run python recipes/split_data.py data/wiki/wiki_hiragana.txt data/wikipedia
```

**Example output:**
```
Output files:
  - data/wikipedia/train.txt.original
  - data/wikipedia/valid.txt.original
  - data/wikipedia/test.txt.original
```

### CHILDES Data Processing

#### 1. Download and Extract CHILDES Data

Download and extract CHILDES data to `data/childes` directory from the following sources:

- [Hamasaki](https://talkbank.org/childes/access/Japanese/Hamasaki.html)
- [NINJAL-Okubo](https://talkbank.org/childes/access/Japanese/NINJAL-Okubo.html)
- [Noji](https://talkbank.org/childes/access/Japanese/Noji.html)
- [Ogawa](https://talkbank.org/childes/access/Japanese/Ogawa.html)
- [Okayama](https://talkbank.org/childes/access/Japanese/Okayama.html)
- [Yokoyama](https://talkbank.org/childes/access/Japanese/Yokoyama.html)

#### 2. Utterance Extraction

Extract only utterances from CHILDES data and combine them into a single text file:

```bash
# Extract utterances from CHILDES data
uv run python recipes/extract_childes_utterances.py data/childes data/childes_utterances.txt
```

This script provides the following features:
- Recursively search all `.cha` files
- Extract utterances from lines starting with `*`
- Clean special characters and symbols
- Optional speaker information inclusion
- Display progress and statistics

#### 3. Hiragana Conversion

Convert tokenized text to hiragana:

```bash
# Convert to hiragana with MeCab
mecab -Oyomi data/childes/utterances.txt > data/childes/utterances_hiragana.txt
```

- `-Oyomi`: Output in reading (katakana) format
- Output file: `data/childes/utterances_hiragana.txt`

#### 4. Data Splitting

Split the hiragana-converted text into training, validation, and test datasets:

```bash
# Split data into train/valid/test
uv run python recipes/split_data.py data/childes/utterances_hiragana.txt data/CHILDES
```

**Example output:**
```
Output files:
  - data/CHILDES/train.txt.original
  - data/CHILDES/valid.txt.original
  - data/CHILDES/test.txt.original
```
