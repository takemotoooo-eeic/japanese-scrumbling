import sys

from lib import get_surprisals_for_strings


def main():
    if len(sys.argv) != 4:
        print("Usage: python calculate_surprisal.py <checkpoint_name> <sentence1> <sentence2>")
        sys.exit(1)

    # 引数の取得
    checkpoint_name = sys.argv[1]  # 例: "childes_exp1__Transformer__e512_h2048_L6_H8_do0.2"
    sentence1 = sys.argv[2]
    sentence2 = sys.argv[3]

    # retrained__ の形でモデルを指定
    model_name = f"retrained__{checkpoint_name}"

    print(f"🔹 Using model: {model_name}")
    print(f"🔸 Sentence 1: {sentence1}")
    print(f"🔸 Sentence 2: {sentence2}\n")

    # サプライザルを計算
    surprisals = get_surprisals_for_strings((sentence1, sentence2), model=model_name)

    # 結果の出力
    for i, sent in enumerate(surprisals.sentences):
        print(f"--- Sentence {i+1} ---")
        for token_info in sent.tokens:
            token = token_info.text
            surprisal = token_info.surprisal
            print(f"{token}\t{surprisal:.3f}")
        print()


if __name__ == "__main__":
    main()
