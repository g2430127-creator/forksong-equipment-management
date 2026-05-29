import pandas as pd
import streamlit as st

# 1. ページの設定
st.set_page_config(page_title="フォークソング研究部機材管理表", page_icon="🎸", layout="wide")

st.title("🎸 フォークソング研究部 機材管理表")
st.markdown("---")

# 2. データの初期化（セッション状態の維持）
if "equipment_data" not in st.session_state:
    data = {
        "機材ID": [
            "A001", "A002", "A003", "A004", "D001", 
            "D002", "DR01", "M001", "M002", "M003", 
            "M004", "M005", "W001", "W002", "W003", 
            "W004", "W005", "W006", "W00A"
        ],
        "機材名": [
            "JC-120(古) ギターアンプ", "JC-120 ギターアンプ", "ベース ヘッドアンプ", "ベース アンプ", "アコギDI",
            "キーボードDI", "Pearl スネア ドラム", "SHURE SM58 (マイク1)", "SHURE SM58 (マイク2)", "SHURE SM58 (マイク3)",
            "SHURE SM58 (マイク4)", "SHURE SM58 (マイク5)", "マイク線(1)", "マイク線(2)", "マイク線(3)",
            "マイク線(4)", "マイク線(5)", "マイク線(6)", "マイク線(A)"
        ],
        "現在の状態": [
            "良好", "要メンテナンス", "良好", "良好", "良好",
            "良好", "良好", "故障中", "良好", "良好",
            "良好", "良好", "良好", "故障中", "良好",
            "良好", "要メンテナンス", "良好", "良好"
        ],
        "前回メンテ日": [
            "2026-01-15", "2025-08-10", "2026-03-01", "2026-04-12", "2026-02-20",
            "2026-02-22", "2026-03-01", "2025-12-20", "2026-04-10", "2026-04-11",
            "2026-04-11", "2026-04-15", "2026-05-01", "2025-11-05", "2026-05-01",
            "2026-05-02", "2025-09-18", "2026-05-05", "2026-05-06"
        ],
    }
    st.session_state.equipment_data = pd.DataFrame(data)

df = st.session_state.equipment_data

# 3. リアルタイムアラート
st.subheader("🚨 重要アラート・ダッシュボード")

broken_items = df[df["現在の状態"] == "故障中"]["機材名"].tolist()
check_items = df[df["現在の状態"] == "要メンテナンス"]["機材名"].tolist()

num_broken = len(broken_items)
num_check = len(check_items)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="総管理機材数", value=f"{len(df)} 点")

with col2:
    if num_broken > 0:
        items_list = "\n".join([f"- {item}" for item in broken_items])
        st.error(f"❌ **故障中の機材: {num_broken} 件**\n\n{items_list}")
    else:
        st.success("❌ 故障中の機材: なし")

with col3:
    if num_check > 0:
        items_list = "\n".join([f"- {item}" for item in check_items])
        st.warning(f"⚠️ **メンテナンス推奨: {num_check} 件**\n\n{items_list}")
    else:
        st.success("⚠️ メンテナンス推奨: なし")

st.markdown("---")

# 4. メインレイアウト（左側にコントロールパネル、右側に一覧表）
col_left, col_right = st.columns([1, 2])

with col_right:
    st.subheader("📋 機材一覧データ")
    st.dataframe(df, use_container_width=True, height=500)

