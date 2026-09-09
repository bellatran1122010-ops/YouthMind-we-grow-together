# -*- coding: utf-8 -*-
"""
Phân hệ Kho Tài Liệu & Cẩm Nang Học Đường YouthMind
- Chắt lọc kiến thức tinh hoa từ các tác phẩm tâm lý học và kỹ năng sống kinh điển:
  + "Cẩm Nang Dành Cho Tuổi Teen - Giải Quyết Các Vấn Đề Về Tâm Lý" (Kate Talmul & Penney Warm)
  + "Bộ Sách Gỡ Rối Tuổi Dậy Thì" (Reiko Uchida, Richard L. Travis, Karen Gravelle, Jennifer Gravelle)
  + "Tư Duy Mở" (Nguyễn Anh Dũng)
  + "Thép Đã Tôi Thế Đấy" (Nikolai Alekseyevich Ostrovsky)
  + Các phương pháp tâm lý học thực nghiệm (Thở 4-7-8, Pomodoro, Ma trận Eisenhower, CBT)
- Toàn bộ cẩm nang luôn ở trạng thái thu gọn (expanded=False)
- Bỏ phần tải về và các đề mục dư thừa theo đúng yêu cầu
"""

import streamlit as st

# Danh mục cẩm nang tinh hoa học đường
HANDBOOKS_DATA = [
    {
        "id": "teen_psychology",
        "title": "Cẩm Nang Dành Cho Tuổi Teen - Giải Quyết Các Vấn Đề Về Tâm Lý",
        "author": "Kate Talmul & Penney Warm",
        "category": "Tâm Lý Học Đường",
        "summary": "Hướng dẫn nhận diện những cơn bão cảm xúc tuổi dậy thì, kỹ thuật đối thoại nội tâm, vượt qua nỗi sợ bị phán xét và thiết lập ranh giới tinh thần vững chắc.",
        "content": """
### 📖 Trích Lọc Tinh Hoa: "Cẩm Nang Dành Cho Tuổi Teen - Giải Quyết Các Vấn Đề Về Tâm Lý"
*Tác giả: Kate Talmul & Penney Warm*

---

#### 1. Nhận Diện Những Cơn Bão Cảm Xúc Tuổi Dậy Thì
Ở lứa tuổi học sinh, sự thay đổi mạnh mẽ của các hormone thần kinh kết hợp với áp lực bài vở dày đặc thường khiến tâm lý rơi vào trạng thái bất ổn định:
- **Cảm giác lo âu mơ hồ (Generalized Anxiety):** Luôn thường trực nỗi lo sợ bị thụt lùi, sợ không đạt được kỳ vọng của người lớn.
- **Bất an về ngoại hình và năng lực (Body & Ability Insecurity):** Dễ dàng phóng đại những khuyết điểm nhỏ nhặt thành sự tự ti nghiêm trọng.
- **Nỗi sợ bị cô lập:** Nỗi ám ảnh bị bạn bè xa lánh hoặc bị đánh giá tiêu cực khi không theo kịp trào lưu số đông.

#### 2. Kỹ Thuật Đối Thoại Nội Tâm Lành Mạnh (Self-Talk)
Hai tác giả Kate Talmul và Penney Warm nhấn mạnh rằng kẻ thù lớn nhất không phải là áp lực bên ngoài, mà chính là **người phán xét khắt khe bên trong bạn**:
- **Nguyên tắc "Người Bạn Thân":** Mỗi khi bạn muốn tự trách mình vì một điểm số kém, hãy tự hỏi: *"Nếu người bạn thân nhất của mình gặp hoàn cảnh này, mình sẽ an ủi bạn ấy bằng sự dịu dàng hay bằng những lời cay nghiệt?"*. Hãy đối xử với chính mình như cách bạn đối xử với một người bạn thân.
- **Tách rời cảm xúc khỏi sự thật:** *"Mình cảm thấy thất bại"* không đồng nghĩa với *"Mình là một kẻ thất bại"*. Cảm xúc chỉ là những đám mây trôi qua bầu trời tâm trí, không phải là bản chất con người bạn.

#### 3. Thiết Lập Ranh Giới Tinh Thần Trước Áp Lực Bạn Bè
- Dũng cảm nói lời **"Không"** với những yêu cầu vượt quá sức chịu đựng hoặc đi ngược lại giá trị bản thân.
- Bạn không có nghĩa vụ phải làm hài lòng tất cả mọi người. Sự tôn trọng chân chính chỉ đến khi bạn biết tôn trọng chính giới hạn của mình.
- Khi một mối quan hệ bạn bè chỉ mang lại sự độc hại, ganh đua và chê bai, bạn hoàn toàn có quyền bước lùi lại một bước để bảo vệ sự bình yên trong tâm hồn.
        """
    },
    {
        "id": "puberty_guide",
        "title": "Bộ Sách Gỡ Rối Tuổi Dậy Thì",
        "author": "Reiko Uchida, Richard L. Travis, Karen Gravelle, Jennifer Gravelle",
        "category": "Tâm Lý & Phát Triển Kỹ Năng",
        "summary": "Giải mã những xung đột tâm sinh lý, nghệ thuật giao tiếp với cha mẹ và phương pháp thoát khỏi cái bẫy so sánh xã hội để bảo vệ sự độc bản cá nhân.",
        "content": """
### 📖 Trích Lọc Tinh Hoa: "Bộ Sách Gỡ Rối Tuổi Dậy Thì"
*Tác giả: Reiko Uchida, Richard L. Travis, Karen Gravelle, Jennifer Gravelle*

---

#### 1. Thấu Hiểu Biến Đổi Tâm Sinh Lý
Tuổi dậy thì là giai đoạn bộ não tái cấu trúc mạnh mẽ nhất. Vỏ não trước trán (nơi chịu trách nhiệm về kiểm soát cảm xúc và tư duy logic) vẫn đang hoàn thiện, trong khi hạch hạnh nhân (trung tâm cảm xúc) hoạt động rất nhạy cảm. Do đó:
- Những cơn bực bội, buồn chán hay nhạy cảm quá mức là phản ứng sinh học bình thường của quá trình trưởng thành.
- Nhận thức được điều này giúp bạn không còn tự trách bản thân tại sao mình lại "thất thường" như vậy.

#### 2. Nghệ Thuật Hóa Giải Xung Đột Với Cha Mẹ
Sự bất đồng quan điểm giữa học sinh và phụ huynh thường bắt nguồn từ sự "lệch pha thế hệ" và nỗi lo lắng của người lớn:
- **Lắng nghe sự lo lắng ẩn sau lời thúc giục:** Khi cha mẹ nhắc nhở về điểm số, điều họ thực sự lo lắng là tương lai bạn sẽ vất vả, nhưng họ chưa biết cách diễn đạt bằng sự dịu dàng.
- **Công thức đối thoại 3 bước:**
  1. *Ghi nhận:* "Con biết bố mẹ rất quan tâm và muốn con đạt kết quả tốt."
  2. *Bộc bạch cảm xúc chân thật:* "Nhưng việc liên tục bị so sánh với bạn bè khiến con cảm thấy rất áp lực và ngộp thở."
  3. *Đưa ra giải pháp rõ ràng:* "Con đã lập thời gian biểu tự học mỗi ngày 2 tiếng. Bố mẹ hãy tin tưởng và để con tự chủ nhé."

#### 3. Thoát Khỏi Hội Chứng Sợ Bị Bỏ Lỡ (FOMO)
- Mạng xã hội tạo ra ảo giác rằng mọi người xung quanh đều đang sống một cuộc đời hoàn hảo, tài giỏi và hạnh phúc hơn bạn.
- Hãy nhớ: **Người ta chỉ khoe khoang những lát cắt rực rỡ nhất, không ai đăng tải những giọt mồ hôi hay thất bại.**
- Hãy quay về với thực tại, tận hưởng từng bữa ăn ngon, giấc ngủ sâu và từng trang sách bạn yêu thích thay vì mải miết theo dõi cuộc sống của người khác.
        """
    },
    {
        "id": "open_mindset",
        "title": "Tư Duy Mở (Open Mindset) - Khơi Mở Tiềm Năng Vô Hạn",
        "author": "Nguyễn Anh Dũng",
        "category": "Phát Triển Tư Duy & Học Tập",
        "summary": "Chuyển hóa từ tư duy đóng sang tư duy mở, biến áp lực và thất bại thành nhiên liệu tiến bộ, từ bỏ thói quen so sánh ngang để tập trung vào hành trình độc bản.",
        "content": """
### 📖 Trích Lọc Tinh Hoa: "Tư Duy Mở (Open Mindset)"
*Tác giả: Nguyễn Anh Dũng*

---

#### 1. Sự Khác Biệt Giữa Tư Duy Đóng Và Tư Duy Mở
- **Tư duy đóng (Fixed Mindset):** Tin rằng trí thông minh và tài năng là bẩm sinh, cố định. Khi gặp bài toán khó hay điểm kém, người có tư duy đóng lập tức nghĩ: *"Mình dốt môn này, mình không có năng khiếu, cố gắng cũng vô ích"*.
- **Tư duy mở (Growth Mindset):** Tin rằng mọi năng lực đều có thể rèn luyện và phát triển qua nỗ lực, phương pháp đúng và sự kiên trì. Thất bại không phải là dấu chấm hết, mà là **tín hiệu não bộ đang học hỏi thêm một điều mới**.

#### 2. Biến Áp Lực Điểm Số Thành Nhiên Liệu Tiến Bộ
- Hãy thay đổi ngôn từ bạn nói với chính mình:
  - Thay vì nói: *"Mình không làm được việc này."*
  - Hãy thêm một từ kỳ diệu: *"Mình **CHƯA** làm được việc này ở thời điểm hiện tại, nhưng mình sẽ làm được nếu kiên trì luyện tập."*
- Điểm 5 hay điểm 6 trong một bài kiểm tra không phản ánh giá trị cả đời bạn, nó chỉ là một bài test phản ánh kiến thức phần đó bạn cần ôn lại thêm một lần nữa.

#### 3. Chuyển Từ "So Sánh Ngang" Sang "So Sánh Dọc"
- **So sánh ngang:** Nhìn sang bạn cùng bàn, thấy bạn ấy đạt giải quốc gia, học thêm trường chuyên rồi tự ti, ghen tị và chán nản. Đây là nguồn gốc lớn nhất của Peer Pressure.
- **So sánh dọc:** So sánh chính bạn của ngày hôm nay với bạn của ngày hôm qua. Bạn đã giải thêm được 1 bài toán khó? Đã đọc thêm được 5 trang sách? Đã đi ngủ sớm hơn 30 phút? Nếu có, **bạn đã là người chiến thắng rực rỡ!**
        """
    },
    {
        "id": "steel_tempered",
        "title": "Thép Đã Tôi Thế Đấy",
        "author": "Nikolai Alekseyevich Ostrovsky",
        "category": "Ý Chí & Nghị Lực Sống",
        "summary": "Biểu tượng bất hủ về bản lĩnh kiên cường của tuổi trẻ, ý chí sắt đá vượt qua mọi giông bão thử thách và khát vọng sống cống hiến đầy nhiệt huyết.",
        "content": """
### 📖 Trích Lọc Tinh Hoa: "Thép Đã Tôi Thế Đấy"
*Tác giả: Nikolai Alekseyevich Ostrovsky*

---

#### 1. Tinh Thần Thép Của Pavel Korchagin Trước Thử Thách
Hình tượng chàng thanh niên Pavel Korchagin trong tác phẩm kinh điển của Ostrovsky là ngọn đuốc sáng rực cho mọi thế hệ tuổi trẻ khi đứng trước bão giông:
- Thép không tự nhiên cứng cáp; thép phải được nung trong ngọn lửa rực cháy và tôi luyện trong dòng nước lạnh buốt.
- Những áp lực học đường, những vấp ngã đầu đời và những đêm dài ôn thi mệt mỏi chính là **ngọn lửa tôi luyện ý chí bạn**. Người vượt qua được áp lực sẽ sở hữu nội lực vững vàng không gì lay chuyển nổi.

#### 2. Giá Trị Của Ý Chí Và Tính Kỷ Luật Tự Giác
- Động lực nhất thời chỉ giúp bạn bắt đầu, nhưng **tính kỷ luật kiên định mới đưa bạn đến đích**.
- Khi cảm thấy chán nản và muốn buông xuôi, hãy nhắc nhở bản thân về mục tiêu ban đầu. Từng giờ tự học nghiêm túc, từng bài tập hoàn thành trọn vẹn đều đang đắp xây nên tương lai vững chãi của bạn.

#### 3. Lời Khuyên Bất Hủ Về Giá Trị Thanh Xuân
> *"Cái quý nhất của con người ta là sự sống. Đời người chỉ sống có một lần. Phải sống sao cho khỏi xót xa, ân hận vì những năm tháng đã sống hoài, sống phí, cho khỏi hổ thẹn vì dĩ vãng ti tiện và hèn đớn của mình..."*

Áp lực thi cử hôm nay rồi sẽ qua đi, nhưng bản lĩnh dấn thân, sự kiên cường vượt khó và trái tim chân thành mà bạn rèn luyện được sẽ theo bạn suốt cả cuộc đời. Hãy ngẩng cao đầu và tự tin bước tiếp!
        """
    },
    {
        "id": "pomodoro_eisenhower",
        "title": "Cẩm Nang Quản Trị Thời Gian Pomodoro & Ma Trận Eisenhower",
        "author": "Chuyên Gia Tâm Lý Học Đường",
        "category": "Phương Pháp Học Tập Hiệu Quả",
        "summary": "Chiến lược chia nhỏ khối học tập 25 phút, loại bỏ thói quen trì hoãn và phân bổ thứ tự ưu tiên thông minh để chấm dứt tình trạng quá tải bài vở.",
        "content": """
### 📖 Cẩm Nang Quản Trị Thời Gian Pomodoro & Ma Trận Eisenhower
*Dành riêng cho học sinh đối mặt với khối lượng bài tập lớn*

---

#### 1. Kỹ Thuật Pomodoro Cải Tiến (25/5)
- **Bước 1:** Chọn 1 nhiệm vụ duy nhất (Ví dụ: Làm 5 câu bài tập Toán).
- **Bước 2:** Bật đồng hồ đếm ngược 25 phút. Trong suốt 25 phút này, tắt hoàn toàn wifi điện thoại, không kiểm tra thông báo mạng xã hội.
- **Bước 3:** Khi chuông reo, nghỉ ngơi trọn vẹn 5 phút: đứng dậy vươn vai, uống nước, hít thở sâu.
- **Bước 4:** Sau 4 chu kỳ Pomodoro (khoảng 2 tiếng), thưởng cho bản thân một khoảng nghỉ dài 20-30 phút.

#### 2. Ma Trận Eisenhower: Phân Loại Bài Tập Thông Minh
Đừng cố gắng làm mọi thứ cùng một lúc. Hãy chia bài vở thành 4 nhóm:
1. **Khẩn cấp & Quan trọng (Làm ngay):** Bài tập ngày mai phải nộp, bài kiểm tra sắp tới.
2. **Quan trọng nhưng không khẩn cấp (Lên lịch làm đều đặn):** Học từ vựng Tiếng Anh mỗi ngày, rèn luyện thể thao, đọc sách nâng cao kỹ năng.
3. **Khẩn cấp nhưng không quan trọng (Giảm thiểu/Nhờ vả):** Những tin nhắn tán gẫu của bạn bè khi đang trong giờ học.
4. **Không khẩn cấp & Không quan trọng (Loại bỏ):** Lướt TikTok/Reels vô định hàng giờ đồng hồ.
        """
    },
    {
        "id": "breathing_grounding",
        "title": "Cẩm Nang Kỹ Thuật Hít Thở 4-7-8 & Neo Cảm Xúc (Grounding 5-4-3-2-1)",
        "author": "Khoa Học Tâm Lý Trị Liệu",
        "category": "Sơ Cứu Cảm Xúc Khẩn Cấp",
        "summary": "Phương pháp sinh học kích hoạt hệ thần kinh đối giao cảm, hạ nhịp tim và ngắt cơn hoảng loạn, lo âu cấp tính trước giờ vào phòng thi.",
        "content": """
### 📖 Cẩm Nang Kỹ Thuật Hít Thở 4-7-8 & Neo Cảm Xúc (Grounding)
*Công cụ sơ cứu tâm lý khẩn cấp khi bị quá tải cảm xúc*

---

#### 1. Cơ Chế Thở 4-7-8 (Tiến sĩ Andrew Weil)
Khi bạn lo âu, hơi thở thường nông và dồn dập, khiến não bộ phát tín hiệu nguy hiểm. Kỹ thuật thở 4-7-8 điều hòa lại lượng oxy và kích hoạt hệ thần kinh phó giao cảm (hệ làm dịu):
- **Hít vào nhẹ nhàng bằng mũi:** Đếm thầm từ 1 đến 4.
- **Nín thở giữ hơi:** Đếm thầm từ 1 đến 7 (cho phép oxy thẩm thấu vào mạch máu).
- **Thở ra từ từ bằng miệng:** Đếm thầm từ 1 đến 8 (đẩy khí CO2 và cảm giác nặng nề ra ngoài).
- *Lặp lại 4 lần:* Nhịp tim của bạn sẽ tự động chậm lại và tâm trí trở nên thông suốt.

#### 2. Kỹ Thuật Tiếp Đất Neo Cảm Xúc (Grounding 5-4-3-2-1)
Khi bạn cảm thấy mất kiểm soát hoặc đầu óc quay cuồng trước phòng thi, hãy nhìn xung quanh và gọi tên:
- **5** đồ vật bạn nhìn thấy (ví dụ: chiếc bút, mặt bàn, cây xanh, chiếc quạt, trang giấy).
- **4** cảm giác xúc giác bạn cảm nhận được (ví dụ: chân chạm sàn, áo chạm vào da, tay cầm bút mát lạnh).
- **3** âm thanh bạn nghe thấy (ví dụ: tiếng lá xào xạc, tiếng kim đồng hồ, tiếng quạt gió).
- **2** mùi hương bạn ngửi thấy (ví dụ: mùi trang sách mới, mùi không khí ban mai).
- **1** điều bạn cảm thấy biết ơn lúc này (ví dụ: mình vẫn đang thở và có cơ hội trải nghiệm).
        """
    }
]

