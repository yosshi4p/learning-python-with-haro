# OSの環境変数（OPENAI_API_KEY や OPENAI_MODEL など）を読むために os を使う
import os

# OpenAI公式ライブラリのクライアント（API呼び出し用）を使えるようにする
from openai import OpenAI

# ------------------------------------------------------------
# 設定：モデル（まずは動作優先なら gpt-4o-mini が堅い）
# ------------------------------------------------------------

# 環境変数 OPENAI_MODEL があればそれを使い、無ければ "gpt-4o-mini" を使う
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# LLMに「作家としてどう振る舞うか」「出力形式」などのルールをまとめて指示する文章
SYSTEM_PROMPT = """あなたは一流のショートショート作家（星新一・筒井康隆系の軽妙さ）。
目的：ユーザーとのチャット往復で、最終的に日本語の約400字ショートショートを1本完成させる。

# 進行ルール（超重要）
- 最初は質問だけを返す（小説は書かない）
- 質問は最大3問。はい/いいえ か短文で答えられる形にする
- ユーザーが回答したら、小説だけを返す（解説・前置き・見出し禁止）
- 小説は380〜420字に収める（句読点含む）
- 条件違反があれば内部で修正してから出力する（ユーザーに調整を頼まない）

# 必須条件
・説教／教訓の直説は禁止（読後に感じさせるのはOK）
・会話を必ず1回入れる（「」を使う）
・最後の1文で「なるほど/え？」となる軽いひねり（オチor余韻）
・固有名詞は最小限、説明は短く、出来事で見せる

# 構成指定
①一文目で状況が分かる掴み
②中盤で小さなトラブル or 違和感
③終盤で視点がズレる／意味が反転する

# 文体
テンポ良く、比喩は1〜2個まで。

# 出力フォーマット
- 質問フェーズ：先頭行を必ず【Q】で始め、質問を箇条書きで出す（質問だけ）
- 小説フェーズ：先頭行を必ず【S】で始め、その後に本文だけを出力
""".strip()  # 先頭・末尾の余計な改行や空白を削って、プロンプトをきれいにする

# OpenAI APIを呼び出すためのクライアントを作成（環境変数 OPENAI_API_KEY を自動で参照）
client = OpenAI()


# LLMにテキストを渡して、返ってきた文章（テキスト）を文字列として受け取る関数
def call_llm(user_text: str) -> str:
    """
    openai==2.21.0 向け：Chat Completions で呼び出す
    """
    # Chat Completions APIで、system(ルール)とuser(入力)を渡して応答を生成する
    resp = client.chat.completions.create(
        model=MODEL,  # 使うモデル名（環境変数 or デフォルト）
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},  # ふるまい・ルールの指示
            {"role": "user", "content": user_text},        # 今回ユーザーが渡した内容
        ],
    )
    # 返答候補の1つ目（choices[0]）の本文を取り出し、前後の空白を削って返す
    return (resp.choices[0].message.content or "").strip()


# 返答テキストが【S】などの目印で始まる場合、その目印を取り除いて本文だけを取り出す関数
def extract_after_marker(text: str, marker: str) -> str:
    t = text.strip()  # テキストの前後の空白・改行を削る
    if t.startswith(marker):  # 先頭が marker（例："【S】"）なら
        return t[len(marker):].lstrip()  # marker分を切り落として、残りの先頭空白も削って返す
    return t  # markerで始まっていなければ、そのまま返す


# 文字数を数える関数（日本語は len() でおおむね「文字数」として数えられる）
def char_count(s: str) -> int:
    return len(s)  # 文字列の長さ（文字数）を返す


# 全体の流れ（入力→質問生成→回答入力→小説生成→条件チェック→出力）をまとめたメイン関数
def main():
    # APIキーが環境変数に無いとOpenAIに接続できないので、最初にチェックする
    if not os.getenv("OPENAI_API_KEY"):
        print("ERROR: 環境変数 OPENAI_API_KEY が見つかりません。")  # エラーメッセージを表示
        print('PowerShell例:  setx OPENAI_API_KEY "あなたのAPIキー"')  # 設定方法を案内
        return  # これ以上進めないので終了

    # プログラムが始まったことがわかるようにタイトル表示
    print("=== 400字ショートショート作成サポート ===")

    # ユーザーから「題材」を1行入力してもらい、前後空白を削る
    theme = input("題材（1行）: ").strip()

    # 任意の補足情報も入力してもらい、前後空白を削る（空でもOK）
    optional = input("追加情報（任意・空OK）: ").strip()

    # 1) 質問フェーズ用のプロンプト（題材と追加情報を渡し、質問だけ出させる）
    q_prompt = f"""題材：{theme}
追加情報：{optional}

まずは質問フェーズです。ルール通り【Q】で最大3問だけ出してください。小説は書かないでください。"""

    # LLMに質問生成を依頼し、返ってきた文章を q_out に保存
    q_out = call_llm(q_prompt)

    # 質問フェーズの出力をユーザーに見せる
    print("\n--- ハロからの質問 ---")
    print(q_out)

    # 2) ユーザーの回答を「複数行」で受け付ける（空行が来たら入力終了）
    print("\n上の質問に答えてください（まとめて入力OK）。空行で確定。")
    lines = []  # 入力された行をためるリスト
    while True:
        line = input()  # 1行入力
        if line == "":  # 空行なら終了
            break
        lines.append(line)  # 空行でなければリストに追加

    # 入力された複数行を改行でつないで、1つの回答文章にする
    user_answers = "\n".join(lines).strip()

    # 3) 小説生成用のプロンプト（質問と回答を渡して、【S】で始まる本文だけを出させる）
    s_prompt = f"""題材：{theme}
追加情報：{optional}

質問：
{q_out}

ユーザー回答：
{user_answers}

いまから小説フェーズ。ルール通り【S】で始めて、本文だけを出力してください。"""

    # LLMに小説生成を依頼し、その返答を s_out に保存
    s_out = call_llm(s_prompt)

    # 返答から【S】を取り除いて本文だけを取り出す（念のため strip() も）
    story = extract_after_marker(s_out, "【S】").strip()

    # 4) 文字数と会話がルール通りか最低限チェックし、ズレていたら改稿させる準備
    need_fix = False  # 修正が必要かどうかのフラグ

    # 文字数が380〜420の範囲外なら修正が必要
    if not (380 <= char_count(story) <= 420):
        need_fix = True

    # 会話のカギ括弧「」が無いなら修正が必要
    if "「" not in story or "」" not in story:
        need_fix = True

    # ルール違反があった場合は、同じ内容を保ちながら条件を満たすように改稿させる
    if need_fix:
        fix_prompt = f"""次の本文を、条件を満たすように改稿してください。

【条件】
- 380〜420字（句読点含む）
- 会話「」を必ず1回入れる
- 説教／教訓の直説は禁止
- 最後の1文で軽いひねり（オチor余韻）
- 固有名詞は最小限、説明は短く、出来事で見せる
- 先頭に【S】を付け、本文だけを出力

【本文】
{story}
"""
        fixed = call_llm(fix_prompt)  # 改稿をLLMに依頼
        story = extract_after_marker(fixed, "【S】").strip()  # 改稿結果から本文だけを取り出す

    # 最終結果を表示
    print("\n=== 完成した400字小説 ===")
    print(story)

    # 参考として最終的な文字数も表示
    print(f"\n（文字数: {char_count(story)}）")


# このファイルが「直接実行されたときだけ」main() を呼び出すお決まりの書き方
if __name__ == "__main__":
    main()