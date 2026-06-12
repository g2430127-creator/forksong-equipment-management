import datetime
import os
import pandas as pd
import streamlit as st

# 1. ページの設定
st.set_page_config(page_title="フォークソング研究部部費管理システム", page_icon="💰", layout="wide")

st.title("💰 フォークソング研究部 部費管理システム")
st.markdown("---")

# 📌 データを保存するCSVファイルの名前
CSV_FILE = "club_fees.csv"

# 💡 画面上の操作があったら自動でCSVに上書き保存する関数
def save_data_to_csv():
    st.session_state.member_data.to_csv(CSV_FILE, index=False, encoding="utf-8-sig")

# 2. データの初期化・読み込みロジック
# 💡 ご提示いただいた36名分のリアルデータを完全に反映
actual_data = {
    "部員名": [
        "金島 暖斗", "永野 煌斗", "荻野 実夏", "松本 祥", "中原 颯太",
        "中村 那菜圭", "城戸 綾香", "山口 紗季", "白濱 瑞稀", "南 小雪",
        "上村 遼珈", "坂田 頼治", "松永 駿介", "伊津野 菜音", "後藤 美穂",
        "緒方 桂太郎", "秋吉 純之介", "木下 澪", "髙田 興悟", "髙橋 育椰",
        "前崎 優太", "向井 教華", "麻生 英里香", "田中 煌騎", "香月 春乃",
        "北口 稜", "坂本 ひかり", "高藤 侑和", "福留 恋杏", "伊藤 雅仁",
        "井上 依香", "大西 蒼", "大町 丈琉", "亀田 淳奈", "川野 莉瑚",
        "神﨑 凜", "久保玉井 祐花"
    ],
    "学年": [
        "4年", "4年", "4年", "4年", "4年", "4年", "4年", "4年", "4年", "4年",
        "4年", "4年", "4年", "3年", "3年", "3年", "3年", "3年", "3年", "3年",
        "3年", "3年", "2年", "2年", "1年", "2年", "2年", "2年", "2年", "2年",
        "2年", "2年", "2年", "2年", "2年", "2年", "2年"
    ],
    "設定部費（円）": [
        41000, 41000, 41000, 40000, 41000, 41000, 30000, 30000, 41000, 41000,
        41000, 41000, 41000, 41000, 20000, 41000, 41000, 41000, 35000, 41000,
        23000, 41000, 29000, 41000, 41000, 41000, 41000, 41000, 41000, 41000,
        41000, 29000, 41000, 40000, 41000, 41000, 41000
    ],
    "現在の支払額（円）": [
        29000, 29000, 29000, 28000, 29000, 30000, 18000, 18000, 29000, 29000,
        32000, 29000, 41000, 22000, 17000, 17000, 17000, 23000, 12000, 17000,
        0, 17000, 0, 6000, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0
    ],
    "残りの額（円）": [
        12000, 12000, 12000, 12000, 12000, 11000, 12000, 12000, 12000, 12000,
        9000, 12000, 0, 19000, 3000, 24000, 24000, 18000, 23000, 24000,
        23000, 24000, 29000, 35000, 41000, 41000, 41000, 41000, 41000, 41000,
        41000, 29000, 41000, 40000, 41000, 41000, 41000
    ],
    "支払状態": [
        "一部未納", "一部未納", "一部未納", "一部未納", "一部未納", "一部未納", "一部未納", "一部未納", "一部未納", "一部未納",
        "一部未納", "一部未納", "完納", "一部未納", "一部未納", "一部未納", "一部未納", "一部未納", "一部未納", "一部未納",
        "未納", "一部未納", "未納", "一部未納", "未納", "未納", "未納", "未納", "未納", "未納",
        "未納", "未納", "未納", "未納", "未納", "未納", "未納"
    ],
    "最終入金日": [
        "2026-06-05", "2026-06-05", "2026-06-05", "2026-06-05", "2026-06-05",
        "2026-06-05", "2026-06-05", "2026-06-05", "2026-06-05", "2026-06-05",
        "2026-06-05", "2026-06-05", "2026-06-05", "2026-06-05", "2026-06-05",
        "2026-06-05", "2026-06-05", "2026-06-05", "2026-06-05", "2026-06-05",
        "-", "2026-06-05", "-", "2026-06-05", "-",
        "-", "-", "-", "-", "-",
        "-", "-", "-", "-", "-",
        "-", "-"
    ]
}

