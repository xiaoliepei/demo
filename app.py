import streamlit as st
import os
import pandas as pd

DATA_FILE = "contacts.txt"


def load_contacts():
    """从 txt 文件读取联系人"""
    if not os.path.exists(DATA_FILE):
        return []
    contacts = []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split("|", 2)
                if len(parts) == 3:
                    contacts.append(parts)
    return contacts


def save_contacts(contacts):
    """保存联系人到 txt 文件"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        for c in contacts:
            f.write(f"{c[0]}|{c[1]}|{c[2]}\n")


# 页面配置
st.set_page_config(page_title="通讯录管理平台", page_icon="📒", layout="wide")
st.title("📒 通讯录管理平台")
st.caption("基于 Streamlit 的在线通讯录，支持添加、删除、查看与搜索")

# 加载数据
contacts = load_contacts()

# ========== 左侧：添加联系人 ==========
with st.sidebar:
    st.header("➕ 添加联系人")
    with st.form("add_form", clear_on_submit=True):
        name = st.text_input("姓名 *", placeholder="请输入姓名")
        phone = st.text_input("电话 *", placeholder="请输入电话")
        addr = st.text_input("地址", placeholder="请输入地址（可选）")
        submitted = st.form_submit_button("添加", use_container_width=True)

        if submitted:
            if not name or not phone:
                st.error("❌ 姓名和电话不能为空！")
            elif any(c[0] == name and c[1] == phone for c in contacts):
                st.error("❌ 该联系人已存在！")
            else:
                contacts.append([name, phone, addr])
                save_contacts(contacts)
                st.success("✅ 添加成功！")
                st.rerun()

    st.divider()
    st.info("💡 数据默认保存在 `contacts.txt` 中")

# ========== 右侧：搜索 + 列表 ==========
search_col, btn_col = st.columns([4, 1])
with search_col:
    keyword = st.text_input("🔍 搜索姓名", placeholder="输入关键词搜索...")
with btn_col:
    st.write("")
    st.write("")
    if st.button("🔄 刷新", use_container_width=True):
        st.rerun()

# 过滤
if keyword.strip():
    filtered = [c for c in contacts if keyword.strip() in c[0]]
else:
    filtered = contacts

if not filtered:
    st.info("📭 暂无联系人数据。")
else:
    st.subheader(f"📋 联系人列表（共 {len(filtered)} 条）")
    df = pd.DataFrame(filtered, columns=["姓名", "电话", "地址"])
    st.dataframe(df, use_container_width=True, hide_index=True)

# ========== 删除联系人 ==========
if contacts:
    st.divider()
    st.subheader("🗑️ 删除联系人")
    del_options = [f"{c[0]}  |  {c[1]}  |  {c[2]}" for c in contacts]
    selected = st.selectbox("选择要删除的联系人", del_options)

    if st.button("删除选中", type="primary"):
        parts = selected.split("  |  ", 2)
        contacts = [
            c for c in contacts
            if not (c[0] == parts[0] and c[1] == parts[1] and c[2] == parts[2])
        ]
        save_contacts(contacts)
        st.success("✅ 删除成功！")
        st.rerun()
