from datetime import datetime
import os
import pandas as pd
import streamlit as st

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, 'workout_log.csv')


st.title('筋トレ記録')
exercises= [
    'チェストプレス',
    'ショルダープレス',
    'ラットプルダウン',
    'レッグプレス',
    'アブドミナルクランチ',
    'アダクター',
    'アブダクター',
    'レッグカール',
    'レッグエクステンション',
    'バックエクステンション'
]

# CSV読み込み
if os.path.exists(CSV_FILE):
    df = pd.read_csv(CSV_FILE)
else:
    df = pd.DataFrame(columns=['日時', '種目', '重量', '回数', 'セット数'])

exercise = st.selectbox('種目', exercises)

past_records = df[df['種目'] == exercise]
if not past_records.empty:
    last = past_records.iloc[-1]

    default_weight = float(last['重量'])
    default_reps = int(last['回数'])
    default_sets = int(last['セット数'])

    st.caption(
      f"前回（{last['日時']}）：{default_weight}kg × {default_reps}回 ×"
        f" {default_sets}セット"
    )
else:
    default_weight = 30.0
    default_reps = 10
    default_sets = 3
    st.caption('前回：記録なし')

# 入力フォーム
with st.form('record_form', clear_on_submit=False):
    col1, col2, col3 = st.columns(3)

    with col1:
        weight = st.number_input(
            '重量(kg)',
            min_value=0.0,
            step=2.5,
            value=default_weight,
            key=f'weight_{exercise}'
        )

    with col2:
        reps = st.number_input(
            '回数',
            min_value=1,
            step=1,
            value=default_reps,
            key=f'reps_{exercise}'
        )

    with col3:
        sets = st.number_input(
            'セット数',
            min_value=1,
            step=1,
            value=default_sets,
            key=f'sets_{exercise}'
        )

    submitted = st.form_submit_button('記録する')

# 保存処理
if submitted:
    new_data = pd.DataFrame([{
        '日時': datetime.now().strftime('%Y-%m-%d %H:%M'),
        '種目': exercise,
        '重量': weight,
        '回数': reps,
        'セット数': sets,
    }])

    if os.path.exists(CSV_FILE):
        new_data.to_csv(CSV_FILE, mode='a', header=False, index=False)
    else:
        new_data.to_csv(CSV_FILE, index=False)

    df = pd.read_csv(CSV_FILE)

    st.success(f'記録しました：{exercise} {weight}kg × {reps}回 × {sets}セット')

# 進捗確認
st.subheader('今日のメニューの進捗')

today_str = datetime.now().strftime('%Y-%m-%d')

if not df.empty:
    today_df = df[df['日時'].astype(str).str.startswith(today_str)]
    done_exercises = today_df['種目'].unique().tolist()
else:
    done_exercises = []

st.progress(
    len(done_exercises) / len(exercises),
    text=f'完了：{len(done_exercises)} / {len(exercises)} 種目'
)

col_left, col_right = st.columns(2)
half = len(exercises) // 2

for i , ex in enumerate(exercises):
    status = f'✅{ex}' if ex in done_exercises else f'◻️{ex}'

    if i < half:
        col_left.write(status)
    else:
        col_right.write(status)

# 記録一覧の表示
st.subheader('過去の記録')

if not df.empty:
    st.dataframe(df.iloc[::-1], width='stretch')
else:
    st.info('まだ記録がありません。')


# streamlit run training_record/main.pyで起動