# Japanese Scrambling
Final Project for Linguistics I

## Environment Setup

### Install MeCab

```bash
# Install MeCab (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install mecab mecab-ipadic-utf8

# Or (macOS)
# brew install mecab mecab-ipadic
```

### Install Python Dependencies

```bash
# Install dependencies
uv sync
```

## Dataset Preparation

### Wikipedia Data Extraction

#### 1. Download and Decompress the Dump

Download and decompress the Japanese Wikipedia dump file:

```bash
# Download
curl -O https://dumps.wikimedia.org/jawiki/latest/jawiki-latest-pages-articles.xml.bz2

# Decompress
bzip2 -d jawiki-latest-pages-articles.xml.bz2

# Move to data/wiki directory
mkdir data/wiki/
mv jawiki-latest-pages-articles.xml data/wiki/
```

#### 2. Extract Plain Text

Extract plain text from the Japanese Wikipedia dump file:

```bash
uv run python -m wikiextractor.WikiExtractor -o data/wiki/ data/wiki/jawiki-latest-pages-articles.xml
```

- `-o data/wiki/`: Output directory
- Input file: `data/wiki/jawiki-latest-pages-articles.xml`

#### 3. Merge Files and Clean Up

Merge extracted files into a single text file and remove unnecessary lines:

```bash
# Merge extracted wiki files
find data/wiki/ -name "wiki_*" | awk '{system("cat "$0" >> data/wiki/wiki.txt")}'

# Remove lines that contain only XML tags
sed -i '/^<[^>]*>$/d' data/wiki/wiki.txt

# Remove empty lines
sed -i '/^$/d' data/wiki/wiki.txt
```

#### 4. Tokenize with MeCab

Convert the merged text file to space-separated tokens using MeCab:

```bash
# Tokenize with MeCab (space-separated)
mecab -Owakati data/wiki/wiki.txt > data/wiki/wiki_wakati.txt
```

- `-Owakati`: Output tokenized format
- Output file: `data/wiki/wiki_wakati.txt`

#### 5. Convert to Katakana

Convert tokenized text to katakana readings:

```bash
# Convert to katakana with MeCab
mecab -Oyomi data/wiki/wiki_wakati.txt > data/wiki/wiki_katakana.txt
```

- `-Oyomi`: Output in reading (katakana) format
- Output file: `data/wiki/wiki_katakana.txt`

#### 6. Split the Dataset

Split the katakana-converted text into training, validation, and test datasets:

```bash
# Split data into train/valid/test
uv run python recipes/split_data.py data/wiki/wiki_katakana.txt data/wikipedia
```

**Example output:**
```
Output files:
  - data/wikipedia/train.txt.original
  - data/wikipedia/valid.txt.original
  - data/wikipedia/test.txt.original
```

### CHILDES Data Processing

#### 1. Download and Extract CHILDES

Download and place CHILDES data under `data/childes` from the following sources:

- [Hamasaki](https://talkbank.org/childes/access/Japanese/Hamasaki.html)
- [NINJAL-Okubo](https://talkbank.org/childes/access/Japanese/NINJAL-Okubo.html)
- [Noji](https://talkbank.org/childes/access/Japanese/Noji.html)
- [Ogawa](https://talkbank.org/childes/access/Japanese/Ogawa.html)
- [Okayama](https://talkbank.org/childes/access/Japanese/Okayama.html)
- [Yokoyama](https://talkbank.org/childes/access/Japanese/Yokoyama.html)

#### 2. Extract Utterances

Extract only utterances from CHILDES data and combine them into a single text file:

```bash
# Extract utterances from CHILDES data
uv run python recipes/extract_childes_utterances.py data/childes data/childes_utterances.txt
```

This script provides the following features:
- Recursively searches all `.cha` files
- Extracts utterances from lines starting with `*`
- Cleans special characters and symbols
- Optionally includes speaker information
- Displays progress and summary statistics

#### 3. Convert to Katakana

Convert the tokenized text to katakana readings:

```bash
# Convert to katakana with MeCab
mecab -Oyomi data/childes/utterances.txt > data/childes/utterance_katakana.txt
```

- `-Oyomi`: Output in reading (katakana) format
- Output file: `data/childes/utterance_katakana.txt`

#### 4. Split the Dataset

Split the katakana-converted text into training, validation, and test datasets:

```bash
# Split data into train/valid/test
uv run python recipes/split_data.py data/childes/utterance_katakana.txt data/CHILDES
```

**Example output:**
```
Output files:
  - data/CHILDES/train.txt.original
  - data/CHILDES/valid.txt.original
  - data/CHILDES/test.txt.original
```

## Run (Start Training)

### Example: Train with CHILDES

Start training with the following command:

```bash
uv run python japanese-scrumble/main.py \
  --experiment-id childes_exp1 \
  --data data/CHILDES \
  --model Transformer
```

- **--experiment-id**: Experiment identifier (used to separate logs and caches)
- **--data**: Dataset directory (expects `train/valid/test.txt.original`)
- **--model**: Model name (e.g., `Transformer`)

If you have a GPU environment, add the CUDA flag:

```bash
uv run python japanese-scrumble/main.py \
  --experiment-id childes_exp1 \
  --data data/CHILDES \
  --model Transformer \
  --cuda
```