with col_left:
    st.subheader("⚙️ 操作メニュー")
    
    # 💡 「編集」か「新規追加」かを選べる切り替えスイッチを設置！
    operation_mode = st.radio(
        "行う操作を選択してください",
        options=["既存機材の編集", "🆕 新しい機材の追加"],
        horizontal=True
    )
    
    st.markdown("---")
    
    # ------------------ 【モード1：既存機材の編集】 ------------------
    if operation_mode == "既存機材の編集":
        st.write("### 📝 機材のステータス編集")
        st.info("💡 編集したい機材をリストから選んでください。")
        
        selected_id = st.selectbox(
            "編集する機材IDを選択",
            options=df["機材ID"].tolist(),
            format_func=lambda x: f"{x} : {df[df['機材ID']==x]['機材名'].values[0]}"
        )
        
        selected_index = df[df["機材ID"] == selected_id].index[0]
        selected_item = df.iloc[selected_index]
        
        with st.form("edit_form", clear_on_submit=False):
            new_status = st.selectbox(
                "現在の状態",
                options=["良好", "要メンテナンス", "故障中"],
                index=["良好", "要メンテナンス", "故障中"].index(selected_item["現在の状態"])
            )
            
            st.write("📅 **前回メンテ日**")
            curr_year, curr_month, curr_day = selected_item["前回メンテ日"].split("-")
            
            date_col1, date_col2, date_col3 = st.columns(3)
            with date_col1:
                year_list = [str(y) for y in range(2024, 2028)]
                selected_year = st.selectbox("年", options=year_list, index=year_list.index(curr_year), key="edit_y")
            with date_col2:
                month_list = [f"{m:02d}" for m in range(1, 13)]
                selected_month = st.selectbox("月", options=month_list, index=month_list.index(curr_month), key="edit_m")
            with date_col3:
                day_list = [f"{d:02d}" for d in range(1, 32)]
                selected_day = st.selectbox("日", options=day_list, index=day_list.index(curr_day), key="edit_d")
                
            submit_button = st.form_submit_button("💾 この機材の変更を保存")
            
            if submit_button:
                new_date_str = f"{selected_year}-{selected_month}-{selected_day}"
                st.session_state.equipment_data.at[selected_index, "現在の状態"] = new_status
                st.session_state.equipment_data.at[selected_index, "前回メンテ日"] = new_date_str
                st.success("変更を保存しました！")
                st.rerun()

    # ------------------ 【モード2：新しい機材の追加】 ------------------
    else:
        st.write("### 🆕 新規機材の登録")
        st.info("💡 新しく管理する機材の情報を入力してください。")
        
        with st.form("add_form", clear_on_submit=True):
            # 新しい機材データの入力欄
            add_id = st.text_input("機材ID（例：A005, M006）")
            add_name = st.text_input("機材名（例：YAMAHA ギターアンプ）")
            
            add_status = st.selectbox(
                "初期の状態",
                options=["良好", "要メンテナンス", "故障中"]
            )
            
            st.write("📅 **登録時のメンテ日・購入日**")
            date_col1, date_col2, date_col3 = st.columns(3)
            with date_col1:
                year_list = [str(y) for y in range(2024, 2028)]
                add_year = st.selectbox("年", options=year_list, index=2, key="add_y") # デフォルト2026年
            with date_col2:
                month_list = [f"{m:02d}" for m in range(1, 13)]
                add_month = st.selectbox("月", options=month_list, index=4, key="add_m") # デフォルト05月
            with date_col3:
                day_list = [f"{d:02d}" for d in range(1, 32)]
                add_day = st.selectbox("日", options=day_list, index=21, key="add_d") # デフォルト22日
            
            add_button = st.form_submit_button("➕ 新しい機材を登録")
            
            if add_button:
                # 簡単な入力チェック
                if not add_id or not add_name:
                    st.error("❌ 機材IDと機材名は必ず入力してください！")
                elif add_id in df["機材ID"].values:
                    st.error(f"❌ 機材ID「{add_id}」は既に使われています！別のIDにしてください。")
                else:
                    # 日付を結合
                    add_date_str = f"{add_year}-{add_month}-{add_day}"
                    
                    # 新しい行（データ）を作成
                    new_row = pd.DataFrame([{
                        "機材ID": add_id,
                        "機材名": add_name,
                        "現在の状態": add_status,
                        "前回メンテ日": add_date_str
                    }])
                    
                    # 既存のデータフレームに結合してセッションを更新
                    st.session_state.equipment_data = pd.concat([df, new_row], ignore_index=True)
                    st.success(f"🎉 {add_name} を新しく登録しました！")
                    st.rerun()

st.markdown("---")
st.caption("森山ゼミ（応用情報学研究室）| 組織アセットマネジメント・シミュレーター")