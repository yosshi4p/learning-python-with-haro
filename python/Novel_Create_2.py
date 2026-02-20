
####VisualStudioCodeで動く、ショートショート小説を書くPythonのコードです。
# 約400字数の小説です。説教臭くないエンタメとして面白い小説です。
# 小説を書くために必要な質問があれば事前に尋ねてください。
# openAIのAPIキーを使用できます。###
import os
from openai import OpenAI

# ------------------------------------------------------------
# 設定：モデル（まずは動作優先なら gpt-4o-mini が堅い）
# ------------------------------------------------------------
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

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
""".strip()

client = OpenAI()


def call_llm(user_text: str) -> str:
    """
    openai==2.21.0 向け：Chat Completions で呼び出す
    """
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text},
        ],
    )
    return (resp.choices[0].message.content or "").strip()


def extract_after_marker(text: str, marker: str) -> str:
    t = text.strip()
    if t.startswith(marker):
        return t[len(marker):].lstrip()
    return t


def char_count(s: str) -> int:
    return len(s)


def main():
    if not os.getenv("OPENAI_API_KEY"):
        print("ERROR: 環境変数 OPENAI_API_KEY が見つかりません。")
        print('PowerShell例:  setx OPENAI_API_KEY "あなたのAPIキー"')
        return

    print("=== 400字ショートショート作成サポート ===")
    theme = input("題材（1行）: ").strip()
    optional = input("追加情報（任意・空OK）: ").strip()

    # 1) 質問フェーズ
    q_prompt = f"""題材：{theme}
追加情報：{optional}

まずは質問フェーズです。ルール通り【Q】で最大3問だけ出してください。小説は書かないでください。"""
    q_out = call_llm(q_prompt)

    print("\n--- ハロからの質問 ---")
    print(q_out)

    # 2) 回答をまとめて入力（複数行OK、空行で確定）
    print("\n上の質問に答えてください（まとめて入力OK）。空行で確定。")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    user_answers = "\n".join(lines).strip()

    # 3) 小説生成
    s_prompt = f"""題材：{theme}
追加情報：{optional}

質問：
{q_out}

ユーザー回答：
{user_answers}

いまから小説フェーズ。ルール通り【S】で始めて、本文だけを出力してください。"""
    s_out = call_llm(s_prompt)
    story = extract_after_marker(s_out, "【S】").strip()

    # 4) 文字数・会話の最低限チェック（ズレたら自動改稿）
    need_fix = False
    if not (380 <= char_count(story) <= 420):
        need_fix = True
    if "「" not in story or "」" not in story:
        need_fix = True

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
        fixed = call_llm(fix_prompt)
        story = extract_after_marker(fixed, "【S】").strip()

    print("\n=== 完成した400字小説 ===")
    print(story)
    print(f"\n（文字数: {char_count(story)}）")


if __name__ == "__main__":
    main()

