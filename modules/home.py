# -*- coding: utf-8 -*-
"""
Trang Chủ (Home): Tổng quan hệ thống YouthMind, thống kê cá nhân nhanh,
chuỗi streak, lời khuyên thay đổi mỗi ngày theo 31 ngày trong tháng và lộ trình 5 bước.
"""

import streamlit as st
import database as db
from datetime import datetime

# Danh sách 31 câu lời khuyên & thành ngữ luân phiên mỗi ngày 1 câu
DAILY_ADVICES_31 = [
    {
        "advice": "Tốc độ của mỗi người là khác nhau. Bông hoa sen không nở cùng lúc với hoa phượng, nhưng cả hai đều mang vẻ đẹp rực rỡ đúng mùa của riêng mình. Đừng dùng thước đo của người khác để phán xét hành trình độc bản của bạn. Hãy tự hào vì bạn đã luôn nỗ lực không ngừng nghỉ!",
        "proverb": "✨ Ca dao Việt Nam: \"Chớ thấy sóng cả mà ngã tay chèo\" – Vững vàng nội tại, tin tưởng chính mình."
    },
    {
        "advice": "Tốc độ của mỗi người là khác nhau. Bông hoa sen không nở cùng lúc với hoa phượng, nhưng cả hai đều mang vẻ đẹp rực rỡ đúng mùa của mình. Đừng dùng thước đo của người khác để phán xét hành trình độc bản của bạn. Hãy tự hào vì bạn đã luôn nỗ lực không ngừng nghỉ!",
        "proverb": "✨ Ca dao Việt Nam: \"Chớ thấy sóng cả mà ngã tay chèo\" – Vững vàng nội tại, tin tưởng chính mình."
    },
    {
        "advice": "Mạng xã hội chỉ là một lát cắt rực rỡ được chọn lọc kỹ càng, không phải là toàn bộ bức tranh cuộc sống của bất kỳ ai. Đừng lấy những giọt mồ hôi sau màn hình của mình ra so sánh với ánh hào quang ảo ảnh của người khác.",
        "proverb": "✨ Tục ngữ Việt Nam: \"Sông sâu tĩnh lặng, lúa chín cúi đầu\" – Bình thản sống cuộc đời của chính mình."
    },
    {
        "advice": "Điểm số thấp hay một lần vấp ngã chỉ là một nốt trầm trong bản nhạc thanh xuân, tuyệt đối không định nghĩa được giới hạn hay giá trị con người bạn. Ngày mai luôn là một tờ giấy trắng để bạn viết tiếp những điều tuyệt vời.",
        "proverb": "✨ Danh ngôn cuộc sống: \"Sau cơn mưa trời lại sáng\" – Luôn giữ vững niềm tin vào ngày mai."
    },
    {
        "advice": "Khi áp lực quá lớn khiến bạn thấy ngộp thở, hãy học cách buông bỏ kỳ vọng hoàn hảo xuống một nhịp. Hít một hơi thật sâu, uống một ngụm nước ấm và cho phép bản thân được nghỉ ngơi trọn vẹn trong hôm nay.",
        "proverb": "✨ Thành ngữ Việt Nam: \"Có chí thì nên\" – Chăm chỉ nhưng phải biết yêu thương bản thân."
    },
    {
        "advice": "Đừng cố gắng làm vừa lòng tất cả mọi người xung quanh, bởi vì ngay cả đóa hoa hồng đẹp nhất cũng có người không thích mùi hương của nó. Điều quan trọng nhất là bạn cảm thấy bình yên với những lựa chọn của chính mình.",
        "proverb": "✨ Ca dao Việt Nam: \"Khéo ăn khéo nói sẽ được lòng người, sống chân thành sẽ được bình yên\" – Sống chân thật với chính mình."
    },
    {
        "advice": "Sự so sánh là kẻ cắp đi niềm vui lớn nhất của tuổi trẻ. Thay vì nhìn sang thành công của người khác rồi tự ti, hãy nhìn lại chặng đường dài mà chính bạn đã kiên cường vượt qua từ ngày hôm qua.",
        "proverb": "✨ Danh ngôn: \"Chiến thắng lớn nhất là chiến thắng chính bản thân mình\" – Trân trọng tiến bộ từng ngày."
    },
    {
        "advice": "Những vết rạn và tổn thương trong quá khứ không làm bạn yếu đi, mà chính là nơi ánh sáng hy vọng chiếu vào để tạo nên sự trưởng thành kiên cường của ngày hôm nay.",
        "proverb": "✨ Tục ngữ Việt Nam: \"Lửa thử vàng, gian nan thử sức\" – Bản lĩnh được tôi luyện từ thử thách."
    },
    {
        "advice": "Đừng giấu chặt những giọt nước mắt hay nỗi buồn vào trong lòng. Khóc không có nghĩa là yếu đuối, đó chỉ là cách tâm hồn bạn tự dội rửa những mỏi mệt để nhẹ nhàng bước tiếp.",
        "proverb": "✨ Ca dao Việt Nam: \"Đêm tháng năm chưa nằm đã sáng, ngày tháng mười chưa cười đã tối\" – Mọi chuyện buồn rồi cũng sẽ qua đi."
    },
    {
        "advice": "Thanh xuân không phải là cuộc đua xem ai về đích trước, mà là hành trình trải nghiệm, vấp ngã và tự đứng dậy bằng đôi chân của chính mình. Hãy tận hưởng từng khoảnh khắc theo cách riêng của bạn.",
        "proverb": "✨ Tục ngữ Việt Nam: \"Có công mài sắt, có ngày nên kim\" – Kiên trì rồi sẽ hái quả ngọt."
    },
    {
        "advice": "Khi cảm thấy cô đơn giữa đám đông náo nhiệt, hãy nhớ rằng bạn luôn có một góc nhỏ bình yên trong tâm hồn để quay về. Trân trọng chính mình là khởi đầu của mọi tình yêu thương chân thành.",
        "proverb": "✨ Danh ngôn: \"Hãy là chính mình, bởi tất cả những người khác đã có chủ\" – Tự tin vào giá trị bản thân."
    },
    {
        "advice": "Thành công không có một công thức chung cố định cho tất cả mọi người. Con đường bạn đang đi có thể gập ghềnh hơn, nhưng nó là con đường chân chính được dệt nên bằng chính mồ hôi và sự tử tế của bạn.",
        "proverb": "✨ Ca dao Việt Nam: \"Trăm hay không bằng tay quen\" – Chăm chỉ thực hành sẽ tạo nên kỳ tích."
    },
    {
        "advice": "Đừng để những lời nói vô tình hay sự phán xét bề ngoài của người khác làm lung lay ý chí của bạn. Họ chỉ nhìn thấy bề nổi của tảng băng, còn bạn mới là người thấu hiểu trọn vẹn nỗ lực của chính mình.",
        "proverb": "✨ Tục ngữ Việt Nam: \"Cây thẳng không sợ chết đứng\" – Hiên ngang vững bước giữa đời."
    },
    {
        "advice": "Sức khỏe tinh thần cũng quan trọng không kém gì điểm số trên lớp. Hôm nay nếu quá mệt mỏi, hãy đóng lại sách vở sớm hơn một chút, ngủ một giấc thật sâu để nạp lại nguồn năng lượng tích cực.",
        "proverb": "✨ Danh ngôn: \"Sức khỏe là tài sản quý giá nhất\" – Yêu chiều bản thân để bền bỉ vươn xa."
    },
    {
        "advice": "Mỗi một ngày trôi qua, dù nhỏ bé đến đâu, bạn cũng đã học thêm được một bài học mới. Đừng xem nhẹ những bước tiến chậm rãi, bởi vì rùa đi chậm nhưng vẫn tới đích an toàn.",
        "proverb": "✨ Tục ngữ Việt Nam: \"Kiến tha lâu cũng đầy tổ\" – Tích tiểu thành đại, kiên trì ắt thành công."
    },
    {
        "advice": "Sự kỳ vọng của gia đình và thầy cô là động lực, nhưng đừng để nó biến thành chiếc vòng kim cô trói buộc tuổi trẻ. Hãy sống hết mình với đam mê và năng lực thực sự của bản thân.",
        "proverb": "✨ Ca dao Việt Nam: \"Uống nước nhớ nguồn\" – Hiểu thấu lòng người để sống trọn vẹn yêu thương."
    },
    {
        "advice": "Đừng sợ hãi những lời chê bai, bởi đó chính là những viên sỏi thô ráp giúp bạn mài giũa bản thân trở nên sắc bén và kiên cường hơn trên hành trình trưởng thành.",
        "proverb": "✨ Tục ngữ Việt Nam: \"Đi một ngày đàng, học một sàng khôn\" – Thử thách mở rộng tầm nhìn."
    },
    {
        "advice": "Khi lòng bạn tĩnh lặng, mọi giông bão ngoài kia tự khắc sẽ hóa nhẹ nhàng. Hãy học cách hít thở sâu và mỉm cười với chính mình trước mỗi thử thách lớn nhỏ trong học tập.",
        "proverb": "✨ Ca dao Việt Nam: \"Chớ buồn trước cảnh éo le\" – Giữ tâm sáng để vượt qua nghịch cảnh."
    },
    {
        "advice": "Sự hoàn hảo là một chiếc bẫy tinh vi khiến bạn mãi mãi mệt mỏi. Hãy hướng tới sự tiến bộ qua từng ngày thay vì tự ép mình phải không bao giờ được phép mắc sai lầm.",
        "proverb": "✨ Danh ngôn: \"Không có sự hoàn hảo, chỉ có sự nỗ lực chân thành\" – Chấp nhận và hoàn thiện bản thân."
    },
    {
        "advice": "Một nụ cười vào buổi sáng có thể xua tan đi một phần áp lực đè nặng trong lòng. Hãy mở cửa sổ đón ánh nắng ban mai và nhắc nhở bản thân rằng bạn xứng đáng được hạnh phúc.",
        "proverb": "✨ Tục ngữ Việt Nam: \"Một nụ cười bằng mười thang thuốc bổ\" – Giữ tinh thần lạc quan yêu đời."
    },
    {
        "advice": "Đừng quên gửi một lời cảm ơn đến chính cơ thể và tâm trí của bạn, vì dẫu có những ngày bão giông mệt mỏi nhất, chúng vẫn kiên cường đồng hành cùng bạn vượt qua.",
        "proverb": "✨ Ca dao Việt Nam: \"Ăn quả nhớ kẻ trồng cây\" – Biết ơn chính sức lao động của mình."
    },
    {
        "advice": "Sự đố kỵ hay ganh đua độc hại chỉ làm hao mòn năng lượng quý giá của tuổi trẻ. Hãy dùng thời gian đó để vun đắp cho khu vườn tri thức và ước mơ của riêng bạn.",
        "proverb": "✨ Tục ngữ Việt Nam: \"Học thầy không tày học bạn\" – Cùng nhau tiến bộ trong văn minh."
    },
    {
        "advice": "Có những ngày bạn chỉ cần làm một người bình thường, không cần phải xuất sắc nhất phòng thi, không cần phải rực rỡ nhất đám đông. Được sống an yên và chân thật đã là một điều tuyệt vời rồi.",
        "proverb": "✨ Danh ngôn: \"Bình yên ở trong tâm\" – Tìm thấy sự an nhiên từ nội tại."
    },
    {
        "advice": "Mỗi một bài toán khó, mỗi một trang sách dày đều đang bồi đắp cho trí tuệ và bản lĩnh của bạn ngày mai. Đừng nản lòng trước những trang sách đầu tiên còn nhiều bỡ ngỡ.",
        "proverb": "✨ Tục ngữ Việt Nam: \"Học hành vất vả kết quả ngọt bùi\" – Tri thức là hành trang vững chắc nhất."
    },
    {
        "advice": "Khi bạn cảm thấy lạc lối giữa ngã ba đường của tương lai, hãy dừng lại lắng nghe tiếng nói sâu thẳm bên trong trái tim mình. Nơi đó luôn biết rõ điều gì thực sự làm bạn cảm thấy thuộc về.",
        "proverb": "✨ Ca dao Việt Nam: \"Lòng ta ta cứ giữ bền\" – Kiên định với ước mơ và hướng đi của mình."
    },
    {
        "advice": "Sự đồng cảm và sẻ chia chính là chiếc cầu nối xóa nhòa mọi khoảng cách áp lực. Đừng ngần ngại mở lời tâm sự với một người bạn tin tưởng khi gánh nặng quá sức chịu đựng.",
        "proverb": "✨ Tục ngữ Việt Nam: \"Một cây làm chẳng nên non, ba cây chụm lại nên hòn núi cao\" – Sức mạnh của sự đoàn kết và sẻ chia."
    },
    {
        "advice": "Đừng bao giờ đánh đổi nụ cười và sức khỏe của mình chỉ để đổi lấy những lời ca tụng sáo rỗng từ người khác. Hạnh phúc chân thật bắt nguồn từ sự bình yên trong tâm hồn bạn.",
        "proverb": "✨ Danh ngôn: \"Hạnh phúc không phải là điểm đến mà là cách chúng ta hành trình\" – Trân trọng hiện tại."
    },
    {
        "advice": "Những áp lực học đường hôm nay rồi sẽ trở thành những kỷ niệm đẹp đẽ khi bạn nhìn lại trong tương lai. Hãy mỉm cười vì bạn đã sống một tuổi trẻ đầy nhiệt huyết và dấn thân.",
        "proverb": "✨ Ca dao Việt Nam: \"Gian nan rèn luyện mới thành tài\" – Thử thách tôi luyện bản lĩnh thanh xuân."
    },
    {
        "advice": "Không có đóa hoa nào nở hoài không tàn, cũng không có cơn mưa nào kéo dài mãi mãi. Sau những ngày tháng ôn thi căng thẳng sẽ là khoảng thời gian rực rỡ để bạn hái quả ngọt.",
        "proverb": "✨ Tục ngữ Việt Nam: \"Hết cơn bỉ cực đến hồi thái lai\" – Khổ tận cam lai, bình yên sẽ đến."
    },
    {
        "advice": "Bạn không cần phải hoàn hảo để trở nên tuyệt vời trong mắt người khác. Chính sự chân thành, nỗ lực mộc mạc và trái tim biết ơn của bạn mới là điều tỏa sáng nhất.",
        "proverb": "✨ Danh ngôn: \"Sự chân thành là thứ ngôn ngữ chạm đến trái tim nhanh nhất\" – Sống đẹp từ những điều giản dị."
    },
    {
        "advice": "Hãy tự ôm lấy chính mình sau một ngày dài mệt mỏi và thì thầm rằng: 'Mình đã làm rất tốt rồi!'. Bạn xứng đáng nhận được sự dịu dàng và yêu thương từ chính bản thân mình trước tiên.",
        "proverb": "✨ Ca dao Việt Nam: \"Thương người như thể thương thân\" – Yêu thương và thấu cảm với chính bản thân mình."
    }
]

