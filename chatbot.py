# -*- coding: utf-8 -*-
"""
Phân hệ Chatbox Gia Sư AI: Bạn Đồng Hành Học Tập & Tâm Lý YouthMind
- Tích hợp Google Gemini AI qua Google AI API Key: AQ.Ab8RN6JakywLews3BDi7OUN5OFPIfI9WXVcShEJaEXBXK0LuEw
- Huấn luyện theo phương pháp gợi mở (Socratic Method):
  + KHÔNG giải hộ bài tập hay đưa ra đáp án trực tiếp
  + Luôn dùng câu hỏi gợi mở để học sinh tự suy luận
  + Hướng dẫn phương pháp học tập: Pomodoro, Feynman, Active Recall, Spaced Repetition
  + Lập kế hoạch học tập cá nhân hóa & vượt qua áp lực tâm lý học đường
"""

import streamlit as st
import database as db
import json
import os
import requests

DEFAULT_CHATBOT_API_KEY = "AQ.Ab8RN6INvYRG3il5ShUwteiHxepddd13rWLpMC7UmMBImqPc5w"

SYSTEM_PROMPT_TEMPLATE = """
Bạn là "Gia Sư AI" - một người bạn đồng hành thông minh, thân thiện và tận tâm, chuyên hỗ trợ học sinh học tập đúng cách, xây dựng kế hoạch và phát triển tư duy. 

### 1. Nguyên tắc cốt lõi (Socratic Method)
- KHÔNG BAO GIỜ giải bài tập hộ hay đưa ra đáp án trực tiếp ngay từ đầu.
- Luôn sử dụng câu hỏi gợi mở để học sinh tự suy luận, tìm ra bản chất vấn đề.
- Khen ngợi sự tiến bộ dù là nhỏ nhất để khích lệ tinh thần học tập của các em.

### 2. Nhiệm vụ chính
a. Hướng dẫn phương pháp học tập đúng cách (Pomodoro, Feynman, Active Recall, Spaced Repetition).
b. Đưa ra lời khuyên tâm lý học tập, cách vượt qua áp lực, chống trì hoãn.
c. Hỗ trợ học sinh lập kế hoạch học tập cá nhân hóa theo ngày/tuần dựa trên khối lượng công việc và mục tiêu của các em.

### 3. Phong cách giao tiếp
- Xưng hô: Thân thiện, ấm áp (ví dụ: Mình - Bạn, Cậu - Tớ).
- Ngôn ngữ: Trong sáng, dễ hiểu, tránh dùng từ ngữ quá hàn lâm.
- Trình bày: Rõ ràng, sử dụng gạch đầu dòng, định dạng in đậm để học sinh dễ theo dõi (tránh viết đoạn văn quá dài).

### 4. Quy trình xử lý khi học sinh hỏi bài hoặc nhờ lập kế hoạch
- Bước 1: Lắng nghe và thấu hiểu vấn đề/cảm xúc của học sinh.
- Bước 2: Chia nhỏ mục tiêu hoặc bài toán lớn thành các bước dễ thực hiện hơn.
- Bước 3: Đặt câu hỏi định hướng hoặc đưa ra khung kế hoạch mẫu để học sinh cùng điền vào.

### Thông tin ngữ cảnh học sinh đang trò chuyện:
- Tên học sinh: {name}
- Chỉ số Áp lực học tập: {study_score}
- Chỉ số Áp lực mạng xã hội: {social_score}
- Chỉ số Lòng tự trọng (RSES): {rses_score}
- Tâm trạng hôm nay: {today_mood}
- Khối lượng việc đang chờ: {pending_todos}
"""

