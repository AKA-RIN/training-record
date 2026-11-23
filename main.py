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
      f'前回（{last['日時']}）：{default_weight}kg × {default_reps}回 ×'
        f' {default_sets}セット'
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
        weight = st.number_input('重量(kg)', min_value=0.0, step=2.5, value=30.0)

    with col2:
        reps = st.number_input('回数', min_value=1, step=1, value=10)

    with col3:
        sets = st.number_input('セット数', min_value=1, step=1, value=3)

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

# 記録一覧の表示
st.subheader('過去の記録')

if not df.empty:
    st.dataframe(df.iloc[::-1], width='stretch')
else:
    st.info('まだ記録がありません。')


# streamlit run training_record/main.pyで起動