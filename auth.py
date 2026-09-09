# -*- coding: utf-8 -*-
"""
Phân hệ Xác thực: Đăng nhập & Đăng ký tài khoản YouthMind
Tối giản thông tin đăng ký (Username, Password, Nhập lại password)
Giao diện hồng pastel, chữ đen, Times New Roman
"""

import streamlit as st
import database as db

def render_auth_page():
    """Hiển thị trang Đăng ký / Đăng nhập YouthMind"""
    st.markdown("""
    <div style="text-align: center; margin-top: 15px; margin-bottom: 25px; padding: 0 10px;">
        <h1 style="color: #ff3366; font-size: 38px; margin-bottom: 12px; font-weight: bold; letter-spacing: 0.5px;">
            🌸 YouthMind 🌸
        </h1>
        <div style="max-width: 820px; margin: 0 auto; background: #ffffff; border: 1.5px solid #ffd1dc; border-radius: 20px; padding: 22px 28px; box-shadow: 0 6px 20px rgba(255, 105, 180, 0.1);">
            <p style="font-size: 16.5px; color: #111827; line-height: 1.8; margin-bottom: 12px; text-align: justify;">
                <b>YouthMind</b> – nơi dành cho những người trẻ đang trên hành trình hiểu mình và lớn lên từng ngày. 
                <i>“Youth”</i> mang ý nghĩa tuổi trẻ, còn <i>“Mind”</i> đại diện cho tâm trí, suy nghĩ và cảm xúc. 
                YouthMind được tạo ra như một người bạn đồng hành, giúp bạn lắng nghe bản thân, nhận diện những áp lực đang gặp phải và tìm kiếm những cách tích cực hơn để đối diện với chúng. 🌱
            </p>
            <p style="font-size: 16.5px; color: #d97706; font-weight: bold; margin: 0; text-align: center;">
                Bạn không cần phải lớn lên thật nhanh. Hãy để chúng mình lớn cùng nhau. 💛
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2.2, 1])

    with col2:
        # Sử dụng st.tabs chuẩn để không bị lỗi ô trắng rỗng (Ảnh 1)
        tab_login, tab_register = st.tabs(["🔑 Đăng Nhập", "📝 Đăng Ký Tài Khoản"])

        with tab_login:
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            st.markdown("<h2 style='text-align: center; color: #ff4757; font-size: 24px; margin-top: 5px;'>Đăng Nhập Tài Khoản</h2>", unsafe_allow_html=True)
            
            username = st.text_input("Username (Tên đăng nhập):", placeholder="Nhập tên tài khoản của bạn...", key="login_uname")
            password = st.text_input("Password (Mật khẩu):", type="password", placeholder="Nhập mật khẩu...", key="login_pwd")
            
            st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
            
            if st.button("ĐĂNG NHẬP NGAY", use_container_width=True, key="btn_submit_login"):
                if not username or not password:
                    st.error("Vui lòng điền đầy đủ Tên đăng nhập và Mật khẩu!")
                else:
                    user, msg = db.authenticate_user(username, password)
                    if user:
                        st.session_state["user"] = user
                        st.session_state["page"] = "🏠 Trang chủ"
                        st.success(f"{msg} Chào mừng bạn quay trở lại! 🔥 Chuỗi {user['streak_count']} ngày đăng nhập liên tiếp!")
                        st.rerun()
                    else:
                        st.error(msg)

        with tab_register:
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            st.markdown("<h2 style='text-align: center; color: #ff4757; font-size: 24px; margin-top: 5px;'>Đăng Ký Thành Viên Mới</h2>", unsafe_allow_html=True)
            
            new_username = st.text_input("Username (Tên đăng nhập):", placeholder="Ví dụ: youth_friend", key="reg_uname")
            new_password = st.text_input("Password (Mật khẩu):", type="password", placeholder="Tối thiểu 6 ký tự...", key="reg_pwd")
            confirm_pwd = st.text_input("Nhập lại mật khẩu:", type="password", placeholder="Nhập lại mật khẩu vừa đặt...", key="reg_pwd2")

            st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

            if st.button("HOÀN TẤT ĐĂNG KÝ", use_container_width=True, key="btn_submit_reg"):
                if not new_username or not new_password or not confirm_pwd:
                    st.error("Vui lòng điền đầy đủ Tên đăng nhập, Mật khẩu và Nhập lại mật khẩu!")
                elif new_password != confirm_pwd:
                    st.error("Mật khẩu nhập lại không khớp. Vui lòng kiểm tra lại!")
                elif len(new_password) < 6:
                    st.error("Mật khẩu phải có độ dài tối thiểu từ 6 ký tự để đảm bảo an toàn!")
                else:
                    success, msg = db.register_user(new_username, new_password)
                    if success:
                        st.success(f"🎉 {msg} Vui lòng chuyển sang tab '🔑 Đăng Nhập' để bắt đầu trải nghiệm cùng YouthMind nhé!")
                    else:
                        st.error(msg)