def render_home_page(user):
    """Hiển thị giao diện Trang chủ"""
    # 1. Hero Card chào mừng cá nhân hóa (Ảnh 3)
    streak = user.get("streak_count", 1)
    
    st.markdown(f"""
    <div class="pink-hero-card">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 15px;">
            <div>
                <h1 style="color: #ff3366; font-size: 32px; margin: 0 0 8px 0;">
                    Xin chào, {user['full_name']}! 👋
                </h1>
                <p style="font-size: 16px; color: #374151; margin-top: 6px; line-height: 1.6;">
                    Chào mừng bạn đến với YouthMind – Không gian an toàn giúp bạn thấu hiểu và giải tỏa những áp lực trong học tập cũng như cuộc sống hằng ngày.
                </p>
            </div>
            <div class="streak-badge" style="font-size: 16px; padding: 10px 18px;">
                🔥 Chuỗi {streak} Ngày Liên Tiếp
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. Thẻ tóm tắt nhanh trạng thái (Test gần nhất, Tâm trạng, Nhiệm vụ)
    latest_test = db.get_latest_test_result(user["id"])
    today_mood = db.get_today_mood(user["id"])
    todos = db.get_user_todos(user["id"])
    pending_todos = [t for t in todos if not t["is_done"]]

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="custom-card" style="text-align: center; border-bottom: 4px solid #ff4757; min-height: 180px;">
            <div style="font-size: 32px; margin-bottom: 8px;">🧠</div>
            <h3 style="font-size: 19px; color: #ff3366; margin-bottom: 6px;">Áp Lực Gần Nhất</h3>
        """, unsafe_allow_html=True)
        if latest_test:
            p_study = round(latest_test["score_study"])
            p_social = round(latest_test["score_social"])
            st.markdown(f"""
            <p style="font-size: 15px; margin: 4px 0;">Học tập: <b style="color: #2ed573;">{p_study}%</b> | MXH: <b style="color: #9b59b6;">{p_social}%</b></p>
            <p style="font-size: 13px; color: #6b7280;">Ngày đo: {latest_test['created_at'][:10]}</p>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <p style="font-size: 14px; color: #6b7280;">Chưa thực hiện bài kiểm tra nào.</p>
            <p style="font-size: 13px; color: #ff4757; font-weight: bold;">👉 Hãy làm test ngay!</p>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="custom-card" style="text-align: center; border-bottom: 4px solid #2ed573; min-height: 180px;">
            <div style="font-size: 32px; margin-bottom: 8px;">😊</div>
            <h3 style="font-size: 19px; color: #10b981; margin-bottom: 6px;">Tâm Trạng Hôm Nay</h3>
        """, unsafe_allow_html=True)
        if today_mood:
            st.markdown(f"""
            <p style="font-size: 17px; font-weight: bold; color: #15803d; margin: 4px 0;">{today_mood['mood']}</p>
            <p style="font-size: 14px; color: #6b7280;">Năng lượng: {today_mood['energy_level']}/5 ⭐</p>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <p style="font-size: 14px; color: #6b7280;">Bạn chưa điểm danh cảm xúc hôm nay.</p>
            <p style="font-size: 13px; color: #10b981; font-weight: bold;">👉 Vào Dashboard để điểm danh!</p>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="custom-card" style="text-align: center; border-bottom: 4px solid #9b59b6; min-height: 180px;">
            <div style="font-size: 32px; margin-bottom: 8px;">📋</div>
            <h3 style="font-size: 19px; color: #8b5cf6; margin-bottom: 6px;">Việc Cần Làm</h3>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <p style="font-size: 26px; font-weight: bold; color: #7c3aed; margin: 4px 0;">{len(pending_todos)}</p>
        <p style="font-size: 14px; color: #6b7280;">Nhiệm vụ học tập đang chờ</p>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # 3. Lộ trình 5 bước vượt qua áp lực (Cập nhật mô tả chính xác theo yêu cầu)
    st.markdown("""
    <div class="custom-card">
        <h2 style="color: #ff3366; font-size: 24px; text-align: center; margin-bottom: 20px;">
            🌿 Vòng Tròn Hỗ Trợ 5 Bước Vượt Qua Áp Lực Đồng Trang Lứa
        </h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 16px; text-align: center;">
            <div style="background: #fff0f3; padding: 18px 12px; border-radius: 16px; border: 1.5px dashed #ffb3c1;">
                <div style="font-size: 28px; margin-bottom: 6px;">1. 🧠</div>
                <b style="color: #d63384; font-size: 16px;">Làm Bài Test</b>
                <p style="font-size: 13.5px; color: #4b5563; margin-top: 6px;">Nhận diện mức độ áp lực học tập và áp lực mạng xã hội</p>
            </div>
            <div style="background: #f0fdf4; padding: 18px 12px; border-radius: 16px; border: 1.5px dashed #86efac;">
                <div style="font-size: 28px; margin-bottom: 6px;">2. 📊</div>
                <b style="color: #16a34a; font-size: 16px;">Xem Dashboard</b>
                <p style="font-size: 13.5px; color: #4b5563; margin-top: 6px;">Biểu đồ đường & cột trực quan, không số ảo</p>
            </div>
            <div style="background: #faf5ff; padding: 18px 12px; border-radius: 16px; border: 1.5px dashed #d8b4fe;">
                <div style="font-size: 28px; margin-bottom: 6px;">3. 🤖</div>
                <b style="color: #9333ea; font-size: 16px;">Trò Chuyện AI</b>
                <p style="font-size: 13.5px; color: #4b5563; margin-top: 6px;">AI hỗ trợ học tập và khó khăn tâm lí trong học đường</p>
            </div>
            <div style="background: #eff6ff; padding: 18px 12px; border-radius: 16px; border: 1.5px dashed #93c5fd;">
                <div style="font-size: 28px; margin-bottom: 6px;">4. 📖</div>
                <b style="color: #2563eb; font-size: 16px;">Ghi Sổ Theo Dõi</b>
                <p style="font-size: 13.5px; color: #4b5563; margin-top: 6px;">Nhật ký đa sắc màu, bộc bạch cảm xúc</p>
            </div>
            <div style="background: #fffbeb; padding: 18px 12px; border-radius: 16px; border: 1.5px dashed #fde68a;">
                <div style="font-size: 28px; margin-bottom: 6px;">5. 🔄</div>
                <b style="color: #d97706; font-size: 16px;">Test Lại & So Sánh</b>
                <p style="font-size: 13.5px; color: #4b5563; margin-top: 6px;">Theo dõi sự giải tỏa áp lực theo thời gian</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 4. Hộp Thông Điệp Truyền Cảm Hứng & Thành Ngữ (Ảnh 4 - Luân phiên 31 câu theo ngày)
    day_of_month = datetime.now().day  # 1 đến 31
    quote_index = (day_of_month - 1) % len(DAILY_ADVICES_31)
    current_quote = DAILY_ADVICES_31[quote_index]

    st.markdown(f"""
    <div class="custom-card" style="background: linear-gradient(135deg, #fdf2f8 0%, #fff1f2 100%); border-left: 6px solid #ff4757;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <h3 style="color: #be123c; margin: 0; font-size: 20px;">💡 Lời Khuyên Dành Riêng Cho Bạn Hôm Nay:</h3>
            <span style="background: #fce7f3; color: #db2777; padding: 3px 10px; border-radius: 12px; font-size: 13px; font-weight: bold;">
                📅 Ngày {day_of_month} Trong Tháng
            </span>
        </div>
        <p style="font-size: 16.5px; line-height: 1.8; color: #111827; margin: 10px 0 12px 0;">
            <i>"{current_quote['advice']}"</i>
        </p>
        <p style="font-size: 15.5px; color: #9d174d; font-weight: bold; margin-bottom: 0;">
            {current_quote['proverb']}
        </p>
    </div>
    """, unsafe_allow_html=True)