if "member_data" not in st.session_state:
    # 💡 前回の古い24人データのCSVが残っている場合は、今回の新しい36人データで上書きする判定
    if os.path.exists(CSV_FILE):
        temp_df = pd.read_csv(CSV_FILE)
        if len(temp_df) != len(actual_data["部員名"]):
            # 人数が違う（古いデータ）場合は新しいデータで上書き
            st.session_state.member_data = pd.DataFrame(actual_data)
            save_data_to_csv()
        else:
            st.session_state.member_data = temp_df
    else:
        st.session_state.member_data = pd.DataFrame(actual_data)
        save_data_to_csv()

df = st.session_state.member_data

# 3. リアルタイムアラート（財務ダッシュボード）
st.subheader("📊 財務ダッシュボード")

total_collected = df["現在の支払額（円）"].sum()
total_unpaid = df["残りの額（円）"].sum()
total_expected = df["設定部費（円）"].sum()
achievement_rate = (total_collected / total_expected) * 100 if total_expected > 0 else 0

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="現在の部費総残高 (集計額)", value=f"{total_collected:,} 円")
with col2:
    st.metric(label="未納部費の総額 (残り必要な額)", value=f"{total_unpaid:,} 円", delta=f"目標総額: {total_expected:,} 円", delta_color="inverse")
with col3:
    st.metric(label="部費集金 達成率", value=f"{achievement_rate:.1f} %")

st.markdown("---")

# 4. メインレイアウト（左側にコントロール、右側に一覧表）
col_left, col_right = st.columns([1, 2])

with col_right:
    st.subheader("📋 部員名簿と部費納入状況")
    st.dataframe(df, use_container_width=True, height=600) # 💡 36名が見やすいようにさらに縦幅を広げました

