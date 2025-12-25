import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

# --- 設定基本參數 ---
# 繼續沿用原本的檔案，方便你操作
DATA_FILE = "exercise_data_v2.csv"
START_DATE = datetime(2025, 12, 22).date()

st.set_page_config(page_title="兒童運動獎勵表", page_icon="🏆")

# --- 1. 資料處理函數 ---
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

# --- 2. 介面標題 ---
st.title("🏆 兒童每週運動挑戰賽 (V5)")
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

    # --- 統計與獎勵 ---
    st.divider()
    df = load_data()
    if not df.empty:
        # 簡單容錯處理
        try:
            df["Date"] = pd.to_datetime(df["Date"]).dt.date
            df["Week_Start"] = pd.to_datetime(df["Week_Start"]).dt.date
        except:
            pass # 如果轉換失敗就跳過，避免報錯

        current_week_start = get_week_start(datetime.now().date())
        this_week_data = df[(df["Child"] == user) & (df["Week_Start"] == current_week_start)]
        count = len(this_week_data)
        
        st.subheader(f"💰 {user} 本週成績單")
        st.write(f"本週 ({current_week_start}) 累積次數： **{count} 次**")
        
        if count >= 5:
            st.balloons()
            st.success(f"🎉 獲得獎金 **$500 元**！")
        elif count >= 4:
            st.info(f"👍 獲得獎金 **$200 元**！")
        elif count >= 3:
            st.warning(f"🥉 獲得獎金 **$100 元**！")
        else:
            remaining = 3 - count
            st.write(f"💪 加油！再運動 **{remaining} 次** 就可以獲得 $100 元零用錢！")
            
        st.progress(min(count / 5.0, 1.0))
        
        if not this_week_data.empty:
             with st.expander("查看本週詳細紀錄"):
                st.table(this_week_data[["Date", "Activity", "Note"]])

# --- Tab 2: 管理區 (新增清空按鈕) ---
with tab2:
    st.subheader("🛠️ 資料管理")
    
    df_all = load_data()
    
    # === 新增功能：一鍵清空 ===
    with st.expander("⚠️ 危險區域：清空資料", expanded=False):
        st.write("點擊下方按鈕將會 **刪除所有紀錄**，無法復原！")
        if st.button("🗑️ 確定清空所有資料 (Reset)", type="primary"):
            # 寫入一個空的 DataFrame 來覆蓋舊檔案
            empty_df = pd.DataFrame(columns=["Date", "Child", "Activity", "Note", "Week_Start"])
            save_data(empty_df)
            st.success("資料已全部清空！")
            st.rerun()
    # ========================

    st.divider()

    if df_all.empty:
        st.info("目前沒有資料。")
    else:
        st.write("下方表格可以修改內容：")
        edited_df = st.data_editor(
            df_all,
            num_rows="dynamic",
            use_container_width=True,
            key="editor_v5"
        )
        
        if st.button("💾 儲存表格修改"):
            if not edited_df.empty:
                edited_df["Date"] = pd.to_datetime(edited_df["Date"]).dt.date
                edited_df["Week_Start"] = edited_df["Date"].apply(get_week_start)
            save_data(edited_df)
            st.success("表格已更新！")
            st.rerun()
