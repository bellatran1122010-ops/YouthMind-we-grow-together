# -*- coding: utf-8 -*-
"""
Dashboard Cá Nhân Chi Tiết
- Cam kết bảo mật, không dữ liệu ảo
- Biểu đồ đường (Áp lực MXH) và Biểu đồ cột (Áp lực Học tập) ở các dòng riêng biệt
- Sổ điểm danh tâm trạng (Mood Tracker)
- Thời khóa biểu tùy chỉnh (Thứ, Ngày, Sáng, Chiều) dạng ngang / dọc linh hoạt
- To-Do List cá nhân
"""

import streamlit as st
import database as db
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import date

def render_dashboard_page(user):
    """Hiển thị giao diện Dashboard cá nhân chi tiết"""
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h1 style="color: #ff3366; font-size: 32px; margin-bottom: 6px;">📊 DASHBOARD PHÂN TÍCH CÁ NHÂN</h1>
        <p style="font-size: 16px; color: #4b5563;">
            Báo cáo trực quan tình trạng áp lực, tâm trạng cảm xúc, thời khóa biểu học tập và danh sách việc cần làm.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Lấy dữ liệu thật từ cơ sở dữ liệu (KHÔNG FAKE DATA)
    test_history = db.get_user_test_history(user["id"], test_type="roleplay_20")
    all_tests = db.get_user_test_history(user["id"])
    mood_history = db.get_user_mood_history(user["id"])

    dash_tab1, dash_tab2, dash_tab3, dash_tab4 = st.tabs([
        "📈 Biểu Đồ Áp Lực (Dòng Riêng Biệt)",
        "😊 Sổ Điểm Danh Tâm Trạng",
        "📅 Thời Khóa Biểu Học Tập",
        "✅ Việc Cần Làm (To-Do List)"
    ])

    with dash_tab1:
        render_pressure_charts_separate_rows(test_history)

    with dash_tab2:
        render_mood_tracker(user, mood_history)

    with dash_tab3:
        render_timetable_section(user)

    with dash_tab4:
        render_todo_section(user)

# ==================== 1. BIỂU ĐỒ NẰM Ở CÁC DÒNG RIÊNG BIỆT ====================

