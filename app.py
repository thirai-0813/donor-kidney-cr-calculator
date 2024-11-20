import streamlit as st
import numpy as np

# タイトルと概要
st.title("ドナー腎提供後1年後の予測Cr値")
st.write("""
このアプリは、体重、クレアチニン値、非摘出腎容積、性別を入力して
提供1年後のクレアチニン値を計算するツールです。
""")

# 各項目の説明を最初に記載
st.markdown("""
### 入力項目の説明
- **Body Weight (Bw)**: ドナーの体重（kg単位）
- **Creatinine (Cre)**: 術前の血中クレアチニン値（mg/dL）
- **Non-Excised Kidney Volume**: CTで測定した非摘出腎の容積（単位：mL）
- **Male (1 for Male, 0 for Female)**: 性別（男性: 1、女性: 0）
""")

# 入力フォーム
st.write("以下のパラメータを入力してください：")
Bw = st.number_input("Body Weight (Bw)", min_value=0.0, step=0.1)
Cre = st.number_input("Creatinine (Cre)", min_value=0.0, step=0.01)
NonExcisedKidney = st.number_input("Non-Excised Kidney Volume", min_value=0.0, step=0.1)
Male = st.selectbox("Male (1 for Male, 0 for Female)", options=[1, 0])

# Simplify_model calculation function
def calculate_simplify_model(Bw, Cre, NonExcisedKidney, Male, Age=50):
    # Fixed values
    CVD_replaced = 0
    HbA1C_replaced = 5.7
    BUN_replaced = 13.8

    # Model calculations
    model_1 = -0.09903755662234529 + 0.006502924180113298 * Bw + 1.3625035862329375 * np.sqrt(Cre) + 0.1139767991517405 * Male - 0.0027455075816872963 * NonExcisedKidney
    model_2 = -0.3901364879414445 + 0.04471756216946074 * BUN_replaced + 0.006715659519617908 * Bw + 1.0352518798689898 * Cre - 0.000009604315179117748 * BUN_replaced**2 * NonExcisedKidney
    model_3 = -0.38478682583687274 + 0.002081547696286225 * Age + 0.04399956263153849 * BUN_replaced + 0.005628920758504391 * Bw + 0.9320131800396743 * Cre + 0.06722065750493375 * Male - 0.000009867424180159245 * BUN_replaced**2 * NonExcisedKidney
    model_4 = 0.049617816124754036 + 0.9225151798784034 * Cre + 0.18320900637720863 * CVD_replaced + 0.10349178758374927 * HbA1C_replaced + 0.13985579153513217 * Male - 0.0019323076033121343 * NonExcisedKidney
    model_5 = -0.18899026587394271 + 0.024398835894397737 * BUN_replaced + 0.0032842131730298754 * Bw + 1.142965718977502e-9 * BUN_replaced**4 * NonExcisedKidney
    model_6 = -0.006961262066861628 + 0.8126766126098913 * Cre + 0.11057326356803435 * Male + 1.4573284728625062 / (0.7326765340341233 + NonExcisedKidney / Bw)
    model_7 = 0.005082859737290714 + 0.03531000856642338 * BUN_replaced + 0.00699894215253158 * Bw + 0.7899600124990199 * Cre + 0.10910119812549417 * Male - 0.0002167791209982864 * BUN_replaced * NonExcisedKidney
    model_8 = 1.2549512514779957 + 0.005164327440285673 * Bw + 0.8188362941962077 * Cre - 4.127069601506772 / (CVD_replaced + HbA1C_replaced + Male) - 0.0026704663767301066 * NonExcisedKidney
    model_9 = -0.15903717053578167 + 0.00025977004836070643 * Age * BUN_replaced + 0.005291867117086743 * Bw + 1.0913423662894317 * Cre - 6.322735119054266e-12 * BUN_replaced**3 * NonExcisedKidney**3

    # Calculate median of all models
    simplify_model = np.median([model_1, model_2, model_3, model_4, model_5, model_6, model_7, model_8, model_9], axis=0)
    return simplify_model


# 計算ボタン
if st.button("Calculate"):
    try:
        # 結果の計算
        result = calculate_simplify_model(Bw, Cre, NonExcisedKidney, Male)
        st.success(f"あなたの腎提供1年後の予測クレアチニン値は以下の通りです（単位mg/dL): {result:.2f}")  # 小数点2桁で表示
        
        # 注意書き
        st.write("""
        **この結果は東京女子医科大学泌尿器科で実際に腎提供された患者さまのデータを元に算出しています。
        実際の測定値とは異なる可能性があることをご了承ください。**
        """)
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")