def render_documents_page(user):
    """Hiển thị giao diện Kho Tài Liệu & Cẩm Nang Học Đường"""
    st.markdown("""
    <div style="margin-bottom: 22px;">
        <h1 style="color: #ff3366; font-size: 32px; margin-bottom: 6px;">📚 KHO TÀI LIỆU & CẨM NANG HỌC ĐƯỜNG</h1>
        <p style="font-size: 16px; color: #111827; line-height: 1.6;">
            Không gian tri thức tinh hoa: tổng hợp các phương pháp tâm lý học và kỹ năng sống từ các tác phẩm kinh điển dành cho tuổi trẻ.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="custom-card" style="border-left: 5px solid #ff4757; margin-bottom: 20px;">
        <h2 style="color: #ff4757; font-size: 22px; margin-top: 0;">✨ Danh Sách Cẩm Nang Tinh Hoa Dành Cho Học Sinh</h2>
        <p style="font-size: 15px; color: #374151; margin-bottom: 0;">
            Tất cả các cẩm nang đều được thiết kế ở trạng thái thu gọn. Hãy bấm vào tiêu đề cẩm nang bạn quan tâm để mở rộng và đọc kiến thức chi tiết.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Bộ lọc chuyên mục
    categories = ["Tất cả chuyên mục"] + sorted(list(set(d["category"] for d in HANDBOOKS_DATA)))
    c_sel1, c_sel2 = st.columns([1, 2])
    with c_sel1:
        selected_cat = st.selectbox("Lọc theo chủ đề cẩm nang:", categories, index=0)
    with c_sel2:
        search_kw = st.text_input("🔍 Tìm kiếm theo tên cẩm nang hoặc tác giả:", placeholder="Nhập từ khóa...")

    filtered_docs = HANDBOOKS_DATA
    if selected_cat != "Tất cả chuyên mục":
        filtered_docs = [d for d in filtered_docs if d["category"] == selected_cat]

    if search_kw:
        filtered_docs = [d for d in filtered_docs if search_kw.lower() in d["title"].lower() or search_kw.lower() in d["author"].lower() or search_kw.lower() in d["summary"].lower()]

    st.markdown(f"<p style='color: #4b5563; font-size: 14.5px; margin: 10px 0 15px 0;'>Đang hiển thị <b>{len(filtered_docs)}</b> cẩm nang tinh hoa:</p>", unsafe_allow_html=True)

    # Hiển thị từng cẩm nang - LUÔN Ở TRẠNG THÁI THU GỌN (expanded=False) và KHÔNG CÓ NÚT TẢI VỀ
    for doc in filtered_docs:
        with st.expander(f"📖 [{doc['category']}] {doc['title']} – {doc['author']}", expanded=False):
            st.markdown(f"""
            <div style="background: #fff0f3; padding: 14px 18px; border-radius: 12px; border-left: 4px solid #ff4757; margin-bottom: 14px;">
                <b style="color: #be123c; font-size: 15px;">Tác giả:</b> <span style="color: #111827;">{doc['author']}</span><br>
                <b style="color: #be123c; font-size: 15px;">Tóm tắt nội dung:</b> <span style="color: #374151;">{doc['summary']}</span>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(doc["content"])