def render_pressure_charts_separate_rows(test_history):
    st.markdown("""
    <div class="custom-card" style="border-left: 5px solid #ff4757;">
        <h2 style="color: #ff4757; font-size: 22px; margin-top: 0;">📊 Phân Tích Diễn Biến Áp Lực Học Đường</h2>
        <p style="font-size: 15px; color: #4b5563; margin-bottom: 0;">
            Hệ thống hiển thị dữ liệu bài kiểm tra thực tế của riêng bạn. Hai biểu đồ đường và cột được phân bổ trên <b>hai dòng độc lập</b> để bạn theo dõi sắc nét nhất.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if not test_history:
        st.markdown("""
        <div class="custom-card" style="text-align: center; padding: 40px; border: 2px dashed #fbcfe8;">
            <div style="font-size: 48px; margin-bottom: 12px;">📊</div>
            <h3 style="color: #be123c;">Chưa Có Dữ Liệu Bài Test Nào</h3>
            <p style="font-size: 16px; color: #6b7280; max-width: 550px; margin: 0 auto 16px auto;">
                Hệ thống cam kết <b>bảo mật tuyệt đối và không tự ý điền dữ liệu ảo</b>. 
                Hãy thực hiện bài kiểm tra "20 Tình huống thực tế" để mở khóa toàn bộ biểu đồ phân tích cá nhân của bạn nhé!
            </p>
        </div>
        """, unsafe_allow_html=True)
        return

    # Chuẩn bị dữ liệu vẽ biểu đồ
    dates = [f"Lần #{i+1} ({item['created_at'][5:16]})" for i, item in enumerate(test_history)]
    study_scores = [round(item["score_study"]) for item in test_history]
    social_scores = [round(item["score_social"]) for item in test_history]
    general_scores = [round(item["score_general"]) for item in test_history]

    # DÒNG 1: BIỂU ĐỒ ĐƯỜNG (ÁP LỰC MẠNG XÃ HỘI)
    st.markdown("""
    <div class="custom-card" style="margin-top: 20px;">
        <h3 style="color: #8b5cf6; font-size: 20px; margin-top: 0;">
            🌐 DÒNG 1: BIỂU ĐỒ ĐƯỜNG - DIỄN BIẾN ÁP LỰC MẠNG XÃ HỘI (SOCIAL MEDIA PRESSURE)
        </h3>
        <p style="font-size: 14.5px; color: #4b5563;">
            Đường biểu diễn mức độ bị ảnh hưởng bởi hình ảnh hoàn hảo, so sánh lượt thích hoặc sự thành công ảo trên không gian mạng qua các lần đo.
        </p>
    </div>
    """, unsafe_allow_html=True)

    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=dates,
        y=social_scores,
        mode='lines+markers+text',
        name='Áp lực Mạng Xã Hội',
        text=[f"{s}%" for s in social_scores],
        textposition="top center",
        line=dict(color='#9b59b6', width=4, shape='spline'),
        marker=dict(size=12, color='#8e44ad', symbol='circle')
    ))

    fig_line.update_layout(
        title="Xu Hướng Áp Lực Mạng Xã Hội Qua Các Lần Kiểm Tra",
        xaxis_title="Thời Gian / Lần Đo",
        yaxis_title="Mức Độ Áp Lực (%)",
        yaxis=dict(range=[0, 110]),
        template="plotly_white",
        font=dict(family="Times New Roman", size=15),
        height=380,
        margin=dict(l=40, r=40, t=60, b=40)
    )
    st.plotly_chart(fig_line, use_container_width=True)

    # DÒNG 2: BIỂU ĐỒ CỘT (ÁP LỰC HỌC TẬP)
    st.markdown("""
    <div class="custom-card" style="margin-top: 30px;">
        <h3 style="color: #2ed573; font-size: 20px; margin-top: 0;">
            📚 DÒNG 2: BIỂU ĐỒ CỘT - CHỈ SỐ ÁP LỰC HỌC TẬP (ACADEMIC PRESSURE)
        </h3>
        <p style="font-size: 14.5px; color: #4b5563;">
            Cột so sánh mức độ căng thẳng điểm số, khối lượng bài tập và kỳ vọng gia đình/thầy cô giữa các lần kiểm tra.
        </p>
    </div>
    """, unsafe_allow_html=True)

    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        x=dates,
        y=study_scores,
        name='Áp lực Học Tập',
        text=[f"{s}%" for s in study_scores],
        textposition="outside",
        marker_color=['#2ed573' if s <= 50 else ('#ffa502' if s <= 75 else '#ff4757') for s in study_scores],
        width=0.45
    ))

    fig_bar.update_layout(
        title="Mức Độ Áp Lực Học Tập Qua Các Lần Kiểm Tra (Xanh: Ổn định | Vàng: Cần chú ý | Đỏ: Căng thẳng cao)",
        xaxis_title="Thời Gian / Lần Đo",
        yaxis_title="Mức Độ Áp Lực (%)",
        yaxis=dict(range=[0, 110]),
        template="plotly_white",
        font=dict(family="Times New Roman", size=15),
        height=380,
        margin=dict(l=40, r=40, t=60, b=40)
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# ==================== 2. SỔ ĐIỂM DANH TÂM TRẠNG ====================

def render_mood_tracker(user, mood_history):
    st.markdown("""
    <div class="custom-card" style="border-left: 5px solid #10b981;">
        <h2 style="color: #10b981; font-size: 22px; margin-top: 0;">😊 Sổ Điểm Danh Tâm Trạng Hằng Ngày (Mood Attendance)</h2>
        <p style="font-size: 15px; color: #4b5563;">
            Ghi nhận cảm xúc mỗi ngày giúp bạn kết nối với nội tâm, theo dõi biến động tâm lý và phát hiện sớm dấu hiệu quá tải.
        </p>
    </div>
    """, unsafe_allow_html=True)

    today_entry = db.get_today_mood(user["id"])

    # Form điểm danh hôm nay
    st.markdown("<h3 style='color: #059669;'>🌸 Điểm Danh Cảm Xúc Ngày Hôm Nay:</h3>", unsafe_allow_html=True)
    
    mood_options = [
        "😊 Vui vẻ & Tự tin",
        "🌿 Bình yên & Thư thái",
        "🤔 Hơi lo lắng về bài vở",
        "⚡ Căng thẳng trước kỳ thi",
        "🥱 Mệt mỏi & Kiệt sức",
        "😔 Tự ti & Chán chường"
    ]

    default_mood_idx = 0
    default_energy = 3
    default_note = ""

    if today_entry:
        for idx, m_opt in enumerate(mood_options):
            if today_entry["mood"] in m_opt:
                default_mood_idx = idx
                break
        default_energy = today_entry.get("energy_level", 3)
        default_note = today_entry.get("note", "")

    with st.form("mood_form"):
        col_m1, col_m2 = st.columns([1, 1])
        with col_m1:
            selected_mood = st.selectbox("Tâm trạng chủ đạo hôm nay:", mood_options, index=default_mood_idx)
            energy = st.slider("Mức năng lượng cơ thể (1: Cạn kiệt -> 5: Tràn đầy):", 1, 5, value=default_energy)
        with col_m2:
            mood_note = st.text_area("Ghi chú ngắn về cảm xúc / Nguyên nhân:", value=default_note, placeholder="Hôm nay mình cảm thấy thế nào? Có chuyện gì khiến mình vui hay bận tâm?", height=110)

        submit_mood = st.form_submit_button("LƯU ĐIỂM DANH HÔM NAY", use_container_width=True)

    if submit_mood:
        db.log_mood(user["id"], selected_mood, energy, mood_note)
        st.success(f"✅ Đã điểm danh thành công: {selected_mood} (Năng lượng {energy}/5 ⭐)")
        st.rerun()

    # Hiển thị lịch sử điểm danh gần đây
    if mood_history:
        st.markdown("<h3 style='color: #059669; margin-top: 25px;'>📅 Lịch Sử Điểm Danh Cảm Xúc:</h3>", unsafe_allow_html=True)
        m_data = []
        for entry in reversed(mood_history):
            m_data.append({
                "Ngày": entry["logged_date"],
                "Tâm trạng": entry["mood"],
                "Mức năng lượng": f"{entry['energy_level']} / 5 ⭐",
                "Ghi chú ngắn": entry["note"] or "(Không ghi chú)"
            })
        st.dataframe(pd.DataFrame(m_data), use_container_width=True, hide_index=True)
    else:
        st.info("Chưa có lịch sử điểm danh nào. Hãy bắt đầu điểm danh cảm xúc hôm nay nhé!")

# ==================== 3. THỜI KHÓA BIỂU HỌC TẬP ====================

def render_timetable_section(user):
    st.markdown("""
    <div class="custom-card" style="border-left: 5px solid #2563eb;">
        <h2 style="color: #2563eb; font-size: 22px; margin-top: 0;">📅 Thời Khóa Biểu Tùy Chỉnh (Thứ, Ngày, Sáng, Chiều)</h2>
        <p style="font-size: 15px; color: #4b5563;">
            Lên kế hoạch học tập khoa học, cân đối giữa buổi sáng và buổi chiều để tránh dồn bài tập gây kiệt sức.
        </p>
    </div>
    """, unsafe_allow_html=True)

    entries = db.get_user_timetable(user["id"])
    
    # Nút chuyển đổi định dạng xem: Dạng Ngang hoặc Dạng Dọc
    col_t1, col_t2 = st.columns([2, 1])
    with col_t2:
        view_mode = st.radio("Chế độ hiển thị thời khóa biểu:", ["📊 Dạng Ngang (Bảng)", "📑 Dạng Dọc (Từng Ngày)"], horizontal=True)

    if view_mode == "📊 Dạng Ngang (Bảng)":
        table_rows = []
        for e in entries:
            table_rows.append({
                "Thứ": e["day_of_week"],
                "Buổi Sáng (Chính khóa / Tự học)": e["morning_schedule"] or "-",
                "Buổi Chiều (Học thêm / Ôn tập)": e["afternoon_schedule"] or "-",
                "Ghi Chú / Mục Tiêu Ngày": e["notes"] or "-"
            })
        st.dataframe(pd.DataFrame(table_rows), use_container_width=True, hide_index=True)

    else:
        for e in entries:
            with st.expander(f"📌 {e['day_of_week']}", expanded=True):
                st.markdown(f"""
                <div style="background: #eff6ff; padding: 12px; border-radius: 12px; margin-bottom: 8px;">
                    <b style="color: #1d4ed8;">🌅 Buổi Sáng:</b> {e['morning_schedule'] or 'Chưa có lịch'}
                </div>
                <div style="background: #fff7ed; padding: 12px; border-radius: 12px; margin-bottom: 8px;">
                    <b style="color: #c2410c;">🌇 Buổi Chiều:</b> {e['afternoon_schedule'] or 'Chưa có lịch'}
                </div>
                <div style="background: #f8fafc; padding: 12px; border-radius: 12px;">
                    <b style="color: #475569;">📝 Ghi chú:</b> {e['notes'] or 'Không có ghi chú'}
                </div>
                """, unsafe_allow_html=True)

    # Form cập nhật thời khóa biểu
    st.markdown("<h3 style='color: #1e40af; margin-top: 25px;'>✏️ Cập Nhật Lịch Học Từng Thứ Trong Tuần:</h3>", unsafe_allow_html=True)
    
    selected_day = st.selectbox("Chọn thứ muốn cập nhật:", [e["day_of_week"] for e in entries])
    current_entry = next(e for e in entries if e["day_of_week"] == selected_day)

    with st.form("edit_timetable_form"):
        col_e1, col_e2 = st.columns(2)
        with col_e1:
            new_morning = st.text_area("Lịch buổi Sáng:", value=current_entry["morning_schedule"] or "", height=90)
        with col_e2:
            new_afternoon = st.text_area("Lịch buổi Chiều:", value=current_entry["afternoon_schedule"] or "", height=90)
        new_notes = st.text_input("Ghi chú / Mục tiêu ngày:", value=current_entry["notes"] or "")

        if st.form_submit_button("LƯU CẬP NHẬT THỜI KHÓA BIỂU", use_container_width=True):
            db.update_timetable_entry(current_entry["id"], new_morning, new_afternoon, new_notes)
            st.success(f"✅ Đã cập nhật thành công lịch học cho {selected_day}!")
            st.rerun()

# ==================== 4. TO-DO LIST ====================

def render_todo_section(user):
    st.markdown("""
    <div class="custom-card" style="border-left: 5px solid #8b5cf6;">
        <h2 style="color: #8b5cf6; font-size: 22px; margin-top: 0;">✅ Danh Sách Việc Cần Làm (To-Do List)</h2>
        <p style="font-size: 15px; color: #4b5563;">
            Ghi chú các bài tập và công việc cần xử lý. Hoàn thành từng mục nhỏ sẽ giúp bạn giảm bớt cảm giác quá tải bài vở.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Form thêm việc mới
    with st.form("add_todo_form"):
        c_t1, c_t2, c_t3 = st.columns([3, 1, 1])
        with c_t1:
            task_text = st.text_input("Nội dung bài tập / Công việc cần làm:", placeholder="Ví dụ: Làm bài tập Toán trang 45, Đọc tài liệu Ngữ văn...")
        with c_t2:
            priority = st.selectbox("Mức ưu tiên:", ["Cao", "Bình thường", "Thấp"], index=1)
        with c_t3:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            add_btn = st.form_submit_button("➕ THÊM VIỆC", use_container_width=True)

    if add_btn and task_text:
        db.add_todo(user["id"], task_text, priority)
        st.success("Đã thêm việc cần làm mới!")
        st.rerun()

    todos = db.get_user_todos(user["id"])
    
    if not todos:
        st.info("Chưa có việc cần làm nào trong danh sách. Hãy thêm nhiệm vụ đầu tiên của bạn nhé!")
        return

    # Tính tỷ lệ hoàn thành
    done_count = sum(1 for t in todos if t["is_done"])
    pct_done = int((done_count / len(todos)) * 100)
    
    st.markdown(f"""
    <div style="margin: 15px 0 20px 0;">
        <div style="display: flex; justify-content: space-between; font-weight: bold; margin-bottom: 6px;">
            <span>Tiến độ hoàn thành:</span>
            <span style="color: #8b5cf6;">{done_count} / {len(todos)} việc ({pct_done}%)</span>
        </div>
        <div style="background: #e2e8f0; border-radius: 10px; height: 12px; width: 100%; overflow: hidden;">
            <div style="background: linear-gradient(90deg, #a855f7, #6366f1); height: 100%; width: {pct_done}%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    for item in todos:
        c_chk, c_txt, c_prio, c_del = st.columns([0.5, 3.5, 1, 0.8])
        with c_chk:
            is_checked = st.checkbox("", value=bool(item["is_done"]), key=f"todo_chk_{item['id']}")
            if is_checked != bool(item["is_done"]):
                db.toggle_todo(item["id"], is_checked)
                st.rerun()
        with c_txt:
            style_str = "text-decoration: line-through; color: #9ca3af;" if item["is_done"] else "color: #111827;"
            st.markdown(f"<span style='font-size: 16px; {style_str}'>{item['task_text']}</span>", unsafe_allow_html=True)
        with c_prio:
            color_map = {"Cao": "#ef4444", "Bình thường": "#f59e0b", "Thấp": "#10b981"}
            st.markdown(f"<span style='background: {color_map.get(item['priority'], '#6b7280')}20; color: {color_map.get(item['priority'], '#6b7280')}; padding: 3px 8px; border-radius: 8px; font-weight: bold; font-size: 13px;'>{item['priority']}</span>", unsafe_allow_html=True)
        with c_del:
            if st.button("🗑️ Xóa", key=f"del_todo_{item['id']}"):
                db.delete_todo(item["id"])
                st.rerun()


