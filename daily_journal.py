# -*- coding: utf-8 -*-
"""
Phân hệ Sổ Theo Dõi Hằng Ngày (Nhật Kí Daily)
- Sử dụng st.selectbox cho màu chữ & màu nền chủ đạo
- Sử dụng st.checkbox cho các hiệu ứng: In đậm (Bold), Chữ nghiêng (Italic), Gạch chân (Underline), Highlight
- Ô nhập nội dung text_area nhiều dòng (Long Paragraph)
- Bản xem trước trực tiếp theo đúng phong cách tùy chọn của người dùng
"""

import streamlit as st
import database as db
from config import JOURNAL_TEXT_COLORS, JOURNAL_BG_THEMES
from datetime import date

def render_daily_journal_page(user):
    """Hiển thị giao diện Sổ theo dõi hằng ngày"""
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h1 style="color: #ff3366; font-size: 32px; margin-bottom: 6px;">📖 SỔ THEO DÕI HẰNG NGÀY (NHẬT KÍ DAILY)</h1>
        <p style="font-size: 16px; color: #111827; line-height: 1.6;">
            Không gian an toàn để bạn trút bỏ mọi áp lực, bộc bạch suy nghĩ thầm kín và theo dõi tiến trình cảm xúc mỗi ngày.
        </p>
    </div>
    """, unsafe_allow_html=True)

    journal_tab1, journal_tab2 = st.tabs([
        "✍️ Viết Trang Nhật Ký Mới",
        "📚 Kho Lưu Trữ Nhật Ký Của Bạn"
    ])

    with journal_tab1:
        render_new_journal_editor(user)

    with journal_tab2:
        render_journal_archive(user)

def render_new_journal_editor(user):
    st.markdown("""
    <div class="custom-card" style="border-left: 5px solid #ff4757; margin-bottom: 20px;">
        <h2 style="color: #ff4757; font-size: 22px; margin-top: 0;">✨ Viết & Trang Trí Nhật Ký Cá Nhân</h2>
        <p style="font-size: 15px; color: #374151; margin-bottom: 0;">
            Sử dụng bộ công cụ định dạng trực quan bên dưới để trang trí trang viết theo đúng cảm xúc của bạn hôm nay.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 1. Tiêu đề và ngày tháng
    col_d1, col_d2 = st.columns([2, 1])
    with col_d1:
        journal_title = st.text_input("Tiêu đề trang nhật ký:", placeholder="Ví dụ: Một ngày vượt qua áp lực bài kiểm tra...", key="j_title")
    with col_d2:
        journal_date = st.date_input("Ngày ghi nhật ký:", value=date.today(), key="j_date")

    # 2. BỘ CÔNG CỤ ĐỊNH DẠNG: st.selectbox & st.checkbox
    st.markdown("""
    <div style="background: #ffffff; padding: 18px; border-radius: 16px; border: 1.5px solid #ffd1dc; margin: 15px 0; box-shadow: 0 4px 12px rgba(255, 105, 180, 0.08);">
        <h4 style="color: #be123c; margin: 0 0 12px 0; font-size: 18px; font-weight: bold;">🎨 Bộ Công Cụ Định Dạng Văn Bản & Sắc Màu:</h4>
    </div>
    """, unsafe_allow_html=True)

    col_tools1, col_tools2 = st.columns(2)
    
    with col_tools1:
        # 1. Các tùy chọn màu sắc từ người dùng bằng st.selectbox
        mau_chu = st.selectbox("Chọn màu chữ:", list(JOURNAL_TEXT_COLORS.keys()), index=0, key="j_txt_color")
        mau_nen = st.selectbox("Chọn nền chủ đạo:", list(JOURNAL_BG_THEMES.keys()), index=0, key="j_bg_color")

    with col_tools2:
        st.markdown("<p style='font-size: 15px; font-weight: bold; margin-bottom: 8px; color: #111827;'>✨ Hiệu ứng định dạng chữ:</p>", unsafe_allow_html=True)
        col_cb1, col_cb2 = st.columns(2)
        with col_cb1:
            bold = st.checkbox("In đậm (Bold)", value=False, key="j_bold")
            italic = st.checkbox("Chữ nghiêng (Italic)", value=False, key="j_italic")
        with col_cb2:
            underline = st.checkbox("Gạch chân (Underline)", value=False, key="j_underline")
            highlight = st.checkbox("Đánh dấu nổi bật (Highlight)", value=False, key="j_highlight")

    # 3. Ô NHẬP NỘI DUNG NHẬT KÝ
    noi_dung = st.text_area(
        "Nhập nội dung nhật ký (Cho phép viết đoạn văn dài và xuống dòng thoải mái):",
        placeholder="Hôm nay bạn cảm thấy thế nào? Áp lực học tập hay bạn bè có khiến bạn băn khoăn điều gì không? Hãy tự do viết ra mọi suy nghĩ của bạn...",
        height=220,
        key="j_content"
    )

    # 4. XỬ LÝ LOGIC CSS VÀ HIỂN THỊ BẢN XEM TRƯỚC
    hex_chu = JOURNAL_TEXT_COLORS[mau_chu]
    bg_data = JOURNAL_BG_THEMES[mau_nen]
    hex_nen = bg_data["bg"]
    hex_vien = bg_data["border"]

    styles = f"color: {hex_chu}; background-color: {hex_nen}; border: 1.5px solid {hex_vien}; padding: 22px; border-radius: 16px; font-family: 'Times New Roman', Times, serif; font-size: 16.5px; line-height: 1.8; margin-bottom: 20px; box-shadow: 0 6px 18px rgba(0,0,0,0.05);"
    if bold:
        styles += " font-weight: bold;"
    if italic:
        styles += " font-style: italic;"
    if underline:
        styles += " text-decoration: underline;"

    st.markdown("<h3 style='color: #ff3366; margin-top: 25px;'>👁️ Bản Xem Trước Trang Nhật Ký:</h3>", unsafe_allow_html=True)
    
    # Render bản xem trước trực tiếp
    display_title = journal_title.strip() if journal_title else "Tiêu Đề Trang Nhật Ký"
    paragraphs = noi_dung.split("\n") if noi_dung else ["(Nội dung bạn viết sẽ hiển thị trực tiếp ở đây theo đúng màu sắc và hiệu ứng bạn đã chọn...)"]
    
    content_html = ""
    for p in paragraphs:
        if p.strip():
            if highlight:
                content_html += f'<p style="margin: 0 0 10px 0;"><span style="background-color: #fef08a; color: #111827; padding: 2px 6px; border-radius: 4px;">{p}</span></p>'
            else:
                content_html += f'<p style="margin: 0 0 10px 0;">{p}</p>'
        else:
            content_html += '<div style="height: 10px;"></div>'

    preview_box = (
        f'<div style="{styles}">\n'
        f'<div style="display: flex; justify-content: space-between; border-bottom: 1.5px solid {hex_vien}; padding-bottom: 10px; margin-bottom: 14px;">\n'
        f'<h3 style="color: {hex_chu}; margin: 0; font-size: 22px; font-family: \'Times New Roman\', Times, serif;">{display_title}</h3>\n'
        f'<span style="color: {hex_chu}; opacity: 0.85; font-size: 14.5px;">📅 {journal_date}</span>\n'
        f'</div>\n'
        f'<div>\n'
        f'{content_html}\n'
        f'</div>\n'
        f'</div>'
    )
    st.markdown(preview_box, unsafe_allow_html=True)

    # 5. NÚT LƯU TRANG NHẬT KÝ
    if st.button("💾 LƯU TRANG NHẬT KÝ VÀO SỔ THEO DÕI", use_container_width=True):
        if not journal_title or not noi_dung:
            st.error("Vui lòng nhập đầy đủ Tiêu đề và Nội dung nhật ký trước khi lưu!")
        else:
            db.save_daily_journal(
                user_id=user["id"],
                journal_date=str(journal_date),
                title=journal_title,
                raw_content=noi_dung,
                text_color=mau_chu,
                bg_color=mau_nen,
                is_bold=bold,
                is_italic=italic,
                is_underline=underline,
                is_highlight=highlight
            )
            st.success("🎉 Đã lưu trang nhật ký thành công vào Sổ theo dõi của bạn!")
            st.rerun()

