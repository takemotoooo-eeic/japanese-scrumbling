# japanese-scrumbling
言語情報学Ⅰ 期末プロジェクト


## Environment Setup

### MeCabのインストール

```bash
# MeCabのインストール（Ubuntu/Debian）
sudo apt-get update
sudo apt-get install mecab mecab-ipadic-utf8

# または（macOS）
# brew install mecab mecab-ipadic
```

### Python依存関係のインストール

```bash
# 依存関係のインストール
uv sync
```

## Dataset Preparation

### Wikipedia データの抽出

#### 1. ダンプファイルのダウンロードと解凍

日本語Wikipediaのダンプファイルをダウンロードして解凍：

```bash
# ダウンロード
curl -O https://dumps.wikimedia.org/jawiki/latest/jawiki-latest-pages-articles.xml.bz2

# 解凍
bzip2 -d jawiki-latest-pages-articles.xml.bz2

# data/wikiディレクトリに移動
mkdir data/wiki/
mv jawiki-latest-pages-articles.xml data/wiki/
```

#### 2. テキスト抽出

日本語Wikipediaのダンプファイルからテキストを抽出する場合：

```bash
uv run python -m wikiextractor.WikiExtractor -o data/wiki/ data/wiki/jawiki-latest-pages-articles.xml
```

- `-o data/wiki/`: 出力先ディレクトリを指定
- 入力ファイル: `data/wiki/jawiki-latest-pages-articles.xml`

#### 3. テキストファイルの統合とクリーンアップ

抽出されたファイルを1つのテキストファイルに統合し、不要な行を削除：

```bash
# 抽出されたwikiファイルを統合
find data/wiki/ -name "wiki_*" | awk '{system("cat "$0" >> data/wiki/wiki.txt")}'

# XMLタグのみの行を削除
sed -i '/^<[^>]*>$/d' data/wiki/wiki.txt

# 空行を削除
sed -i '/^$/d' data/wiki/wiki.txt
```

#### 4. MeCabによる分ち書き

統合されたテキストファイルをMeCabで分ち書き（スペース区切り）に変換：

```bash
# MeCabで分ち書き（スペース区切り）
mecab -Owakati data/wiki/wiki.txt > data/wiki/wiki_wakati.txt
```

- `-Owakati`: 分ち書き形式で出力
- 出力ファイル: `data/wiki/wiki_wakati.txt`

#### 5. ひらがな変換

分ち書きされたテキストをひらがなに変換：

```bash
# MeCabでひらがな変換
mecab -Oyomi data/wiki/wiki_wakati.txt > data/wiki/wiki_hiragana.txt
```

- `-Oyomi`: 読み仮名（カタカナ）形式で出力
- `sed 'y/ア-ン/あ-ん/'`: カタカナをひらがなに変換
- 出力ファイル: `data/wiki/wiki_hiragana.txt`

#### 6. データ分割

ひらがな変換されたテキストを訓練・検証・テストデータに分割：

```bash
# データをtrain/valid/testに分割
uv run python recipes/split_data.py data/wiki/wiki_hiragana.txt data/wikipedia
```

**実行結果の例：**
```
入力ファイル: data/wiki/wiki_hiragana.txt
出力ディレクトリ: data/wikipedia
分割比率 - Train: 80.0%, Valid: 10.0%, Test: 10.0%
ファイルを読み込み中...
総行数: 1,234,567
データをシャッフル中...
分割点 - Train: 987,653, Valid: 1,111,110, Test: 1,234,567
訓練データを書き込み中...
検証データを書き込み中...
テストデータを書き込み中...

分割完了!
訓練データ: 987,653 行 (80.0%)
検証データ: 123,457 行 (10.0%)
テストデータ: 123,457 行 (10.0%)

出力ファイル:
  - data/wikipedia/train.txt.original
  - data/wikipedia/valid.txt.original
  - data/wikipedia/test.txt.original
```

このスクリプトは以下の機能を提供します：
- デフォルトで80:10:10の比率でデータを分割
- ランダムシード（デフォルト: 42）で再現可能な分割
- カスタム分割比率の指定が可能
- 進捗状況と統計情報の表示
