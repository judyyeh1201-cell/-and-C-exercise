import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

# --- 設定基本參數 ---
START_DATE = datetime(2025, 12, 22).date()
DATA_FILE = "exercise_log.csv"

# 設定頁面資訊
st.set_page_config(page_title="兒童運動獎勵表", page_icon="🏆")

# --- 1. 資料處理函數 ---
def load_data():
    if not os.path.exists(DATA_FILE):
        return pd.DataFrame(columns=["Date", "Child", "Activity", "Note", "Week_Start"])
    return pd.read_csv(DATA_FILE)

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

def get_week_start(date_obj):
    """取得該日期所屬週的'週一'日期"""
    start = date_obj - timedelta(days=date_obj.weekday())
    return start

# --- 2. 介面設計 ---
st.title("🏆 兒童每週運動挑戰賽")
st.write(f"📅 挑戰起始日：{START_DATE} (每週一結算)")

# 選擇使用者
user = st.radio("請問是誰要紀錄？", ["Jacqueline", "Cheryl"], horizontal=True)

# 設定角色專屬主題
if user == "Jacqueline":
    avatar = "🐰"
    theme_color = "pink"
    st.markdown(f"### {avatar} Jacqueline 的兔子運動站")
else:
    avatar = "🦊"
    theme_color = "orange"
    st.markdown(f"### {avatar} Cheryl 的狐狸訓練營")

# --- 3. 新增紀錄區塊 ---
with st.expander(f"➕ 新增今天的運動紀錄 ({avatar})", expanded=True):
    with st.form("entry_form"):
        col1, col2 = st.columns(2)
        with col1:
            date_input = st.date_input("運動日期", datetime.now())
        with col2:
            activity = st.selectbox("運動項目", ["跑步 (30分鐘)", "跳繩 (500下)", "游泳", "騎腳踏車", "球類運動", "其他"])
        
        note = st.text_input("備註 (例如：跟爸爸一起跑、很累但堅持住了)")
        
        submitted = st.form_submit_button("✅ 提交紀錄")
        
        if submitted:
            # 檢查日期是否早於開始計畫日
            if date_input < START_DATE:
                st.error("不能記錄 2025/12/22 以前的資料喔！")
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
                st.success(f"{avatar} 太棒了！紀錄成功！")
                st.rerun()

# --- 4. 統計與獎勵區塊 ---
st.divider()
st.subheader("💰 本週成績與獎勵")

# 讀取資料
df = load_data()
if not df.empty:
    # 轉換日期格式以便計算
    df["Date"] = pd.to_datetime(df["Date"]).dt.date
    df["Week_Start"] = pd.to_datetime(df["Week_Start"]).dt.date

    # 找出「本週」的起始日 (以今天為準，或是以最後輸入的日期為準)
    current_week_start = get_week_start(datetime.now().date())
    
    # 篩選出該位小孩 + 本週的資料
    this_week_data = df[(df["Child"] == user) & (df["Week_Start"] == current_week_start)]
    
    count = len(this_week_data)
    
    # 顯示進度條
    st.write(f"本週 ({current_week_start} ~ {current_week_start + timedelta(days=6)}) 累積次數： **{count} 次**")
    
    # 計算獎金邏輯
    reward = 0
    next_goal = ""
    
    if count >= 5:
        reward = 500
        st.balloons() # 達標放氣球
        st.success(f"🎉 太厲害了！本週運動 {count} 次，獲得獎金 **${reward} 元**！")
    elif count >= 4:
        reward = 200
        next_goal = "再 1 次就可以拿 $500 囉！"
        st.info(f"👍 很棒！本週運動 {count} 次，獲得獎金 **${reward} 元**！ ({next_goal})")
    elif count >= 3:
        reward = 100
        next_goal = "再 1 次就可以拿 $200 囉！"
        st.warning(f"🥉 恭喜達標！本週運動 {count} 次，獲得獎金 **${reward} 元**！ ({next_goal})")
    else:
        remaining = 3 - count
        st.write(f"💪 加油！再運動 **{remaining} 次** 就可以獲得 $100 元零用錢！")

    # 進度條視覺化
    progress = min(count / 5.0, 1.0)
    st.progress(progress)

    # --- 5. 歷史紀錄表格 ---
    st.markdown("---")
    st.write(f"📜 {user} 的本週詳細紀錄")
    if not this_week_data.empty:
        st.table(this_week_data[["Date", "Activity", "Note"]])
    else:
        st.caption("本週還沒有紀錄喔，快去運動吧！")

else:
    st.info("目前還沒有任何資料，快開始第一次運動吧！")