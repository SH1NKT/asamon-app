import streamlit as st
import pandas as pd
import random

st.set_page_config(
    page_title="診断士 朝問アーカイブ",
    page_icon="📚",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans JP', sans-serif;
}

.main-title {
    text-align: center;
    font-size: 2rem;
    font-weight: 900;
    color: #1a1a2e;
    margin-bottom: 0.2rem;
}

.sub-title {
    text-align: center;
    font-size: 0.9rem;
    color: #888;
    margin-bottom: 2rem;
}

.question-box {
    background: #f8f9ff;
    border-left: 5px solid #4361ee;
    border-radius: 8px;
    padding: 1.2rem 1.5rem;
    font-size: 1.05rem;
    font-weight: 700;
    color: #1a1a2e;
    margin-bottom: 1.2rem;
    line-height: 1.7;
}

.correct-box {
    background: #e8f5e9;
    border: 2px solid #4caf50;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    color: #2e7d32;
    font-weight: 700;
    font-size: 1rem;
    margin-top: 1rem;
}

.wrong-box {
    background: #fce4ec;
    border: 2px solid #e91e63;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    color: #880e4f;
    font-weight: 700;
    font-size: 1rem;
    margin-top: 1rem;
}

.explanation-box {
    background: #fff8e1;
    border-left: 4px solid #ffc107;
    border-radius: 6px;
    padding: 1rem 1.2rem;
    font-size: 0.93rem;
    color: #333;
    margin-top: 1rem;
    line-height: 1.8;
}

.stat-badge {
    display: inline-block;
    background: #e8eaf6;
    color: #3949ab;
    border-radius: 20px;
    padding: 0.2rem 0.8rem;
    font-size: 0.82rem;
    font-weight: 700;
    margin-right: 0.4rem;
}

.subject-tag {
    display: inline-block;
    background: #4361ee;
    color: white;
    border-radius: 4px;
    padding: 0.15rem 0.6rem;
    font-size: 0.78rem;
    font-weight: 700;
    margin-bottom: 0.8rem;
}

