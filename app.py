# -*- coding: utf-8 -*-
"""
YouthMind - Ứng Dụng Phân Tích Áp Lực Đồng Trang Lứa & Trợ Lý Học Đường
Giao diện: Hồng pastel, nền hồng pastel dịu ngọt, chữ đen, font Times New Roman chuẩn khoa học
"""

import streamlit as st
import os
import sys

# Đảm bảo đường dẫn import hoạt động ổn định
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

import config
import database as db
from modules.auth import render_auth_page
from modules.home import render_home_page
from modules.pressure_test import render_pressure_test_page
from modules.dashboard import render_dashboard_page
from modules.daily_journal import render_daily_journal_page
from modules.chatbot import render_chatbot_page
from modules.documents import render_documents_page

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="YouthMind - Ngôi Nhà Nhỏ Của Những Tâm Hồn Trẻ",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Khởi tạo cơ sở dữ liệu
db.init_db()

# Nạp stylesheet CSS chuẩn Times New Roman, nền hồng pastel & bảo vệ icon
st.markdown(config.APP_CUSTOM_CSS, unsafe_allow_html=True)

# Khởi tạo session state
if "user" not in st.session_state:
    st.session_state["user"] = None

if "page" not in st.session_state:
    st.session_state["page"] = "🏠 Trang chủ"

def render_top_navbar(user):
    """Hiển thị thanh điều hướng Top Navbar ở phần đầu trang (Đã xóa chữ 'Lớp')"""
    st.markdown(f"""
    <div class="top-navbar-container">
        <div style="display: flex; align-items: center; gap: 14px;">
            <span style="font-size: 36px;">🌸</span>
            <div>
                <span style="font-size: 24px; font-weight: bold; color: #ff3366; letter-spacing: 0.5px; display: block;">
                    YouthMind Assistant
                </span>
                <span style="font-size: 14.5px; color: #4b5563; display: block; margin-top: 2px;">
                    Ngôi Nhà Nhỏ Của Những Tâm Hồn Trẻ - Nơi Lắng Nghe Và Vỗ Về Mọi Áp Lực Học Trò
                </span>
            </div>
        </div>
        <div style="display: flex; align-items: center; gap: 16px; flex-wrap: wrap;">
            <div class="streak-badge">
                🔥 Chuỗi {user.get('streak_count', 1)} Ngày
            </div>
            <div style="text-align: right;">
                <b style="color: #111827; font-size: 16px;">{user['full_name']}</b>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Thanh điều hướng các trang ngang (Đã xóa hoàn toàn phần Diễn đàn & Nhắn tin)
    nav_pages = [
        "🏠 Trang chủ",
        "🧠 Pressure Test",
        "📊 Dashboard",
        "📖 Sổ theo dõi",
        "🤖 Chatbot AI",
        "📚 Kho tài liệu",
        "🚪 Đăng xuất"
    ]

    current_p = st.session_state.get("page", "🏠 Trang chủ")
    if current_p not in nav_pages or "Đăng xuất" in current_p:
        current_p = "🏠 Trang chủ"
        st.session_state["page"] = "🏠 Trang chủ"

    current_idx = nav_pages.index(current_p)

    selected_nav = st.radio(
        "Menu chức năng chính:",
        options=nav_pages,
        index=current_idx,
        horizontal=True,
        label_visibility="collapsed",
        key="main_top_nav"
    )

    if "Đăng xuất" in selected_nav:
        # Xóa toàn bộ dữ liệu phiên đăng nhập
        st.session_state["user"] = None
        st.session_state["page"] = "🏠 Trang chủ"
        for k in ["main_top_nav", "roleplay_answers", "roleplay_current_q", "roleplay_last_result", "chat_messages"]:
            if k in st.session_state:
                del st.session_state[k]
        st.rerun()
    elif selected_nav != st.session_state.get("page"):
        st.session_state["page"] = selected_nav
        st.rerun()

    st.markdown("<hr style='border: none; border-top: 1.5px solid #fecdd3; margin: 8px 0 22px 0;'>", unsafe_allow_html=True)

def main():
    user = st.session_state["user"]

    # Nếu chưa đăng nhập -> Hiển thị trang Auth
    if not user:
        render_auth_page()
        return

    # Luôn hiển thị thanh điều hướng Top Navbar ở phần đầu trang
    render_top_navbar(user)

    # Điều hướng đến trang tương ứng
    current_page = st.session_state["page"]

    if current_page == "🏠 Trang chủ":
        render_home_page(user)
    elif current_page == "🧠 Pressure Test":
        render_pressure_test_page(user)
    elif current_page == "📊 Dashboard":
        render_dashboard_page(user)
    elif current_page == "📖 Sổ theo dõi":
        render_daily_journal_page(user)
    elif current_page == "🤖 Chatbot AI":
        render_chatbot_page(user)
    elif current_page == "📚 Kho tài liệu":
        render_documents_page(user)
    else:
        render_home_page(user)

    # Chân trang (Footer) nhẹ nhàng
    st.markdown("""
    <div style="text-align: center; color: #9ca3af; font-size: 14px; margin-top: 45px; padding-top: 20px; border-top: 1px dashed #fbcfe8;">
        © 2026 YouthMind Assistant. Nơi Lắng Nghe & Đồng Hành Cùng Tuổi Trẻ. All Rights Reserved.
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