def render_chatbot_page(user):
    """Hiển thị giao diện Chatbox Gia Sư AI"""
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h1 style="color: #ff3366; font-size: 32px; margin-bottom: 6px;">🤖 CHATBOX GIA SƯ AI - BẠN ĐỒNG HÀNH HỌC TẬP</h1>
        <p style="font-size: 16px; color: #111827; line-height: 1.6;">
            Trợ lý học tập thông minh theo phương pháp gợi mở <b>Socratic Method</b>: hỗ trợ phương pháp học tập, lập kế hoạch cá nhân hóa và thấu hiểu áp lực tâm lý.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 1. TỔNG HỢP TOÀN DIỆN NGỮ CẢNH HỌC SINH
    latest_test = db.get_latest_test_result(user["id"], "roleplay_20")
    latest_rses = db.get_latest_test_result(user["id"], "rses_10")
    today_mood = db.get_today_mood(user["id"])
    todos = db.get_user_todos(user["id"])
    pending_todos = [t for t in todos if not t["is_done"]]

    st.markdown("""
    <div class="custom-card" style="background: linear-gradient(135deg, #fff5f7 0%, #fff0f3 100%); border: 1.5px solid #ffccd5; padding: 18px 22px; margin-bottom: 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <b style="color: #e11d48; font-size: 16px;">🔗 Dữ Liệu Học Sinh Đang Được Đồng Bộ Trực Tiếp Với Gia Sư AI:</b>
            <span style="background: #2ed573; color: white; padding: 3px 12px; border-radius: 12px; font-size: 13px; font-weight: bold;">Đang Kết Nối Gemini AI</span>
        </div>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; font-size: 14.5px; color: #1f2937;">
            <div>👤 <b>Học sinh:</b> {name}</div>
            <div>📊 <b>Áp lực Học tập:</b> {study_pct}</div>
            <div>🌐 <b>Áp lực Mạng xã hội:</b> {social_pct}</div>
            <div>💎 <b>Lòng tự trọng (RSES):</b> {rses_stat}</div>
            <div>😊 <b>Tâm trạng hôm nay:</b> {mood_stat}</div>
            <div>📋 <b>Nhiệm vụ đang chờ:</b> {todo_stat}</div>
        </div>
    </div>
    """.format(
        name=user["full_name"],
        study_pct=f"{round(latest_test['score_study'])}%" if latest_test else "Chưa đo",
        social_pct=f"{round(latest_test['score_social'])}%" if latest_test else "Chưa đo",
        rses_stat=f"{round(latest_rses['score_general'])}/40 điểm" if latest_rses else "Chưa đo",
        mood_stat=today_mood["mood"] if today_mood else "Chưa điểm danh",
        todo_stat=f"{len(pending_todos)} việc" if pending_todos else "0 việc"
    ), unsafe_allow_html=True)

    # 2. KHỞI TẠO LỊCH SỬ CHAT VÀ CẤU HÌNH API KEY
    if "gemini_api_key" not in st.session_state:
        st.session_state["gemini_api_key"] = DEFAULT_CHATBOT_API_KEY

    if "chat_messages" not in st.session_state:
        welcome_msg = (
            f"Chào {user['full_name']}! Mình là **Gia Sư AI** - người bạn đồng hành của bạn trong học tập và phát triển tư duy. 🌸\n\n"
            "Mình ở đây để giúp bạn:\n"
            "- 🎯 **Lập kế hoạch học tập cá nhân hóa** theo ngày/tuần để không bị quá tải.\n"
            "- 💡 **Gợi mở tư duy bài tập khó** theo phương pháp Socratic (mình sẽ không giải hộ đâu nhé, mà sẽ cùng bạn tìm ra bản chất vấn đề!).\n"
            "- 🧘 **Giải tỏa áp lực điểm số, so sánh bạn bè** và xây dựng phương pháp học hiệu quả (Pomodoro, Feynman, Active Recall).\n\n"
            "Hôm nay bạn đang băn khoăn về bài học nào hay cần mình hỗ trợ lập kế hoạch việc gì không? Hãy chia sẻ cùng mình nhé!"
        )
        st.session_state["chat_messages"] = [
            {"role": "assistant", "content": welcome_msg}
        ]

    # Cấu hình API Key (Mặc định đã nạp Google AI API Key)
    with st.expander("⚙️ Cấu hình Google AI API Key", expanded=False):
        api_key_input = st.text_input(
            "Google AI API Key:",
            type="password",
            value=st.session_state.get("gemini_api_key", DEFAULT_CHATBOT_API_KEY),
            key="gemini_key_input"
        )
        if api_key_input:
            st.session_state["gemini_api_key"] = api_key_input

    # 3. HIỂN THỊ HỘI THOẠI
    for msg in st.session_state["chat_messages"]:
        if msg["role"] == "user":
            st.markdown(f"""
            <div style="display: flex; justify-content: flex-end; margin-bottom: 14px;">
                <div style="background: linear-gradient(135deg, #ff4757 0%, #ff6b81 100%); color: white; padding: 12px 18px; border-radius: 18px 18px 2px 18px; max-width: 80%; box-shadow: 0 4px 12px rgba(255, 71, 87, 0.25); font-size: 16px; line-height: 1.6;">
                    {msg['content']}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="display: flex; justify-content: flex-start; margin-bottom: 14px;">
                <div style="background: #ffffff; color: #111827; border: 1.5px solid #ffd1dc; padding: 16px 20px; border-radius: 18px 18px 18px 2px; max-width: 85%; box-shadow: 0 4px 14px rgba(255, 105, 180, 0.08); font-size: 16px; line-height: 1.7;">
                    <div style="font-weight: bold; color: #ff3366; font-size: 14.5px; margin-bottom: 6px;">🌸 Gia Sư AI Đồng Hành:</div>
                    {msg['content']}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # 4. GỢI Ý CÂU HỎI NHANH
    st.markdown("<p style='font-size: 14px; font-weight: bold; color: #6b7280; margin-bottom: 6px;'>💡 Gợi ý chủ đề nhanh:</p>", unsafe_allow_html=True)
    q_col1, q_col2, q_col3 = st.columns(3)
    quick_prompt = None
    with q_col1:
        if st.button("📋 Giúp mình lập kế hoạch học tập tuần này", use_container_width=True):
            quick_prompt = "Mình đang có khá nhiều bài tập cần hoàn thành, bạn giúp mình lập kế hoạch học tập chi tiết cho tuần này với!"
    with q_col2:
        if st.button("🧠 Hướng dẫn phương pháp Feynman & Pomodoro", use_container_width=True):
            quick_prompt = "Bạn hướng dẫn mình cách áp dụng phương pháp học Feynman và Pomodoro để nhớ lâu và bớt trì hoãn nhé."
    with q_col3:
        if st.button("❓ Mình gặp bài toán khó, bạn gợi ý giúp mình", use_container_width=True):
            quick_prompt = "Mình đang gặp một bài tập khó và chưa biết bắt đầu từ đâu, bạn đặt câu hỏi gợi mở hướng dẫn mình tự giải nhé."

    # 5. KHUNG NHẬP TIN NHẮN
    user_input = st.chat_input("Nhập tin nhắn tâm sự hoặc câu hỏi cần Gia Sư AI hướng dẫn...")
    prompt_to_process = quick_prompt or user_input

    if prompt_to_process:
        st.session_state["chat_messages"].append({"role": "user", "content": prompt_to_process})
        
        # Tạo phản hồi thông minh với Gemini API và toàn bộ ngữ cảnh
        response_text = generate_ai_response(
            prompt=prompt_to_process,
            user=user,
            latest_test=latest_test,
            latest_rses=latest_rses,
            today_mood=today_mood,
            pending_todos=pending_todos
        )

        st.session_state["chat_messages"].append({"role": "assistant", "content": response_text})
        st.rerun()

def build_gemini_contents_history(current_prompt):
    """Định dạng lịch sử hội thoại nhiều lượt cho Gemini API"""
    contents = []
    history = st.session_state.get("chat_messages", [])
    # Lấy tối đa 10 tin nhắn gần nhất để giữ ngữ cảnh liền mạch
    recent_history = history[-10:] if len(history) > 10 else history
    
    for m in recent_history:
        role = "user" if m["role"] == "user" else "model"
        contents.append({
            "role": role,
            "parts": [{"text": m["content"]}]
        })
    
    if not contents or contents[-1]["parts"][0]["text"] != current_prompt:
        contents.append({
            "role": "user",
            "parts": [{"text": current_prompt}]
        })
    return contents

def generate_ai_response(prompt, user, latest_test, latest_rses, today_mood, pending_todos):
    """Xử lý tạo câu trả lời với Google Gemini AI (gemini-3.6-flash) theo đúng nguyên tắc Gia Sư AI"""
    api_key = st.session_state.get("gemini_api_key", DEFAULT_CHATBOT_API_KEY)
    
    # Xây dựng System Instruction cá nhân hóa cho học sinh
    system_instruction = SYSTEM_PROMPT_TEMPLATE.format(
        name=user["full_name"],
        study_score=f"{round(latest_test['score_study'])}%" if latest_test else "Chưa đo",
        social_score=f"{round(latest_test['score_social'])}%" if latest_test else "Chưa đo",
        rses_score=f"{round(latest_rses['score_general'])}/40" if latest_rses else "Chưa đo",
        today_mood=today_mood["mood"] if today_mood else "Bình thường",
        pending_todos=f"{len(pending_todos)} nhiệm vụ" if pending_todos else "0 việc"
    )

    if api_key:
        # Danh sách các model Gemini hiện đại được hỗ trợ bởi Google AI
        supported_models = [
            "gemini-3.6-flash",
            "gemini-flash-latest",
            "gemini-2.5-pro",
            "gemini-3.5-flash"
        ]

        contents = build_gemini_contents_history(prompt)

        for model_name in supported_models:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
                payload = {
                    "system_instruction": {
                        "parts": [{"text": system_instruction}]
                    },
                    "contents": contents,
                    "generationConfig": {
                        "temperature": 0.7,
                        "maxOutputTokens": 1024
                    }
                }
                res = requests.post(url, json=payload, timeout=15)
                if res.status_code == 200:
                    data = res.json()
                    if "candidates" in data and len(data["candidates"]) > 0:
                        candidate = data["candidates"][0]
                        if "content" in candidate and "parts" in candidate["content"]:
                            return candidate["content"]["parts"][0]["text"]
            except Exception:
                continue

    # ==================== DỰ PHÒNG CỤC BỘ: LOCAL SOCRATIC GIA SƯ ENGINE ====================
    # Dự phòng thông minh chuẩn Socratic Method nếu mạng ngắt kết nối
    prompt_lower = prompt.lower()
    name = user["full_name"]

    if any(k in prompt_lower for k in ["kế hoạch", "lập kế hoạch", "thời gian biểu", "sắp xếp"]):
        return f"""
Chào {name}! Mình rất vui vì cậu đã chủ động muốn lên kế hoạch học tập. Lên kế hoạch là bước đầu tiên để biến những áp lực bài vở thành các bước đi cụ thể và nhẹ nhàng đấy! 🎯

Để mình cùng cậu xây dựng một **khung kế hoạch học tập cá nhân hóa** thật thực tế và không bị kiệt sức, cậu hãy trả lời giúp mình 3 câu hỏi nhỏ này nhé:

1. **Mục tiêu quan trọng nhất:** Trong tuần này, môn học hoặc bài kiểm tra nào là ưu tiên số 1 của cậu?
2. **Khối lượng bài vở:** Cậu đang có khoảng bao nhiêu bài tập cần hoàn thành trước ngày nào?
3. **Thời gian tự học:** Mỗi buổi tối, cậu cảm thấy bản thân tập trung tốt nhất trong khoảng bao nhiêu tiếng (ví dụ: 1.5 tiếng hay 2 tiếng)?

Hãy chia sẻ với mình nhé, rồi chúng mình cùng bắt tay vào chia nhỏ từng khung giờ học theo phương pháp **Pomodoro (25 phút học - 5 phút nghỉ)** nha! ✨
        """

    elif any(k in prompt_lower for k in ["giải hộ", "bài tập", "toán", "văn", "lý", "hóa", "tiếng anh", "bài 1", "đáp án"]):
        return f"""
Chào {name}! Mình hiểu là cậu đang đứng trước một bài tập khó và cảm thấy bối rối. Đừng lo lắng nhé, ai trong chúng mình cũng từng có những lúc gặp bài toán "hóc búa" như vậy.

Tuy nhiên, với tư cách là **Gia Sư AI**, mình sẽ **không đưa ra đáp án hay giải hộ cậu ngay từ đầu** đâu nhé 😉. Vì nếu mình giải hộ, cậu sẽ mất đi cơ hội rèn luyện tư duy và niềm vui khi tự mình chinh phục nó!

Thay vào đó, mình sẽ đồng hành và đưa ra gợi ý từng bước một:
- **Bước 1:** Cậu hãy gõ hoặc tóm tắt **đề bài** ra đây cho mình nhé.
- **Bước 2:** Cậu hãy cho mình biết bài tập này thuộc **chủ đề/dạng bài** nào mà thầy cô đã dạy trên lớp?
- **Bước 3:** Cho đến thời điểm này, cậu đã thử làm được đến bước nào rồi, hay có công thức nào cậu nghĩ là có thể áp dụng không?

Cứ bình tĩnh chia sẻ nhé, chúng mình cùng nhau gỡ rối từng chút một nào! 💡
        """

    elif any(k in prompt_lower for k in ["feynman", "pomodoro", "active recall", "spaced repetition", "phương pháp học"]):
        return f"""
Tuyệt vời quá {name}! Cậu đang tìm hiểu về những **vũ khí học tập tối thượng** đã được khoa học thần kinh chứng minh hiệu quả đấy:

1. 🍅 **Phương pháp Pomodoro (Chống kiệt sức & Trì hoãn):**
   - Học tập tập trung cao độ trong **25 phút** (tắt mạng xã hội).
   - Nghỉ ngơi trọn vẹn **5 phút** (vươn vai, uống nước, hít thở sâu).
   - Sau 4 chu kỳ, tự thưởng cho mình một khoảng nghỉ dài 20-30 phút.

2. 🧠 **Kỹ thuật Feynman (Hiểu sâu bản chất):**
   - Chọn một khái niệm khó và thử giải thích lại nó bằng ngôn từ đơn giản nhất như đang dạy cho một đứa trẻ 10 tuổi.
   - Chỗ nào cậu bị ngắc ngứ, đó chính là "lỗ hổng kiến thức" cần mở sách ôn lại ngay.

3. 📝 **Active Recall (Chủ động nhớ lại) & Spaced Repetition (Lặp lại ngắt quãng):**
   - Thay vì đọc đi đọc lại một trang sách một cách thụ động, hãy gấp sách lại và tự hỏi: *"Trang vừa rồi có những ý chính nào?"*.
   - Ôn lại kiến thức sau 1 ngày, 3 ngày, 7 ngày để chuyển thông tin vào bộ nhớ dài hạn.

Cậu muốn chúng mình cùng áp dụng phương pháp nào vào môn học cụ thể của cậu tối nay không? Chia sẻ với mình nhé! 🌸
        """

    elif any(k in prompt_lower for k in ["áp lực", "lo âu", "mệt mỏi", "stress", "nản", "chán", "so sánh"]):
        return f"""
{name} ơi, mình lắng nghe và thấu hiểu trọn vẹn cảm giác này của cậu. Khi khối lượng bài vở dồn dập hay chứng kiến bạn bè xung quanh dường như đang làm quá tốt, chúng mình rất dễ rơi vào trạng thái kiệt sức ngầm và nghi ngờ giá trị bản thân.

Cậu hãy dừng lại một nhịp, buông cây bút xuống và cùng mình làm một việc đơn giản này nhé:
- 🌿 **Hít một hơi thật sâu bằng mũi trong 4 giây**, rồi thở ra từ từ bằng miệng trong 8 giây.
- Nhớ rằng: **Bông hoa sen không nở cùng lúc với hoa phượng**, mỗi người có một hành trình và tốc độ trưởng thành của riêng mình.

Cậu đã luôn rất nỗ lực cho đến tận hôm nay rồi, đó đã là một điều vô cùng đáng tự hào! Cậu có muốn chia sẻ cụ thể điều gì đang khiến cậu cảm thấy nặng nề nhất lúc này không? Mình luôn ở đây để lắng nghe cậu. 💛
        """

    else:
        return f"""
Chào {name}! Mình là Gia Sư AI, luôn sẵn sàng đồng hành cùng cậu trên hành trình học tập và rèn luyện tư duy.

Hôm nay cậu đang muốn:
- 📋 **Lập kế hoạch học tập** cho tuần mới?
- 💡 **Thảo luận về một bài tập khó** (mình sẽ đặt câu hỏi gợi ý để cậu tự giải)?
- 🧘 **Học phương pháp ghi nhớ sâu** hay tìm cách giải tỏa áp lực thi cử?

Cậu hãy chia sẻ cho mình biết nhé, chúng mình cùng nhau tiến bộ từng bước một nào! 🌱
        """