.counter-box {
    text-align: center;
    font-size: 0.85rem;
    color: #888;
    margin-bottom: 1.5rem;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# データ読み込み
# ============================================================

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("asamon.csv", encoding="utf-8-sig")
    except Exception:
        df = pd.DataFrame([
            {
                "id": "001",
                "subject": "経営法務",
                "question": "法定相続人と法定相続分の組み合わせとして、最も適切なのはどれ？",
                "choice_ア": "配偶者と子：配偶者1/2・子1/2",
                "choice_イ": "配偶者と親：配偶者1/3・親2/3",
                "choice_ウ": "配偶者と兄弟姉妹：配偶者2/3・兄弟1/3",
                "answer": "ア",
                "explanation": "法定相続分は相続人の組み合わせによって異なります。配偶者と子の場合は1/2ずつが正しい組み合わせです。",
                "correct_rate_insta": "86",
                "correct_rate_x": "54",
            },
            {
                "id": "002",
                "subject": "経営情報システム",
                "question": "ディープラーニングの説明として、最も適切なものはどれ？",
                "choice_ア": "入力層・出力層のみで構成される",
                "choice_イ": "特徴量を自動的に学習できる",
                "choice_ウ": "少量のデータで高精度が出る",
                "answer": "イ",
                "explanation": "ディープラーニングは特徴量を自動的に学習できる点が最大の強みです。",
                "correct_rate_insta": "80",
                "correct_rate_x": "71",
            },
        ])
    df = df[df["choice_ア"].notna() & df["choice_ア"].str.strip().ne("")]
    df = df.reset_index(drop=True)
    return df

df = load_data()

# ============================================================
# セッション初期化
# ============================================================

if "current_idx" not in st.session_state:
    st.session_state.current_idx = 0
if "answered" not in st.session_state:
    st.session_state.answered = False
if "selected" not in st.session_state:
    st.session_state.selected = None
if "filtered_df" not in st.session_state:
    st.session_state.filtered_df = df

# ============================================================
# サイドバー
# ============================================================

st.sidebar.markdown("## ⚙️ 設定")

subjects = ["すべて"] + sorted(df["subject"].dropna().unique().tolist())
selected_subject = st.sidebar.selectbox("科目", subjects)
mode = st.sidebar.radio("出題順", ["順番", "ランダム"])

if st.sidebar.button("🔄 条件を適用"):
    filtered = df.copy()
    if selected_subject != "すべて":
        filtered = filtered[filtered["subject"] == selected_subject]
    if mode == "ランダム":
        filtered = filtered.sample(frac=1).reset_index(drop=True)
    st.session_state.filtered_df = filtered
    st.session_state.current_idx = 0
    st.session_state.answered = False
    st.session_state.selected = None
    st.rerun()

filtered_df = st.session_state.filtered_df

# ============================================================
# メインUI
# ============================================================

st.markdown('<div class="main-title">📚 診断士 朝問アーカイブ</div>', unsafe_allow_html=True)
st.markdown('''
<div class="sub-title">
    中小企業診断士 1次試験 オリジナル問題集<br>
    作成者：中小企業診断士 仲田俊一<br>
    <a href="https://x.com/nakata4dan4" target="_blank">𝕏 @nakata4dan4</a>　
    <a href="https://www.instagram.com/shindanshi.1day1neta" target="_blank">📷 Instagram</a>
</div>
''', unsafe_allow_html=True)

if len(filtered_df) == 0:
    st.warning("該当する問題がありません。条件を変更してください。")
    st.stop()

idx = st.session_state.current_idx
if idx >= len(filtered_df):
    st.success("🎉 全問終了！お疲れ様でした。")
    if st.button("最初からやり直す"):
        st.session_state.current_idx = 0
        st.session_state.answered = False
        st.session_state.selected = None
        st.rerun()
    st.stop()

row = filtered_df.iloc[idx]

st.markdown(f'<div class="counter-box">{idx + 1} / {len(filtered_df)} 問</div>', unsafe_allow_html=True)

subject = str(row.get("subject", ""))
if subject and subject != "nan":
    st.markdown(f'<span class="subject-tag">{subject}</span>', unsafe_allow_html=True)

question = str(row.get("question", ""))
st.markdown(f'<div class="question-box">{question}</div>', unsafe_allow_html=True)

choices = {
    "ア": str(row.get("choice_ア", "")),
    "イ": str(row.get("choice_イ", "")),
    "ウ": str(row.get("choice_ウ", "")),
}
answer = str(row.get("answer", "")).strip()

if not st.session_state.answered:
    for key, text in choices.items():
        if text and text != "nan":
            if st.button(f"{key}．{text}", key=f"choice_{key}", use_container_width=True):
                st.session_state.selected = key
                st.session_state.answered = True
                st.rerun()
else:
    selected = st.session_state.selected
    for key, text in choices.items():
        if text and text != "nan":
            if key == answer:
                st.markdown(f'✅ **{key}．{text}**')
            elif key == selected and key != answer:
                st.markdown(f'❌ ~~{key}．{text}~~')
            else:
                st.markdown(f'　{key}．{text}')

    if selected == answer:
        st.markdown('<div class="correct-box">🎉 正解！素晴らしい！</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="wrong-box">😢 不正解... 正解は「{answer}」でした</div>', unsafe_allow_html=True)

    insta = str(row.get("correct_rate_insta", ""))
    x_rate = str(row.get("correct_rate_x", ""))
    if insta and insta not in ["nan", ""]:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            f'<span class="stat-badge">📸 インスタ正答率 {insta}%</span>'
            f'<span class="stat-badge">🐦 X正答率 {x_rate}%</span>',
            unsafe_allow_html=True
        )

    explanation = str(row.get("explanation", ""))
    if explanation and explanation != "nan":
        st.markdown(
            f'<div class="explanation-box">📝 <strong>解説</strong><br><br>{explanation}</div>',
            unsafe_allow_html=True
        )

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⏭ 次の問題へ", use_container_width=True):
            st.session_state.current_idx += 1
            st.session_state.answered = False
            st.session_state.selected = None
            st.rerun()
    with col2:
        if st.button("⏩ スキップ", use_container_width=True):
            st.session_state.current_idx += 1
            st.session_state.answered = False
            st.session_state.selected = None
            st.rerun()