def render_journal_archive(user):
    st.markdown("""
    <div class="custom-card" style="border-left: 5px solid #2563eb;">
        <h2 style="color: #2563eb; font-size: 22px; margin-top: 0;">📚 Kho Lưu Trữ Nhật Ký Của Bạn</h2>
        <p style="font-size: 15px; color: #374151;">
            Đọc lại những dòng nhật ký cũ để thấy tâm trí mình đã vững vàng và trưởng thành hơn qua từng ngày.
        </p>
    </div>
    """, unsafe_allow_html=True)

    journals = db.get_user_journals(user["id"])

    if not journals:
        st.info("Bạn chưa lưu trang nhật ký nào. Hãy sang tab 'Viết Trang Nhật Ký Mới' để bắt đầu ghi chép nhé!")
        return

    # Tìm kiếm nhật ký theo từ khóa
    kw = st.text_input("🔍 Tìm kiếm nhật ký theo từ khóa:", placeholder="Nhập từ khóa cần tìm trong tiêu đề hoặc nội dung...", key="j_search")
    if kw:
        journals = [j for j in journals if kw.lower() in j["title"].lower() or kw.lower() in j["raw_content"].lower()]

    st.markdown(f"<p style='color: #4b5563; font-size: 14px;'>Đang hiển thị <b>{len(journals)}</b> trang nhật ký:</p>", unsafe_allow_html=True)

    for j in journals:
        t_color = JOURNAL_TEXT_COLORS.get(j["text_color"], "#000000")
        bg_d = JOURNAL_BG_THEMES.get(j["bg_color"], {"bg": "#ffffff", "border": "#e2e8f0"})
        b_bg = bg_d["bg"]
        b_border = bg_d["border"]

        s_styles = f"color: {t_color}; background-color: {b_bg}; border: 1.5px solid {b_border}; padding: 18px; border-radius: 16px; margin-bottom: 16px;"
        if j.get("is_bold"): s_styles += " font-weight: bold;"
        if j.get("is_italic"): s_styles += " font-style: italic;"
        if j.get("is_underline"): s_styles += " text-decoration: underline;"

        with st.expander(f"📖 {j['title']} (📅 {j['journal_date']})", expanded=False):
            pars = j["raw_content"].split("\n")
            p_html = ""
            for p in pars:
                if p.strip():
                    if j.get("is_highlight"):
                        p_html += f'<p style="margin-bottom: 8px;"><span style="background-color: #fef08a; color: #111827; padding: 2px 5px; border-radius: 3px;">{p}</span></p>'
                    else:
                        p_html += f'<p style="margin-bottom: 8px;">{p}</p>'
                else:
                    p_html += '<div style="height: 8px;"></div>'

            archive_box = (
                f'<div style="{s_styles}">\n'
                f'<div style="border-bottom: 1px dashed {b_border}; padding-bottom: 6px; margin-bottom: 12px; font-size: 13.5px; opacity: 0.85;">\n'
                f'Ghi nhận lúc: {j["created_at"]}\n'
                f'</div>\n'
                f'<div>\n'
                f'{p_html}\n'
                f'</div>\n'
                f'</div>'
            )
            st.markdown(archive_box, unsafe_allow_html=True)
