import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

# --- 設定基本參數 ---
# 為了不讓你剛剛測試的資料不見，我們繼續沿用 v2 的檔案
DATA_FILE = "exercise_data_v2.csv"
START_DATE = datetime(2025, 12, 22).date()

st.set_page_config(page_title="兒童運動獎勵表", page_icon="🏆")

# --- 1. 資料處理函數 (保持 V3 的穩定性) ---
def load_data():
    if not os.path.exists(DATA_FILE):
        return pd.DataFrame(columns=["Date", "Child", "Activity", "Note", "Week_Start"])
    
    try:
        df = pd.read_csv(DATA_FILE)
        if df.empty:
            return pd.DataFrame(columns=["Date", "Child", "Activity", "Note", "Week_Start"])
        return df
    except:
        return pd.DataFrame(columns=["Date", "Child", "Activity", "Note", "Week_Start"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

def get_week_start(date_obj):
    """取得該日期所屬週的'週一'日期"""
    start = date_obj - timedelta(days=date_obj.weekday())
    return start

# --- 2. 介面標題 ---
st.title("🏆 兒童每週運動挑戰賽 (V4)")
st.caption(f"📅 挑戰起始日：{START_DATE} (每週一結算)")

tab1, tab2 = st.tabs(["📝 紀錄運動", "🛠️ 管理紀錄"])

# --- Tab 1: 紀錄區 ---
with tab1:
    user = st.radio("請問是誰要紀錄？", ["Jacqueline", "Cheryl"], horizontal=True)
    
    if user == "Jacqueline":
        avatar = "🐰"
        st.info(f"### {avatar} Jacqueline 的兔子運動站")
    else:
        avatar = "🦊"
        st.warning(f"### {avatar} Cheryl 的狐狸訓練營")

    with st.form("entry_form"):
        col1, col2 = st.columns(2)
        with col1:
            date_input = st.date_input("運動日期", datetime.now())
        with col2:
            activity = st.selectbox("運動項目", ["跑步 (30分鐘)", "跳繩 (500下)", "游泳", "騎腳踏車", "球類運動", "其他"])
        
        note = st.text_input("備註")
        submitted = st.form_submit_button("✅ 提交紀錄")
        
        if submitted:
            if date_input < START_DATE:
                st.error("不能記錄開始日之前的資料喔！")
            else:
                df = load_data()
                week_start = get_week_start(date_input)
                new_entry = pd.DataFrame({
                    "Date": [date_input],
                    "Child": [user],
                    "Activity": [activity],
                    "Note": [note],
                    "Week_Start": [week_start]
                })
                df = pd.concat([df, new_entry], ignore_index=True)
                save_data(df)
                st.success(f"{avatar} 紀錄成功！")
                st.rerun()

    # --- 3. 統計與獎勵 (這裡修復了！) ---
    st.divider()
    df = load_data()
    if not df.empty:
        # 轉換格式
        df["Date"] = pd.to_datetime(df["Date"]).dt.date
        df["Week_Start"] = pd.to_datetime(df["Week_Start"]).dt.date
        
        # 抓取「本週」的資料
        current_week_start = get_week_start(datetime.now().date())
        this_week_data = df[(df["Child"] == user) & (df["Week_Start"] == current_week_start)]
        count = len(this_week_data)
        
        st.subheader(f"💰 {user} 本週成績單")
        st.write(f"本週 ({current_week_start}) 累積次數： **{count} 次**")
        
        # --- 獎勵邏輯 ---
        if count >= 5:
            st.balloons() # 放氣球
            st.success(f"🎉 太厲害了！本週運動 {count} 次，獲得獎金 **$500 元**！")
        elif count >= 4:
            st.info(f"👍 很棒！本週運動 {count} 次，獲得獎金 **$200 元**！ (再 1 次就可以拿 $500 囉！)")
        elif count >= 3:
            st.warning(f"🥉 恭喜達標！本週運動 {count} 次，獲得獎金 **$100 元**！ (再 1 次就可以拿 $200 囉！)")
        else:
            remaining = 3 - count
            st.write(f"💪 加油！再運動 **{remaining} 次** 就可以獲得 $100 元零用錢！")
