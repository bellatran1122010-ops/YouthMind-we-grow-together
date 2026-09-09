# -*- coding: utf-8 -*-
"""
Phân hệ Diễn Đàn Xã Hội & Nhắn Tin Riêng
1. Mạng xã hội tâm sự: Đăng bài (ẩn danh / hiện tên), gắn thẻ hashtag, thả tim, bình luận
2. Nhắn tin riêng tư 1-1: Danh sách bạn bè, trò chuyện riêng tư, gửi ảnh/video đính kèm
"""

import streamlit as st
import database as db
from config import FORUM_TAGS
import os

MEDIA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads", "chat_media")
os.makedirs(MEDIA_DIR, exist_ok=True)

def render_social_forum_page(user):
    """Hiển thị giao diện Diễn đàn & Nhắn tin riêng"""
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h1 style="color: #ff3366; font-size: 32px; margin-bottom: 6px;">💬 DIỄN ĐÀN HỌC ĐƯỜNG & NHẮN TIN RIÊNG</h1>
        <p style="font-size: 16px; color: #4b5563;">
            Cộng đồng chia sẻ áp lực học đường an toàn, kết nối bạn bè cùng chí hướng và nhắn tin riêng tư 1-1.
        </p>
    </div>
    """, unsafe_allow_html=True)

    soc_tab1, soc_tab2 = st.tabs([
        "📢 1. Diễn Đàn Tâm Sự Học Đường",
        "💌 2. Nhắn Tin Riêng Tư (1-1 Direct Message)"
    ])

    with soc_tab1:
        render_forum_feed(user)

    with soc_tab2:
        render_private_chat(user)

# ==================== 1. DIỄN ĐÀN TÂM SỰ ====================

def render_forum_feed(user):
    st.markdown("""
    <div class="custom-card" style="border-left: 5px solid #ff4757;">
        <h2 style="color: #ff4757; font-size: 22px; margin-top: 0;">📢 Bảng Tin Tâm Sự Học Đường</h2>
        <p style="font-size: 15px; color: #4b5563; margin-bottom: 0;">
            Nơi bạn có thể tự do trải lòng về những áp lực điểm số, sự so sánh bạn bè hay băn khoăn tuổi học trò. Bạn có thể chọn <b>Đăng ẩn danh</b> để bảo mật tuyệt đối danh tính.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Form đăng bài tâm sự mới
    with st.expander("✍️ ĐĂNG BÀI TÂM SỰ / CHIA SẺ MỚI", expanded=False):
        f_title = st.text_input("Tiêu đề bài viết:", placeholder="Ví dụ: Áp lực khi bạn bè trong lớp ai cũng giỏi tiếng Anh...", key="post_title")
        
        col_f1, col_f2 = st.columns([1, 1])
        with col_f1:
            f_tag = st.selectbox("Chọn chủ đề hashtag:", [t for t in FORUM_TAGS if t != "Tất cả chủ đề"], key="post_tag")
        with col_f2:
            is_anon = st.checkbox("🕶️ Đăng bài ở chế độ ẨN DANH (Không hiện tên và lớp)", value=True, key="post_anon")

        f_content = st.text_area("Nội dung tâm sự hoặc câu hỏi của bạn:", placeholder="Hãy viết ra những suy nghĩ của bạn, chúng mình luôn lắng nghe và đồng cảm...", height=150, key="post_content")

        if st.button("ĐĂNG BÀI LÊN DIỄN ĐÀN", use_container_width=True):
            if not f_title or not f_content:
                st.error("Vui lòng nhập đầy đủ tiêu đề và nội dung bài viết!")
            else:
                author_display = "Ẩn danh (Học sinh giấu tên)" if is_anon else f"{user['full_name']} - Lớp {user.get('student_class', '')}"
                db.create_forum_post(
                    user_id=user["id"],
                    is_anonymous=is_anon,
                    author_name=author_display,
                    tag=f_tag,
                    title=f_title,
                    content=f_content
                )
                st.success("🎉 Bài viết của bạn đã được đăng thành công lên diễn đàn!")
                st.rerun()

    # Bộ lọc bài viết theo hashtag
    selected_filter_tag = st.selectbox("🏷️ Lọc bài viết theo chủ đề:", FORUM_TAGS, index=0, key="filter_forum_tag")
    posts = db.get_forum_posts(selected_filter_tag)

    st.markdown(f"<p style='font-weight: bold; color: #4b5563; margin-top: 15px;'>Có {len(posts)} bài viết trên bảng tin:</p>", unsafe_allow_html=True)

    if not posts:
        st.info("Chưa có bài viết nào trong chủ đề này. Hãy là người đầu tiên chia sẻ tâm sự nhé!")
        return

    for post in posts:
        with st.container():
            st.markdown(f"""
            <div class="custom-card" style="border: 1.5px solid #ffe4e6; margin-bottom: 16px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <div>
                        <b style="color: #be123c; font-size: 15px;">👤 {post['author_name']}</b>
                        <span style="color: #6b7280; font-size: 13px; margin-left: 10px;">📅 {post['created_at'][:16]}</span>
                    </div>
                    <span style="background: #fff0f3; color: #e11d48; padding: 3px 10px; border-radius: 12px; font-size: 13px; font-weight: bold; border: 1px solid #fecdd3;">
                        {post['tag']}
                    </span>
                </div>
                <h3 style="color: #111827; font-size: 20px; margin: 6px 0 10px 0;">{post['title']}</h3>
                <p style="font-size: 16px; line-height: 1.7; color: #374151; white-space: pre-wrap; margin-bottom: 14px;">{post['content']}</p>
            </div>
            """, unsafe_allow_html=True)

            # Khối tương tác: Like và Bình luận
            c_like, c_cmt_count = st.columns([1, 4])
            with c_like:
                if st.button(f"❤️ Thả tim ({post['likes_count']})", key=f"like_btn_{post['id']}"):
                    db.toggle_like_post(post["id"], user["id"])
                    st.rerun()

            # Khu vực bình luận
            comments = db.get_post_comments(post["id"])
            with st.expander(f"💬 Xem {len(comments)} bình luận & Gửi phản hồi", expanded=False):
                for cmt in comments:
                    st.markdown(f"""
                    <div style="background: #fdf2f8; padding: 8px 14px; border-radius: 12px; margin-bottom: 8px; font-size: 14.5px;">
                        <b style="color: #9d174d;">{cmt['author_name']}:</b> {cmt['content']}
                        <div style="font-size: 12px; color: #9ca3af; text-align: right;">{cmt['created_at'][:16]}</div>
                    </div>
                    """, unsafe_allow_html=True)

                # Form gửi bình luận
                with st.form(f"cmt_form_{post['id']}"):
                    col_cm1, col_cm2 = st.columns([3, 1])
                    with col_cm1:
                        cmt_text = st.text_input("Viết bình luận động viên hoặc chia sẻ:", key=f"cmt_input_{post['id']}")
                    with col_cm2:
                        cmt_anon = st.checkbox("Bình luận ẩn danh", value=True, key=f"cmt_anon_{post['id']}")
                    
                    if st.form_submit_button("GỬI BÌNH LUẬN", use_container_width=True):
                        if cmt_text:
                            cmt_author = "Học sinh ẩn danh" if cmt_anon else user["full_name"]
                            db.add_forum_comment(post["id"], user["id"], cmt_author, cmt_anon, cmt_text)
                            st.success("Đã gửi bình luận thành công!")
                            st.rerun()

