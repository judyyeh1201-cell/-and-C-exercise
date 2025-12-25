import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

# --- 1. 改一個新檔名，避開舊的壞資料 ---
DATA_FILE = "exercise_data_v2.csv"
START_DATE = datetime(2025, 12, 22).date()

st.set_page_config(page_title="兒童運動獎勵表", page_icon="🏆")

# --- 資料處理 ---
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
    start = date_obj - timedelta(days=date_obj.weekday())
    return start

# --- 2. 標題 ---
st.title("🏆 兒童每週運動挑戰賽 (V3 成功版)")
st.caption(f"📅 挑戰起始日：{START_DATE}")

tab1, tab2 = st.tabs(["📝 紀錄運動", "🛠️ 管理紀錄"])

# --- Tab 1: 紀錄區 ---
with tab1:
    user = st.radio("請問是誰要紀錄？", ["Jacqueline", "Cheryl"], horizontal=True)
    
    if user == "Jacqueline":
        st.info("### 🐰 Jacqueline 的兔子運動站")
    else:
        st.warning("### 🦊 Cheryl 的狐狸訓練營")

    with st.form("entry_form"):
        col1, col2 = st.columns(2)
        with col1:
            date_input = st.date_input("運動日期", datetime.now())
        with col2:
            activity = st.selectbox("運動項目", ["跑步 (30分鐘)", "跳繩 (500下)", "游泳", "其他"])
        
        note = st.text_input("備註")
        submitted = st.form_submit_button("✅ 提交紀錄")
        
        if submitted:
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
            st.success("紀錄成功！")
            st.rerun()

    # 統計
    st.divider()
    df = load_data()
    if not df.empty:
        # 簡單處理日期格式，避免報錯
        df["Date"] = pd.to_datetime(df["Date"]).dt.date
        df["Week_Start"] = pd.to_datetime(df["Week_Start"]).dt.date
        
        current_week_start = get_week_start(datetime.now().date())
        this_week_data = df[(df["Child"] == user) & (df["Week_Start"] == current_week_start)]
        count = len(this_week_data)
        
        st.write(f"本週 ({current_week_start}) 累積次數： **{count} 次**")
        
        if count >= 3:
            st.balloons()
            st.success(f"🎉 恭喜！本週已運動 {count} 次，達標了！")
        else:
            st.write(f"💪 加油！再運動 {3-count} 次就有獎勵了！")
            
        st.progress(min(count/5.0, 1.0))

# --- Tab 2: 管理區 (最簡化版) ---
with tab2:
    st.subheader("🛠️ 資料管理")
    
    df_all = load_data()
    
    if df_all.empty:
        st.info("目前沒有資料，請先去新增一筆紀錄。")
    else:
        st.write("勾選左邊可以用來刪除：")
        # 3. 簡化表格設定，先把容易出錯的 config 拿掉
        edited_df = st.data_editor(
            df_all,
            num_rows="dynamic",
            use_container_width=True,
            key="simple_editor"
        )
        
        if st.button("💾 儲存修改"):
            save_data(edited_df)
            st.success("資料已更新！")
            st.rerun()