with col_left:
    st.subheader("⚙️ 操作メニュー")
    
    operation_mode = st.radio(
        "行う操作を選択してください",
        options=["💰 部費の支払記録", "✏️ 部員情報の修正", "🆕 新入部員の登録"],
        horizontal=False
    )
    
    st.markdown("---")
    
    # ------------------ 【モード1：部費の支払記録】 ------------------
    if operation_mode == "💰 部費の支払記録":
        st.write("### 📝 支払データの更新")
        
        selected_name = st.selectbox(
            "部員を選択してください",
            options=df["部員名"].tolist()
        )
        
        selected_index = df[df["部員名"] == selected_name].index[0]
        selected_member = df.iloc[selected_index]
        
        target_fees = int(selected_member["設定部費（円）"])
        
        st.info(f"現在の状況: **{selected_member['支払状態']}**\n- 設定部費(全額): {target_fees:,}円\n- 支払済: {selected_member['現在の支払額（円）']:,}円\n- 残り額: {selected_member['残りの額（円）']:,}円")
        
        with st.form("pay_form", clear_on_submit=False):
            st.write("**💵 納入額の変更**")
            
            new_paid_amount = st.number_input(
                "現在の累計支払額（円）", 
                min_value=0, 
                max_value=100000, 
                step=1000,
                value=int(selected_member["現在の支払額（円）"]),
                help="この部員がこれまでに支払った総額を入力してください。"
            )
            
            submit_button = st.form_submit_button("💾 支払額を確定する")
            
            if submit_button:
                new_unpaid = target_fees - new_paid_amount
                
                if new_paid_amount >= target_fees:
                    new_status = "完納"
                    new_unpaid = max(0, new_unpaid)
                elif new_paid_amount > 0:
                    new_status = "一部未納"
                else:
                    new_status = "未納"
                
                today_str = datetime.date.today().strftime("%Y-%m-%d")
                
                st.session_state.member_data.at[selected_index, "現在の支払額（円）"] = new_paid_amount
                st.session_state.member_data.at[selected_index, "残りの額（円）"] = new_unpaid
                st.session_state.member_data.at[selected_index, "支払状態"] = new_status
                st.session_state.member_data.at[selected_index, "最終入金日"] = today_str
                
                save_data_to_csv()
                
                st.success(f"🎉 {selected_name} さんの支払額を {new_paid_amount:,} 円（状態：{new_status}）に更新しました！")
                st.rerun()

    # ------------------ 【モード2：部員情報の修正】 ------------------
    elif operation_mode == "✏️ 部員情報の修正":
        st.write("### ✏️ 登録情報の修正 / ❌ 部員の削除")
        st.info("💡 部員の名前・学年のほか、入部時期に応じた「設定部費（全額）」もここで変更できます。")
        
        selected_name = st.selectbox(
            "対象の部員を選択",
            options=df["部員名"].tolist(),
            key="edit_member_select"
        )
        
        selected_index = df[df["部員名"] == selected_name].index[0]
        selected_member = df.iloc[selected_index]
        
        with st.form("edit_member_form", clear_on_submit=False):
            st.write("**🔄 登録情報の修正**")
            new_name = st.text_input("部員名（修正後）", value=selected_member["部員名"])
            new_grade = st.selectbox(
                "学年（修正後）", 
                options=["1年", "2年", "3年", "4年"], 
                index=["1年", "2年", "3年", "4年"].index(selected_member["学年"])
            )
            new_target_fee = st.number_input(
                "この部員の設定部費（全額）", 
                min_value=0, 
                max_value=100000, 
                step=1000,
                value=int(selected_member["設定部費（円）"])
            )
            
            save_button = st.form_submit_button("💾 部員情報を上書き保存")
            
            if save_button:
                if not new_name:
                    st.error("❌ 名前を空欄にすることはできません！")
                elif new_name != selected_name and new_name in df["部員名"].values:
                    st.error(f"❌ 「{new_name}」さんは既に別の部員として登録されています。")
                else:
                    current_paid = int(selected_member["現在の支払額（円）"])
                    new_unpaid = new_target_fee - current_paid
                    
                    if current_paid >= new_target_fee:
                        new_status = "完納"
                        new_unpaid = max(0, new_unpaid)
                    elif current_paid > 0:
                        new_status = "一部未納"
                    else:
                        new_status = "未納"
                        
                    st.session_state.member_data.at[selected_index, "部員名"] = new_name
                    st.session_state.member_data.at[selected_index, "学年"] = new_grade
                    st.session_state.member_data.at[selected_index, "設定部費（円）"] = new_target_fee
                    st.session_state.member_data.at[selected_index, "残りの額（円）"] = new_unpaid
                    st.session_state.member_data.at[selected_index, "支払状態"] = new_status
                    
                    save_data_to_csv()
                    
                    st.success(f"✏️ {new_name} さんの情報を更新しました！（設定部費: {new_target_fee:,}円）")
                    st.rerun()
        
        st.markdown("---")
        
        with st.form("delete_member_form", clear_on_submit=False):
            st.write("**🚨 部員の削除（名簿から除外）**")
            st.warning(f"「{selected_name}」さんに関する全てのデータ（支払履歴など）が消去されます。")
            
            confirm_delete = st.checkbox("本当にこの部員を削除しますか？", value=False)
            delete_button = st.form_submit_button("🗑️ この部員を削除する")
            
            if delete_button:
                if not confirm_delete:
                    st.error("❌ 削除するには「本当にこの部員を削除しますか？」にチェックを入れてください。")
                else:
                    st.session_state.member_data = df.drop(selected_index).reset_index(drop=True)
                    save_data_to_csv()
                    
                    st.success(f"🗑️ {selected_name} さんのデータを削除しました。")
                    st.rerun()

    # ------------------ 【モード3：新入部員の登録】 ------------------
    else:
        st.write("### 🆕 新入部員の登録")
        st.info("💡 入部時期に応じた初期設定部費を入力して登録してください。")
        
        with st.form("add_member_form", clear_on_submit=True):
            add_name = st.text_input("部員名（氏名）")
            add_grade = st.selectbox("学年", options=["1年", "2年", "3年", "4年"])
            add_target_fee = st.number_input("この部員の設定部費（全額）", min_value=0, max_value=100000, step=1000, value=41000)
            
            add_button = st.form_submit_button("➕ 部員を登録")
            
            if add_button:
                if not add_name:
                    st.error("❌ 名前を入力してください！")
                elif add_name in df["部員名"].values:
                    st.error(f"❌ 「{add_name}」さんは既に登録されています。")
                else:
                    new_member = pd.DataFrame([{
                        "部員名": add_name,
                        "学年": add_grade,
                        "設定部費（円）": add_target_fee,
                        "現在の支払額（円）": 0,
                        "残りの額（円）": add_target_fee,
                        "支払状態": "未納",
                        "最終入金日": "-"
                    }])
                    st.session_state.member_data = pd.concat([df, new_member], ignore_index=True)
                    save_data_to_csv()
                    
                    st.success(f"🎉 {add_name} さん（設定部費: {add_target_fee:,}円）を新しく登録しました！")
                    st.rerun()

st.markdown("---")
st.caption("森山ゼミ（応用情報学研究室）| 組織アセットマネジメント・シミュレーター（部費管理版）")