# ==================== 2. NHẮN TIN RIÊNG 1-1 ====================

def render_private_chat(user):
    st.markdown("""
    <div class="custom-card" style="border-left: 5px solid #2563eb;">
        <h2 style="color: #2563eb; font-size: 22px; margin-top: 0;">💌 Hộp Thư Trò Chuyện Riêng Tư 1-1</h2>
        <p style="font-size: 15px; color: #4b5563; margin-bottom: 0;">
            Kết nối và trò chuyện bí mật cùng bạn bè trong trường hoặc hệ thống. Hỗ trợ gửi tin nhắn văn bản, hình ảnh và video đính kèm.
        </p>
    </div>
    """, unsafe_allow_html=True)

    other_users = db.get_all_users_except(user["id"])

    if not other_users:
        st.info("Hiện tại chưa có học sinh nào khác trên hệ thống. Hãy mời bạn cùng lớp đăng ký tài khoản để bắt đầu trò chuyện riêng tư nhé!")
        return

    # Danh sách chọn người nhận
    user_options = {u["id"]: f"{u['full_name']} (@{u['username']}) - {u.get('school', '')} Lớp {u.get('student_class', '')}" for u in other_users}
    selected_recipient_id = st.selectbox(
        "👥 Chọn người bạn muốn trò chuyện:",
        options=list(user_options.keys()),
        format_func=lambda x: user_options[x]
    )

    recipient = next(u for u in other_users if u["id"] == selected_recipient_id)

    st.markdown(f"""
    <div style="background: #eff6ff; padding: 12px 18px; border-radius: 14px; border: 1.5px solid #bfdbfe; margin-bottom: 16px;">
        <b style="color: #1d4ed8; font-size: 16px;">💬 Cuộc trò chuyện với: {recipient['full_name']}</b> 
        <span style="color: #4b5563; font-size: 14px;">(Lớp {recipient.get('student_class', '')} - {recipient.get('school', '')})</span>
    </div>
    """, unsafe_allow_html=True)

    # Lấy lịch sử hội thoại
    messages = db.get_conversation_messages(user["id"], recipient["id"])

    # Khung hiển thị tin nhắn
    st.markdown("<div style='min-height: 250px; background: #ffffff; padding: 18px; border-radius: 16px; border: 1.5px solid #e2e8f0; margin-bottom: 20px;'>", unsafe_allow_html=True)
    
    if not messages:
        st.markdown("<p style='text-align: center; color: #9ca3af; font-style: italic; margin-top: 50px;'>Chưa có tin nhắn nào. Hãy gửi lời chào đầu tiên đến bạn ấy nhé! 👋</p>", unsafe_allow_html=True)
    else:
        for m in messages:
            is_me = (m["sender_id"] == user["id"])
            align = "flex-end" if is_me else "flex-start"
            bubble_bg = "linear-gradient(135deg, #ff4757 0%, #ff6b81 100%)" if is_me else "#f1f5f9"
            txt_color = "#ffffff" if is_me else "#111827"
            border_radius = "16px 16px 2px 16px" if is_me else "16px 16px 16px 2px"

            st.markdown(f"""
            <div style="display: flex; justify-content: {align}; margin-bottom: 12px;">
                <div style="background: {bubble_bg}; color: {txt_color}; padding: 10px 16px; border-radius: {border_radius}; max-width: 75%; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
                    <div style="font-size: 15.5px; line-height: 1.5;">{m['message_text'] or ''}</div>
                    <div style="font-size: 11px; opacity: 0.75; text-align: right; margin-top: 4px;">{m['created_at'][11:16]}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Hiển thị tệp đính kèm nếu có
            if m["media_path"] and os.path.exists(m["media_path"]):
                m_type = m.get("media_type")
                if m_type == "image":
                    st.image(m["media_path"], width=300)
                elif m_type == "video":
                    st.video(m["media_path"])

    st.markdown("</div>", unsafe_allow_html=True)

    # Form gửi tin nhắn mới
    with st.form("send_msg_form"):
        col_inp, col_att = st.columns([3, 1])
        with col_inp:
            msg_text = st.text_input("Nhập tin nhắn:", placeholder="Nhập nội dung tin nhắn riêng...", key="direct_msg_text")
        with col_att:
            attached_media = st.file_uploader("Gửi ảnh/video:", type=["png", "jpg", "jpeg", "mp4"], key="direct_media_upload")

        if st.form_submit_button("GỬI TIN NHẮN ✈️", use_container_width=True):
            if not msg_text and not attached_media:
                st.error("Vui lòng nhập tin nhắn hoặc chọn ảnh/video cần gửi!")
            else:
                saved_media_path = None
                media_type = None

                if attached_media:
                    f_name = f"chat_{user['id']}_{recipient['id']}_{attached_media.name}"
                    saved_media_path = os.path.join(MEDIA_DIR, f_name)
                    with open(saved_media_path, "wb") as f:
                        f.write(attached_media.getbuffer())
                    media_type = "video" if attached_media.name.lower().endswith(".mp4") else "image"

                db.send_private_message(
                    sender_id=user["id"],
                    receiver_id=recipient["id"],
                    message_text=msg_text,
                    media_path=saved_media_path,
                    media_type=media_type
                )
                st.success("Đã gửi tin nhắn!")
                st.rerun()

