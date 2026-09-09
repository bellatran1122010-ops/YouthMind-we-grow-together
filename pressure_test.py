# -*- coding: utf-8 -*-
"""
Phân hệ Pressure Test: 3 bài kiểm tra chuyên biệt
1. Test 20 tình huống thực tế (Peer Echoes chuẩn từ file nghiên cứu)
2. Test Rosenberg Self-Esteem Scale (RSES - Đo lòng tự trọng)
3. Test DASS-21 (Đo Trầm cảm, Lo âu, Căng thẳng)
Kèm lịch sử làm bài và so sánh tiến trình.
"""

import streamlit as st
import database as db
import json
import random

FOOD_ICONS = ["🍕", "🍔", "🍟", "🌭", "🍿", "🍗", "🍦", "🍩", "🍪", "🍫", "🧋", "🍜", "🍣", "🥗", "🥪", "🥞", "🧀", "🍇", "🍓", "🍉"]

ROLEPLAY_QUESTIONS = [
    {
        "id": 1, "type": "study",
        "text": "Sắp tới kỳ thi học kỳ quan trọng, bạn nhận ra mình còn rất nhiều kiến thức chưa ôn tập kịp. Bạn sẽ làm gì?",
        "options": [
            {"text": "A. Lên lịch trình ôn cấp tốc, chấp nhận thức khuya dậy sớm để cày bù phần thiếu sót.", "score": 4, "general": 4},
            {"text": "B. Cố gắng giữ bình tĩnh, chọn lọc những phần trọng tâm nhất để học, phần nào khó quá thì tạm gác lại.", "score": 2, "general": 2},
            {"text": "C. Cảm thấy hoảng loạn, lo lắng đến mức không tập trung học được gì và muốn buông xuôi.", "score": 5, "general": 5},
            {"text": "D. Chấp nhận điểm kém lần này, tự nhủ kỳ sau cố gắng chứ không quá áp lực bản thân.", "score": 1, "general": 1}
        ]
    },
    {
        "id": 2, "type": "study",
        "text": "Khi điểm số bài kiểm tra của bạn thấp hơn kỳ vọng của bản thân và gia đình, phản ứng đầu tiên của bạn là gì?",
        "options": [
            {"text": "A. Cảm giác tội lỗi, sợ hãi khi phải đối mặt với bố mẹ và thầy cô.", "score": 4, "general": 4},
            {"text": "B. Buồn bã trong chốc lát nhưng nhanh chóng xem lại bài để tìm lỗi sai và rút kinh nghiệm.", "score": 2, "general": 2},
            {"text": "C. Tự trách móc bản thân kém cỏi, mất tinh thần học tập trong nhiều ngày liên tiếp.", "score": 5, "general": 5},
            {"text": "D. Thờ ơ, coi như không có chuyện gì vì điểm số không phải là tất cả.", "score": 1, "general": 1}
        ]
    },
    {
        "id": 3, "type": "study",
        "text": "Khối lượng bài tập về nhà và dự án ở trường quá lớn khiến bạn không có thời gian nghỉ ngơi. Bạn sẽ xử lý thế nào?",
        "options": [
            {"text": "A. Cố gắng hoàn thành tất cả bằng mọi giá, kể cả hy sinh thời gian ngủ nghỉ và giải trí.", "score": 4, "general": 4},
            {"text": "B. Sắp xếp thời gian theo thứ tự ưu tiên, làm việc nào quan trọng trước, việc nào không gấp thì làm sau hoặc xin gia hạn.", "score": 2, "general": 2},
            {"text": "C. Cảm thấy kiệt sức, bức bối, vừa làm vừa than thở hoặc nổi cáu với những người xung quanh.", "score": 5, "general": 5},
            {"text": "D. Làm qua loa cho xong chuyện để có thời gian nghỉ ngơi, chất lượng bài tập ra sao cũng được.", "score": 1, "general": 1}
        ]
    },
    {
        "id": 4, "type": "social",
        "text": "Khi nghe bạn bè xung quanh bàn tán về việc họ đã luyện thi chứng chỉ quốc tế hoặc đi học thêm rất nhiều nơi, bạn cảm thấy thế nào?",
        "options": [
            {"text": "A. Áp lực nặng nề, cảm thấy bản thân đang bị tụt lại phía sau và phải đăng ký học thêm ngay lập tức.", "score": 5, "general": 5},
            {"text": "B. Coi đó là động lực để bản thân nỗ lực hơn theo đúng kế hoạch riêng của mình.", "score": 2, "general": 2},
            {"text": "C. Cảm thấy tự ti, ghen tỵ và chán nản với năng lực hiện tại của bản thân.", "score": 4, "general": 4},
            {"text": "D. Bình thản vì mỗi người có một định hướng và tốc độ phát triển khác nhau.", "score": 1, "general": 1}
        ]
    },
    {
        "id": 5, "type": "study",
        "text": "Bố mẹ thường xuyên kỳ vọng bạn phải đạt thành tích cao. Phản ứng của bạn khi nghe những lời kỳ vọng này là gì?",
        "options": [
            {"text": "A. Xem đó là trách nhiệm bắt buộc phải hoàn thành để không làm bố mẹ thất vọng.", "score": 4, "general": 4},
            {"text": "B. Lắng nghe, chia sẻ cởi mở với bố mẹ về năng lực thực tế và áp lực mình đang gặp phải.", "score": 2, "general": 2},
            {"text": "C. Cảm thấy ngột ngạt, căng thẳng, chỉ muốn né tránh hoặc cãi lại khi nghe bố mẹ nhắc đến điểm số.", "score": 5, "general": 5},
            {"text": "D. Phớt lờ, làm theo ý mình vì nghĩ rằng điểm số là chuyện của riêng mình.", "score": 1, "general": 1}
        ]
    },
    {
        "id": 6, "type": "social",
        "text": "Trong một giờ học trên lớp, thầy cô gọi lên bảng kiểm tra bài cũ nhưng bạn hoàn toàn không thuộc bài. Bạn sẽ ứng xử ra sao?",
        "options": [
            {"text": "A. Cực kỳ căng thẳng, tim đập nhanh, lắp bắp không nói nên lời và cầu nguyện qua nhanh.", "score": 4, "general": 4},
            {"text": "B. Thành thật nhận lỗi với giáo viên, xin phép được trả lời vào buổi sau hoặc tìm cách gỡ điểm.", "score": 2, "general": 2},
            {"text": "C. Cảm thấy xấu hổ tột cùng, chỉ muốn 'độn thổ' hoặc giả vờ mệt để xin xuống chỗ ngồi.", "score": 5, "general": 5},
            {"text": "D. Bình tĩnh đón nhận, bị điểm kém thì lần sau chuẩn bị kỹ hơn, không quá nặng nề.", "score": 1, "general": 1}
        ]
    },
    {
        "id": 7, "type": "study",
        "text": "Bạn có hay gặp tình trạng mất ngủ, đau đầu hoặc kiệt sức do lo lắng về việc học hành không?",
        "options": [
            {"text": "A. Thường xuyên xảy ra, đặc biệt là trước các kỳ thi lớn.", "score": 4, "general": 4},
            {"text": "B. Thỉnh thoảng có khi dồn dập nhiều việc cùng lúc, nhưng biết cách điều chỉnh lại.", "score": 2, "general": 2},
            {"text": "C. Hầu như lúc nào cũng trong trạng thái mệt mỏi, căng thẳng kéo dài.", "score": 5, "general": 5},
            {"text": "D. Rất ít khi hoặc không bao giờ, tôi luôn ngủ đủ giấc và giữ tinh thần thoải mái.", "score": 1, "general": 1}
        ]
    },
    {
        "id": 8, "type": "study",
        "text": "Khi không hiểu một bài giảng khó trên lớp, bạn thường chọn cách nào?",
        "options": [
            {"text": "A. Giấu dốt vì sợ bị bạn bè chê cười hoặc sợ thầy cô đánh giá kém.", "score": 4, "general": 4},
            {"text": "B. Chủ động hỏi lại thầy cô ngay lúc đó hoặc tìm gặp bạn bè giỏi hơn để được giảng lại.", "score": 2, "general": 2},
            {"text": "C. Bỏ qua luôn phần đó, tự nhủ chắc thi không vào đâu rồi mặc kệ nó.", "score": 1, "general": 1},
            {"text": "D. Lên mạng tự tìm tòi, xem video hướng dẫn cho đến khi hiểu thì thôi.", "score": 2, "general": 2}
        ]
    },
    {
        "id": 9, "type": "study",
        "text": "Thời gian dành cho sở thích cá nhân (xem phim, chơi game, nghe nhạc, thể thao...) của bạn bị ảnh hưởng ra sao bởi việc học?",
        "options": [
            {"text": "A. Cắt giảm hoàn toàn, dành 100% thời gian cho việc học và ôn thi.", "score": 4, "general": 4},
            {"text": "B. Vẫn duy trì nhưng tiết chế lại, coi đó là cách xả stress hiệu quả sau giờ học căng thẳng.", "score": 1, "general": 1},
            {"text": "C. Bị cấm đoán bởi gia đình hoặc bản thân cảm thấy tội lỗi khi chơi vì sợ mất thời gian học.", "score": 5, "general": 5},
            {"text": "D. Vẫn chơi thoải mái, việc học xếp sau nhu cầu giải trí và thư giãn cá nhân.", "score": 1, "general": 1}
        ]
    },
    {
        "id": 10, "type": "study",
        "text": "Nhìn lại chặng đường học tập gần đây, bạn đánh giá mức độ hài lòng và áp lực của mình như thế nào?",
        "options": [
            {"text": "A. Áp lực đè nặng, cảm giác như cái lò xo bị kéo căng hết cỡ và sắp đứt.", "score": 5, "general": 5},
            {"text": "B. Có áp lực nhưng nằm trong tầm kiểm soát, biết cách cân bằng giữa học và nghỉ ngơi.", "score": 2, "general": 2},
            {"text": "C. Mệt mỏi rã rời, chán nản, không tìm thấy niềm vui trong việc đến trường mỗi ngày.", "score": 5, "general": 5},
            {"text": "D. Thư thả, thoải mái, không đặt nặng vấn đề học hành thi cử.", "score": 1, "general": 1}
        ]
    },
    {
        "id": 11, "type": "social",
        "text": "Bạn bè xung quanh thường xuyên so sánh thành tích, ngoại hình hoặc gia cảnh với bạn. Thái độ của bạn là gì?",
        "options": [
            {"text": "A. Cảm thấy tự ái, tổn thương và tìm mọi cách để 'bằng bạn bằng bè'.", "score": 4, "general": 4},
            {"text": "B. Lờ đi những lời so sánh tiêu cực, tập trung vào những giá trị riêng của bản thân.", "score": 1, "general": 1},
            {"text": "C. Cảm thấy tự ti trầm trọng, thu mình lại và ngại giao tiếp với mọi người.", "score": 5, "general": 5},
            {"text": "D. Cười trừ hoặc trêu lại, hoàn toàn không để tâm đến những lời so sánh đó.", "score": 1, "general": 1}
        ]
    },
    {
        "id": 12, "type": "social",
        "text": "Khi tham gia vào một nhóm bạn mới hoặc tập thể lớp, bạn thường có xu hướng gì để được công nhận?",
        "options": [
            {"text": "A. Cố gắng thay đổi bản thân, chiều lòng tất cả mọi người dù đôi khi cảm thấy mệt mỏi.", "score": 4, "general": 4},
            {"text": "B. Thể hiện sự hòa đồng, chân thành và tôn trọng cá tính riêng của mỗi người.", "score": 1, "general": 1},
            {"text": "C. Lo lắng bản thân bị cô lập hoặc nói sai điều gì nên rất ít khi phát biểu hay thể hiện quan điểm.", "score": 4, "general": 4},
            {"text": "D. Sống đúng với cá tính của mình, ai hợp thì chơi, không quan trọng việc phải lấy lòng tất cả.", "score": 1, "general": 1}
        ]
    },
    {
        "id": 13, "type": "social",
        "text": "Bạn có bao giờ cảm thấy áp lực phải mặc đúng xu hướng thời trang hoặc dùng đồ hiệu giống như các bạn khác trong trường không?",
        "options": [
            {"text": "A. Có, cảm thấy tủi thân và áp lực khi mình không có những món đồ đắt tiền như người khác.", "score": 4, "general": 4},
            {"text": "B. Không quan tâm lắm, chỉ chọn trang phục gọn gàng, phù hợp với hoàn cảnh và kinh tế gia đình.", "score": 1, "general": 1},
            {"text": "C. Cố gắng vòi vĩnh bố mẹ mua bằng được dù biết gia đình khó khăn để không bị chê cười.", "score": 5, "general": 5},
            {"text": "D. Thoải mái với phong cách cá nhân, thấy điều đó hoàn toàn bình thường.", "score": 1, "general": 1}
        ]
    },
    {
        "id": 14, "type": "social",
        "text": "Khi lướt mạng xã hội (Facebook, Instagram, TikTok) nhìn thấy hình ảnh thành công, giàu có hay cuộc sống hoàn hảo của người khác, bạn cảm thấy thế nào?",
        "options": [
            {"text": "A. Cảm thấy chạnh lòng, tự ti về cuộc sống bình thường và kém cỏi của mình.", "score": 4, "general": 4},
            {"text": "B. Xem đó là một nội dung giải trí bình thường, hiểu rằng mạng xã hội chỉ khoe những mặt đẹp.", "score": 1, "general": 1},
            {"text": "C. Bị ảnh hưởng tâm trạng nặng nề, đâm ra ghen tỵ và suy nghĩ tiêu cực suốt cả ngày.", "score": 5, "general": 5},
            {"text": "D. Nhanh chóng lướt qua, không quan tâm đến cuộc sống ảo của người khác.", "score": 1, "general": 1}
        ]
    },
    {
        "id": 15, "type": "social",
        "text": "Bạn được giao nhiệm vụ đứng trước đám đông thuyết trình. Cảm xúc và phản ứng của bạn lúc đó là gì?",
        "options": [
            {"text": "A. Lo lắng run rẩy, đứng ngồi không yên, sợ mọi người soi mói và chê cười lỗi sai của mình.", "score": 4, "general": 4},
            {"text": "B. Hơi hồi hộp nhưng chuẩn bị kỹ kịch bản để hoàn thành tốt phần việc của mình.", "score": 2, "general": 2},
            {"text": "C. Hoảng loạn thực sự, tìm mọi cách để từ chối hoặc trốn tránh nhiệm vụ.", "score": 5, "general": 5},
            {"text": "D. Tự tin, xem đây là cơ hội để rèn luyện kỹ năng giao tiếp trước công chúng.", "score": 1, "general": 1}
        ]
    },
    {
        "id": 16, "type": "social",
        "text": "Trong các buổi tụ tập bạn bè, khi mọi người bàn luận về một chủ đề mà bạn không thích hoặc không biết gì, bạn sẽ làm gì?",
        "options": [
            {"text": "A. Cố gắng hùa theo, gật đầu đồng ý cho qua chuyện để không bị coi là lạc lõng.", "score": 3, "general": 3},
            {"text": "B. Thẳng thắn chia sẻ rằng mình chưa biết về chủ đề đó và hào hứng lắng nghe mọi người kể chuyện.", "score": 1, "general": 1},
            {"text": "C. Im lặng, ngồi bấm điện thoại và mong buổi tụ tập mau kết thúc.", "score": 2, "general": 2},
            {"text": "D. Chủ động chuyển hướng sang một chủ đề khác mà mình hứng thú hơn.", "score": 1, "general": 1}
        ]
    },
    {
        "id": 17, "type": "social",
        "text": "Khi vướng phải một tin đồn không đúng sự thật về mình ở trường học, phản ứng của bạn là gì?",
        "options": [
            {"text": "A. Mất ăn mất ngủ, tìm gặp từng người để đính chính và thanh minh cho bằng được.", "score": 4, "general": 4},
            {"text": "B. Bình tĩnh xác minh nguồn tin, chia sẻ rõ ràng với những người thân thiết và bỏ ngoài tai những kẻ ác ý.", "score": 1, "general": 1},
            {"text": "C. Khóc lóc, uất ức, cảm thấy thế giới xung quanh thật tồi tệ và không muốn đến trường nữa.", "score": 5, "general": 5},
            {"text": "D. Kệ họ, 'cây ngay không sợ chết đứng', thời gian sẽ trả lời tất cả.", "score": 1, "general": 1}
        ]
    },
    {
        "id": 18, "type": "social",
        "text": "Bạn có cảm thấy áp lực từ việc phải xây dựng một 'hình ảnh hoàn hảo' trên không gian mạng không?",
        "options": [
            {"text": "A. Có, tôi luôn cân nhắc rất kỹ trước khi đăng ảnh hay viết gì để nhận được nhiều lượt tương tác.", "score": 4, "general": 4},
            {"text": "B. Không quá nặng nề, mạng xã hội chỉ là nơi lưu giữ khoảnh khắc cá nhân.", "score": 1, "general": 1},
            {"text": "C. Cảm thấy mệt mỏi khi phải đóng vai một người luôn vui vẻ, hạnh phúc trên mạng.", "score": 4, "general": 4},
            {"text": "D. Rất ít khi hoặc không bao giờ dùng mạng xã hội để phô trương hình ảnh.", "score": 1, "general": 1}
        ]
    },
    {
        "id": 19, "type": "social",
        "text": "Khi gia đình hoặc họ hàng so sánh thành tích của bạn với 'con nhà người ta' trong các dịp lễ Tết, bạn xử lý thế nào?",
        "options": [
            {"text": "A. Cúi đầu im lặng, cảm thấy nhục nhã và chỉ muốn trốn vào phòng riêng.", "score": 4, "general": 4},
            {"text": "B. Khéo léo cười trừ hoặc chuyển chủ đề sang chuyện khác để xoa dịu bầu không khí.", "score": 1, "general": 1},
            {"text": "C. Tỏ thái độ khó chịu, bực bội ra mặt hoặc cãi lại người lớn.", "score": 3, "general": 3},
            {"text": "D. Thần thái thản nhiên, xem đó là chuyện thường tình của người lớn tuổi mỗi dịp gặp mặt.", "score": 1, "general": 1}
        ]
    },
    {
        "id": 20, "type": "social",
        "text": "Nhìn tổng thể về các mối quan hệ xã hội (bạn bè, gia đình, nhà trường), bạn có cảm thấy mình được là chính mình khi ở bên cạnh họ không?",
        "options": [
            {"text": "A. Rất ít khi, tôi luôn phải giả vờ để làm hài lòng tất cả mọi người xung quanh.", "score": 5, "general": 5},
            {"text": "B. Phần lớn là có, tôi biết điều chỉnh cách ứng xử phù hợp nhưng vẫn giữ được bản sắc cá nhân.", "score": 1, "general": 1},
            {"text": "C. Hoàn toàn không, tôi cảm thấy cô độc và lạc lõng ngay cả khi đứng giữa đám đông.", "score": 5, "general": 5},
            {"text": "D. Chắc chắn là có, tôi luôn sống thật và tự do là chính mình trong mọi hoàn cảnh.", "score": 1, "general": 1}
        ]
    }
]

RSES_QUESTIONS = [
    {"id": 1, "text": "1. Tôi cảm thấy mình là một người có giá trị, ít nhất là ngang bằng với những người khác.", "reverse": False},
    {"id": 2, "text": "2. Tôi có xu hướng cảm thấy mình là một người thất bại.", "reverse": True},
    {"id": 3, "text": "3. Tôi cảm thấy mình có nhiều phẩm chất tốt đẹp.", "reverse": False},
    {"id": 4, "text": "4. Tôi có khả năng hoàn thành mọi việc tốt như hầu hết những người khác.", "reverse": False},
    {"id": 5, "text": "5. Tôi cảm thấy mình không có nhiều điều để tự hào.", "reverse": True},
    {"id": 6, "text": "6. Tôi có thái độ tích cực và thiện cảm đối với bản thân.", "reverse": False},
    {"id": 7, "text": "7. Nhìn chung, tôi cảm thấy hài lòng về con người của mình.", "reverse": False},
    {"id": 8, "text": "8. Tôi ước gì mình có thể tự tôn trọng bản thân mình nhiều hơn.", "reverse": True},
    {"id": 9, "text": "9. Đôi khi tôi cảm thấy mình thật vô dụng và thừa thãi.", "reverse": True},
    {"id": 10, "text": "10. Đôi khi tôi nghĩ mình hoàn toàn chẳng làm nên trò trống gì.", "reverse": True}
]

DASS21_QUESTIONS = [
    {"id": 1, "cat": "Stress", "text": "1. Tôi cảm thấy khó mà thư giãn hoặc thả lỏng được."},
    {"id": 2, "cat": "Anxiety", "text": "2. Tôi cảm thấy khô miệng."},
    {"id": 3, "cat": "Depression", "text": "3. Tôi không hề cảm thấy có bất kỳ cảm xúc tích cực nào."},
    {"id": 4, "cat": "Anxiety", "text": "4. Tôi bị rối loạn nhịp thở (thở gấp, hụt hơi dù không vận động nặng)."},
    {"id": 5, "cat": "Depression", "text": "5. Tôi cảm thấy khó bắt tay vào làm việc gì đó."},
    {"id": 6, "cat": "Stress", "text": "6. Tôi có xu hướng phản ứng thái quá với các tình huống."},
    {"id": 7, "cat": "Anxiety", "text": "7. Tôi bị run rẩy (ví dụ run tay, run chân)."},
    {"id": 8, "cat": "Stress", "text": "8. Tôi cảm thấy mình đang tiêu tốn quá nhiều năng lượng lo lắng vô cớ."},
    {"id": 9, "cat": "Anxiety", "text": "9. Tôi lo lắng về các tình huống có thể làm mình hoảng loạn hoặc biến mình thành trò cười."},
    {"id": 10, "cat": "Depression", "text": "10. Tôi cảm thấy mình chẳng có điều gì để trông đợi ở tương lai."},
    {"id": 11, "cat": "Stress", "text": "11. Tôi thấy mình dễ bị kích động hoặc bồn chồn đứng ngồi không yên."},
    {"id": 12, "cat": "Stress", "text": "12. Tôi cảm thấy khó có thể tĩnh tâm để nghỉ ngơi."},
    {"id": 13, "cat": "Depression", "text": "13. Tôi cảm thấy buồn rầu, chán chường và ủ rũ."},
    {"id": 14, "cat": "Stress", "text": "14. Tôi không thể chịu đựng được việc bị cản trở hoặc ngắt lời khi đang làm việc gì đó."},
    {"id": 15, "cat": "Anxiety", "text": "15. Tôi cảm thấy mình gần như rơi vào trạng thái hoảng loạn."},
    {"id": 16, "cat": "Depression", "text": "16. Tôi không thể cảm thấy hào hứng hay nhiệt tình với bất cứ điều gì."},
    {"id": 17, "cat": "Depression", "text": "17. Tôi cảm thấy mình là người không có giá trị."},
    {"id": 18, "cat": "Stress", "text": "18. Tôi thấy mình khá dễ nổi cáu và chạm nọc."},
    {"id": 19, "cat": "Anxiety", "text": "19. Tôi cảm nhận rõ tiếng tim đập dù không vận động thể lực (tim đập nhanh, lỡ nhịp)."},
    {"id": 20, "cat": "Anxiety", "text": "20. Tôi cảm thấy sợ hãi mà không có lý do rõ ràng."},
    {"id": 21, "cat": "Depression", "text": "21. Tôi cảm thấy cuộc sống hoàn toàn vô nghĩa."}
]

PROVERBS_LIST = [
    "Thành ngữ đúc kết: 'Trèo cao ngã đau' kết hợp 'Biết dừng đúng lúc là khôn ngoan' – Đừng để những tiêu chuẩn hoàn hảo làm phai mờ đi niềm vui khám phá tri thức và sự bình yên thẳm sâu trong tâm hồn bạn.",
    "Ca dao đúc kết: 'Cây ngay không sợ chết đứng' – Hãy luôn giữ vững bản sắc cá nhân, tự tin vào giá trị nguyên bản của chính mình thay vì chạy theo những chiếc bóng ảo trên không gian mạng.",
    "Thành ngữ đúc kết: 'Chớ thấy sóng cả mà ngã tay chèo' – Giữ vững tay lái, tin tưởng vào trực giác và năng lực nội tại, bạn sẽ luôn vượt qua mọi bão giông học đường.",
    "Ca dao đúc kết: 'Học thầy không tày học bạn' – Biết nhìn nhận điểm mạnh của người khác để làm động lực phấn đấu, nhưng đồng thời phải biết thương lấy sức khỏe tinh thần của chính mình."
]

def render_pressure_test_page(user):
    """Hiển thị mục Pressure Test với 3 bài kiểm tra chuyên biệt"""
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h1 style="color: #ff3366; font-size: 32px; margin-bottom: 6px;">🧠 PHÂN HỆ KIỂM TRA ÁP LỰC (PRESSURE TEST)</h1>
        <p style="font-size: 16px; color: #111827; line-height: 1.6;">
            Hệ thống bài kiểm tra tâm lý học đường chuyên sâu: đo lường áp lực học tập, áp lực so sánh mạng xã hội dựa trên phương pháp đóng vai tình huống thực tế, thang đo lòng tự trọng Rosenberg Self-Esteem Scale (RSES), thang đo căng thẳng DASS-21.
        </p>
    </div>
    """, unsafe_allow_html=True)

    test_tab1, test_tab2, test_tab3, test_tab4 = st.tabs([
        "🎯 1. 20 câu tình huống thực tế (Reality situation)",
        "💎 2. Bài kiểm tra thang đo lòng tự trọng Rosenberg Self-Esteem Scale (RSES)",
        "🩺 3. Bài kiểm tra thang đo căng thẳng DASS-21",
        "📈 4. Lịch Sử & So Sánh Tiến Trình"
    ])

    with test_tab1:
        render_roleplay_test(user)

    with test_tab2:
        render_rses_test(user)

    with test_tab3:
        render_dass21_test(user)

    with test_tab4:
        render_test_history_comparison(user)

# ==================== BÀI TEST 1: ROLEPLAY 20 TÌNH HUỐNG ====================

def render_roleplay_test(user):
    st.markdown("""
    <div class="custom-card" style="border-left: 5px solid #ff4757;">
        <h2 style="color: #ff4757; font-size: 24px; margin-top: 0;">✨ 20 Câu Tình Huống Thực Tế (Reality Situation) - Peer Echoes</h2>
        <p style="font-size: 15.5px; line-height: 1.6; color: #111827;">
            Một trải nghiệm tương tác đưa bạn vào các tình huống thực tế thường gặp: từ lịch học thêm dày đặc, áp lực điểm số thi cử đến những bài đăng thành tích trên mạng xã hội.
            Hãy chọn cách ứng xử tự nhiên nhất của bạn để giải mã toàn diện các chỉ số tâm lý!
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Khởi tạo trạng thái phiên làm bài
    if "roleplay_answers" not in st.session_state:
        st.session_state["roleplay_answers"] = {}
    if "roleplay_current_q" not in st.session_state:
        st.session_state["roleplay_current_q"] = 0

    answers = st.session_state["roleplay_answers"]
    completed_count = len(answers)
    total_q = len(ROLEPLAY_QUESTIONS)

    # Thanh tiến độ và biểu tượng bong bóng
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
        <span style="font-size: 16px; font-weight: bold; color: #ff3366;">
            Học sinh: {user['full_name']} | Lớp {user.get('student_class', '')}
        </span>
        <span style="font-size: 16px; font-weight: bold; color: #2ed573;">
            Tiến độ: {completed_count} / {total_q} câu
        </span>
    </div>
    """, unsafe_allow_html=True)

    # Hiển thị lưới 20 bong bóng món ăn
    st.markdown("<p style='font-weight: bold; color: #4b5563; font-size: 15px;'>Danh sách 20 tình huống (Bấm vào biểu tượng để chọn câu hỏi):</p>", unsafe_allow_html=True)
    bubble_cols = st.columns(10)
    bubble_cols_2 = st.columns(10)
    all_cols = bubble_cols + bubble_cols_2

    for i in range(total_q):
        with all_cols[i]:
            icon = FOOD_ICONS[i % len(FOOD_ICONS)]
            is_done = i in answers
            label = f"✔ {i+1}" if is_done else f"{icon} #{i+1}"
            if st.button(label, key=f"bubble_btn_{i}", use_container_width=True):
                st.session_state["roleplay_current_q"] = i
                st.rerun()

    current_idx = st.session_state["roleplay_current_q"]
    q = ROLEPLAY_QUESTIONS[current_idx]

    st.markdown(f"""
    <div class="custom-card" style="margin-top: 20px; border: 2px solid #ffb3c1; background: #fffdfd;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <span style="background: #ffe4e6; color: #e11d48; padding: 4px 12px; border-radius: 12px; font-weight: bold; font-size: 14px;">
                Tình huống #{q['id']} / 20 ({'Áp lực Học tập' if q['type'] == 'study' else 'Áp lực Mạng xã hội'})
            </span>
            <span style="font-size: 26px;">{FOOD_ICONS[current_idx % len(FOOD_ICONS)]}</span>
        </div>
        <h3 style="color: #111827; font-size: 19px; line-height: 1.6; margin-bottom: 16px;">
            {q['text']}
        </h3>
    </div>
    """, unsafe_allow_html=True)

    # Lựa chọn các phương án
    chosen_opt_idx = answers.get(current_idx)
    
    for opt_idx, opt in enumerate(q["options"]):
        is_selected = (chosen_opt_idx == opt_idx)
        btn_type = "primary" if is_selected else "secondary"
        
        # Nút lựa chọn phương án
        prefix = "✅ " if is_selected else "🔘 "
        if st.button(f"{prefix}{opt['text']}", key=f"opt_{current_idx}_{opt_idx}", use_container_width=True):
            answers[current_idx] = opt_idx
            # Tự động nhảy sang câu kế tiếp chưa làm
            for next_i in range(total_q):
                if next_i not in answers:
                    st.session_state["roleplay_current_q"] = next_i
                    break
            st.rerun()

    # Nút điều hướng trước/sau
    nav_c1, nav_c2, nav_c3 = st.columns([1, 2, 1])
    with nav_c1:
        if current_idx > 0:
            if st.button("⬅️ Câu Trước", use_container_width=True):
                st.session_state["roleplay_current_q"] = current_idx - 1
                st.rerun()
    with nav_c3:
        if current_idx < total_q - 1:
            if st.button("Câu Sau ➡️", use_container_width=True):
                st.session_state["roleplay_current_q"] = current_idx + 1
                st.rerun()

    # Nếu đã hoàn thành toàn bộ 20 câu -> Nút nộp bài và xem kết quả
    if completed_count == total_q:
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        st.success("🎉 Bạn đã hoàn thành xuất sắc toàn bộ 20 tình huống!")
        if st.button("📊 NỘP BÀI & GIẢI MÃ KẾT QUẢ TÂM LÝ", use_container_width=True):
            # Tính điểm chuẩn theo tài liệu nghiên cứu
            score_study = 0
            score_social = 0
            score_general = 0

            for q_idx, opt_idx in answers.items():
                q_item = ROLEPLAY_QUESTIONS[q_idx]
                opt_item = q_item["options"][opt_idx]
                if q_item["type"] == "study":
                    score_study += opt_item["score"]
                elif q_item["type"] == "social":
                    score_social += opt_item["score"]
                score_general += opt_item["general"]

            p_study = round((score_study / 50) * 100)
            p_social = round((score_social / 60) * 100)
            p_general = round((score_general / 100) * 100)

            p_study = min(max(p_study, 10), 100)
            p_social = min(max(p_social, 10), 100)
            p_general = min(max(p_general, 10), 100)

            achieve_lower = (user.get("achievements") or "").lower()
            selected_proverb = random.choice(PROVERBS_LIST)

            if any(k in achieve_lower for k in ["giỏi", "xuất sắc", "tiêu biểu", "cán sự", "nhất"]):
                analysis_text = (
                    '<h4 style="color: #15803d; font-size: 18px; margin: 14px 0 6px 0; font-weight: bold;">🌟 Xu hướng tâm lý & Điểm mạnh nổi bật:</h4>\n'
                    f'<p style="font-size: 16px; line-height: 1.8; color: #111827; margin-bottom: 12px;">Dựa trên khảo sát thực nghiệm tại trường {user.get("school", "THPT")}, bạn là học sinh sở hữu tư duy nhận thức sắc bén, tính kỷ luật tự giác cao độ cùng khát vọng khẳng định bản thân mãnh liệt. Nền tảng này giúp bạn luôn có mục tiêu rõ ràng và trách nhiệm lớn đối với tương lai.</p>\n'
                    '<h4 style="color: #b91c1c; font-size: 18px; margin: 14px 0 6px 0; font-weight: bold;">⚠️ Điểm yếu cần khắc phục:</h4>\n'
                    '<p style="font-size: 16px; line-height: 1.8; color: #111827; margin-bottom: 12px;">Tuy nhiên, chính sự cầu toàn thái quá và tâm lý gánh nặng thành tích vô tình biến những kỳ vọng thành áp lực vô hình siết chặt tâm trí. Bạn dễ sa vào cạm bẫy so sánh trực diện với bạn bè xuất sắc xung quanh, dẫn đến trạng thái kiệt sức ngầm (burnout) khi kết quả không tiệm cận sự hoàn hảo.</p>\n'
                    '<h4 style="color: #0369a1; font-size: 18px; margin: 14px 0 6px 0; font-weight: bold;">💡 Lời khuyên định hướng hành động:</h4>\n'
                    '<p style="font-size: 16px; line-height: 1.8; color: #111827; margin-bottom: 12px;">Thành tích học thuật chỉ là một lát cắt, nó không định nghĩa trọn vẹn giá trị con người bạn. Hãy thiết lập ranh giới: học cách chia nhỏ mục tiêu, cho phép bản thân nghỉ ngơi trọn vẹn vào cuối tuần mà không mang cảm giác tội lỗi.</p>'
                )
            else:
                analysis_text = (
                    '<h4 style="color: #15803d; font-size: 18px; margin: 14px 0 6px 0; font-weight: bold;">🌟 Xu hướng tâm lý & Điểm mạnh nổi bật:</h4>\n'
                    f'<p style="font-size: 16px; line-height: 1.8; color: #111827; margin-bottom: 12px;">Kết quả khảo sát phản ánh bạn là hình mẫu của sự cân bằng và tỉnh táo nội tại trong môi trường học đường {user.get("school", "THPT")}. Bạn biết cách tiết chế cảm xúc, bảo vệ khoảng không gian bình yên cho chính mình, giúp bạn hòa nhập mà không bị cuốn theo áp lực thành tích số đông.</p>\n'
                    '<h4 style="color: #b91c1c; font-size: 18px; margin: 14px 0 6px 0; font-weight: bold;">⚠️ Điểm yếu cần khắc phục:</h4>\n'
                    '<p style="font-size: 16px; line-height: 1.8; color: #111827; margin-bottom: 12px;">Đôi khi, xu hướng dĩ hòa vi quý thái quá khiến bạn vô tình kìm nén tiếng nói nội tâm thực sự. Sự e ngại va chạm có thể làm chậm lại quá trình khẳng định chính kiến cá nhân khi đứng trước những quyết định quan trọng.</p>\n'
                    '<h4 style="color: #0369a1; font-size: 18px; margin: 14px 0 6px 0; font-weight: bold;">💡 Lời khuyên định hướng hành động:</h4>\n'
                    '<p style="font-size: 16px; line-height: 1.8; color: #111827; margin-bottom: 12px;">Sự cân bằng là một phẩm chất quý giá. Hãy dũng cảm cất lên tiếng nói độc lập và đừng ngần ngại chia sẻ chân thành với thầy cô và bạn bè thân thiết để bồi đắp thêm sự tự tin.</p>'
                )

            full_detailed_html = (
                f'<div class="analysis-box" style="background: #ffffff; padding: 18px; border-radius: 14px; border: 1.5px solid #bbf7d0; margin-top: 14px;">\n'
                f'{analysis_text}\n'
                f'<div style="background: #fdf2f8; border-left: 5px solid #ec4899; padding: 12px; margin-top: 14px; font-style: italic; color: #831843; border-radius: 0 8px 8px 0; font-size: 15.5px; line-height: 1.7;">\n'
                f'💬 {selected_proverb}\n'
                f'</div>\n'
                f'</div>'
            )

            subscores = {
                "score_study_raw": score_study,
                "score_social_raw": score_social,
                "score_general_raw": score_general,
                "p_study": p_study,
                "p_social": p_social,
                "p_general": p_general,
                "proverb": selected_proverb
            }

            db.save_test_result(
                user_id=user["id"],
                test_type="roleplay_20",
                score_study=p_study,
                score_social=p_social,
                score_general=p_general,
                subscores_dict=subscores,
                detailed_analysis=full_detailed_html
            )

            st.session_state["roleplay_answers"] = {}
            st.session_state["roleplay_last_result"] = {
                "p_study": p_study,
                "p_social": p_social,
                "p_general": p_general,
                "html": full_detailed_html
            }
            st.rerun()

    # Hiển thị kết quả mới nhất nếu có
    if "roleplay_last_result" in st.session_state:
        res = st.session_state["roleplay_last_result"]
        card_content = (
            f'<div class="custom-card" style="margin-top: 30px; border: 2px solid #2ed573; background: #f0fdf4;">\n'
            f'<h2 style="color: #15803d; text-align: center; margin-top: 0;">🎯 BẢN ĐỒ GIẢI MÃ TÂM LÝ HỌC ĐƯỜNG</h2>\n'
            f'<div style="margin-bottom: 15px; font-size: 15.5px;">\n'
            f'<b>Chỉ số Áp lực học tập (Academic Pressure):</b> <span style="color: #2ed573; font-weight: bold; font-size: 18px;">{res["p_study"]}%</span>\n'
            f'<div style="background: #e2e8f0; border-radius: 10px; height: 14px; width: 100%; overflow: hidden; margin-top: 4px;">\n'
            f'<div style="background: #2ed573; height: 100%; width: {res["p_study"]}%;"></div>\n'
            f'</div>\n'
            f'</div>\n'
            f'<div style="margin-bottom: 15px; font-size: 15.5px;">\n'
            f'<b>Chỉ số Áp lực mạng xã hội (Social Media Pressure):</b> <span style="color: #9b59b6; font-weight: bold; font-size: 18px;">{res["p_social"]}%</span>\n'
            f'<div style="background: #e2e8f0; border-radius: 10px; height: 14px; width: 100%; overflow: hidden; margin-top: 4px;">\n'
            f'<div style="background: #9b59b6; height: 100%; width: {res["p_social"]}%;"></div>\n'
            f'</div>\n'
            f'</div>\n'
            f'<div style="margin-bottom: 15px; font-size: 15.5px;">\n'
            f'<b>Tổng mức độ chịu áp lực chung (General Stress Level):</b> <span style="color: #ff4757; font-weight: bold; font-size: 18px;">{res["p_general"]}%</span>\n'
            f'<div style="background: #e2e8f0; border-radius: 10px; height: 14px; width: 100%; overflow: hidden; margin-top: 4px;">\n'
            f'<div style="background: #ff4757; height: 100%; width: {res["p_general"]}%;"></div>\n'
            f'</div>\n'
            f'</div>\n'
            f'<hr style="border: none; border-top: 1px dashed #bbf7d0; margin: 15px 0;">\n'
            f'{res["html"]}\n'
            f'</div>'
        )
        st.markdown(card_content, unsafe_allow_html=True)

# ==================== BÀI TEST 2: ROSENBERG SELF-ESTEEM (RSES) ====================

def render_rses_test(user):
    st.markdown("""
    <div class="custom-card" style="border-left: 5px solid #2563eb;">
        <h2 style="color: #2563eb; font-size: 24px; margin-top: 0;">💎 Thang Đo Lòng Tự Trọng Rosenberg (RSES)</h2>
        <p style="font-size: 15.5px; line-height: 1.6; color: #374151;">
            Thang đo Rosenberg (1965) là công cụ chuẩn hóa quốc tế được sử dụng rộng rãi nhất trong tâm lý học để đo lường mức độ tự tin, 
            sự trân trọng bản thân và khả năng kháng cự trước áp lực so sánh đồng lứa.
        </p>
    </div>
    """, unsafe_allow_html=True)

    options_rses = [
        ("Hoàn toàn không đồng ý", 1),
        ("Không đồng ý", 2),
        ("Đồng ý", 3),
        ("Hoàn toàn đồng ý", 4)
    ]

    rses_answers = {}
    with st.form("rses_form"):
        for q in RSES_QUESTIONS:
            st.markdown(f"<p style='font-size: 16px; font-weight: bold; margin-bottom: 4px;'>{q['text']}</p>", unsafe_allow_html=True)
            choice = st.radio(
                f"Lựa chọn cho câu {q['id']}:",
                [opt[0] for opt in options_rses],
                key=f"rses_radio_{q['id']}",
                horizontal=True,
                label_visibility="collapsed"
            )
            # Lấy điểm tương ứng
            raw_score = next(item[1] for item in options_rses if item[0] == choice)
            rses_answers[q["id"]] = raw_score
            st.markdown("<hr style='border: none; border-top: 1px dotted #e2e8f0; margin: 8px 0;'>", unsafe_allow_html=True)

        submit_rses = st.form_submit_button("📊 TÍNH ĐIỂM LÒNG TỰ TRỌNG RSES", use_container_width=True)

    if submit_rses:
        total_score = 0
        for q in RSES_QUESTIONS:
            val = rses_answers[q["id"]]
            if q["reverse"]:
                # Nghịch biến: 1->4, 2->3, 3->2, 4->1
                total_score += (5 - val)
            else:
                total_score += val

        # Phân loại theo chuẩn RSES (Thang điểm 10-40)
        if total_score < 15:
            level = "Lòng tự trọng Thấp (Low Self-Esteem)"
            color = "#ef4444"
            desc = "Bạn có xu hướng dễ tự ti, cảm thấy mình kém cỏi hơn người khác và chịu ảnh hưởng tiêu cực nặng nề từ các lời nhận xét hoặc bài đăng thành tích trên mạng xã hội. Bạn rất cần học cách ghi nhận điểm mạnh của chính mình."
        elif 15 <= total_score <= 25:
            level = "Lòng tự trọng Trung bình / Ổn định (Normal / Healthy)"
            color = "#10b981"
            desc = "Bạn có cái nhìn khá cân bằng về bản thân. Dù đôi lúc cũng cảm thấy chạnh lòng khi bị so sánh, bạn vẫn nhận thức được giá trị cá nhân và có khả năng điều hòa cảm xúc tốt."
        else:
            level = "Lòng tự trọng Cao & Vững vàng (High Self-Esteem)"
            color = "#2563eb"
            desc = "Bạn rất tự tin vào giá trị độc bản của mình, có bản lĩnh nội tại vững chắc và hiếm khi bị xao động bởi sự so sánh hơn thua với bạn bè đồng trang lứa."

        analysis_html = f"""
        <div style="background: #f8fafc; border-left: 5px solid {color}; padding: 16px; border-radius: 12px; margin-top: 15px;">
            <h3 style="color: {color}; margin-top: 0;">Kết quả RSES: {total_score} / 40 Điểm - {level}</h3>
            <p style="font-size: 15.5px; line-height: 1.7; color: #1e293b;">{desc}</p>
        </div>
        """

        db.save_test_result(
            user_id=user["id"],
            test_type="rses_10",
            score_study=0,
            score_social=0,
            score_general=total_score,
            subscores_dict={"rses_total": total_score, "level": level},
            detailed_analysis=analysis_html
        )

        st.markdown(analysis_html, unsafe_allow_html=True)
        st.success("✅ Đã lưu kết quả bài kiểm tra RSES vào hệ thống!")

# ==================== BÀI TEST 3: DASS-21 ====================

def render_dass21_test(user):
    st.markdown("""
    <div class="custom-card" style="border-left: 5px solid #8b5cf6;">
        <h2 style="color: #8b5cf6; font-size: 24px; margin-top: 0;">🩺 Thang Đo Trầm Cảm - Lo Âu - Căng Thẳng (DASS-21)</h2>
        <p style="font-size: 15.5px; line-height: 1.6; color: #374151;">
            DASS-21 gồm 21 mục đánh giá mức độ trải nghiệm cảm xúc tiêu cực của bạn trong <b>suốt một tuần qua</b>.
            Quy ước điểm: <b>0</b>: Không đúng chút nào | <b>1</b>: Thỉnh thoảng đúng | <b>2</b>: Khá thường xuyên | <b>3</b>: Hoàn toàn đúng / Rất thường xuyên.
        </p>
    </div>
    """, unsafe_allow_html=True)

    dass_answers = {}
    with st.form("dass21_form"):
        for q in DASS21_QUESTIONS:
            st.markdown(f"<p style='font-size: 15.5px; font-weight: bold; margin-bottom: 4px;'>{q['text']}</p>", unsafe_allow_html=True)
            score = st.radio(
                f"Lựa chọn câu {q['id']}:",
                [0, 1, 2, 3],
                format_func=lambda x: {0: "0 - Không đúng chút nào", 1: "1 - Đúng một phần", 2: "2 - Khá thường xuyên", 3: "3 - Rất thường xuyên"}[x],
                key=f"dass_radio_{q['id']}",
                horizontal=True,
                label_visibility="collapsed"
            )
            dass_answers[q["id"]] = score
            st.markdown("<hr style='border: none; border-top: 1px dotted #e2e8f0; margin: 6px 0;'>", unsafe_allow_html=True)

        submit_dass = st.form_submit_button("📊 PHÂN TÍCH SỨC KHỎE TÂM LÝ DASS-21", use_container_width=True)

    if submit_dass:
        dep_score = sum(dass_answers[q["id"]] for q in DASS21_QUESTIONS if q["cat"] == "Depression") * 2
        anx_score = sum(dass_answers[q["id"]] for q in DASS21_QUESTIONS if q["cat"] == "Anxiety") * 2
        str_score = sum(dass_answers[q["id"]] for q in DASS21_QUESTIONS if q["cat"] == "Stress") * 2

        # Phân độ Trầm cảm
        if dep_score <= 9: dep_lvl = "Bình thường"
        elif dep_score <= 13: dep_lvl = "Nhẹ"
        elif dep_score <= 20: dep_lvl = "Vừa"
        elif dep_score <= 27: dep_lvl = "Nặng"
        else: dep_lvl = "Rất nặng"

        # Phân độ Lo âu
        if anx_score <= 7: anx_lvl = "Bình thường"
        elif anx_score <= 9: anx_lvl = "Nhẹ"
        elif anx_score <= 14: anx_lvl = "Vừa"
        elif anx_score <= 19: anx_lvl = "Nặng"
        else: anx_lvl = "Rất nặng"

        # Phân độ Căng thẳng
        if str_score <= 14: str_lvl = "Bình thường"
        elif str_score <= 18: str_lvl = "Nhẹ"
        elif str_score <= 25: str_lvl = "Vừa"
        elif str_score <= 33: str_lvl = "Nặng"
        else: str_lvl = "Rất nặng"

        analysis_html = f"""
        <div style="background: #faf5ff; border: 2px solid #d8b4fe; padding: 20px; border-radius: 16px; margin-top: 15px;">
            <h3 style="color: #7c3aed; margin-top: 0;">Bảng Đánh Giá Mức Độ DASS-21 Của Bạn:</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; text-align: center; margin: 15px 0;">
                <div style="background: #ffffff; padding: 12px; border-radius: 12px; border: 1.5px solid #fbcfe8;">
                    <b style="color: #e11d48; font-size: 16px;">Trầm Cảm (Depression)</b>
                    <p style="font-size: 24px; font-weight: bold; margin: 6px 0; color: #be123c;">{dep_score}</p>
                    <span style="font-weight: bold; color: #4b5563;">{dep_lvl}</span>
                </div>
                <div style="background: #ffffff; padding: 12px; border-radius: 12px; border: 1.5px solid #bfdbfe;">
                    <b style="color: #2563eb; font-size: 16px;">Lo Âu (Anxiety)</b>
                    <p style="font-size: 24px; font-weight: bold; margin: 6px 0; color: #1d4ed8;">{anx_score}</p>
                    <span style="font-weight: bold; color: #4b5563;">{anx_lvl}</span>
                </div>
                <div style="background: #ffffff; padding: 12px; border-radius: 12px; border: 1.5px solid #fed7aa;">
                    <b style="color: #ea580c; font-size: 16px;">Căng Thẳng (Stress)</b>
                    <p style="font-size: 24px; font-weight: bold; margin: 6px 0; color: #c2410c;">{str_score}</p>
                    <span style="font-weight: bold; color: #4b5563;">{str_lvl}</span>
                </div>
            </div>
            <p style="font-size: 15px; line-height: 1.6; color: #374151;">
                💡 <b>Khuyến nghị từ trợ lý:</b> Nếu bạn đang ở mức 'Vừa' hoặc 'Nặng' ở bất kỳ chỉ số nào, hãy dành thêm thời gian thực hành kỹ thuật thở 4-7-8, tâm sự cùng Chatbot AI hoặc tìm gặp chuyên viên tư vấn tâm lý học đường tại trường nhé!
            </p>
        </div>
        """

        db.save_test_result(
            user_id=user["id"],
            test_type="dass_21",
            score_study=str_score,
            score_social=anx_score,
            score_general=dep_score,
            subscores_dict={
                "depression_score": dep_score, "depression_level": dep_lvl,
                "anxiety_score": anx_score, "anxiety_level": anx_lvl,
                "stress_score": str_score, "stress_level": str_lvl
            },
            detailed_analysis=analysis_html
        )

        st.markdown(analysis_html, unsafe_allow_html=True)
        st.success("✅ Đã ghi nhận kết quả bài kiểm tra DASS-21 vào hồ sơ sức khỏe tâm lý của bạn!")

# ==================== BẢNG LỊCH SỬ & SO SÁNH TIẾN TRÌNH ====================

def render_test_history_comparison(user):
    st.markdown("""
    <div class="custom-card">
        <h2 style="color: #ff3366; font-size: 24px; margin-top: 0;">📈 Lịch Sử Kiểm Tra & So Sánh Sự Thay Đổi Tâm Lý</h2>
        <p style="font-size: 15.5px; color: #4b5563;">
            Theo dõi sự thay đổi của mức độ áp lực qua các mốc thời gian làm bài test để nhận thấy sự tiến bộ và khả năng thích ứng của bạn.
        </p>
    </div>
    """, unsafe_allow_html=True)

    history = db.get_user_test_history(user["id"])

    if not history:
        st.info("ℹ️ Bạn chưa có dữ liệu bài test nào trong hồ sơ. Hãy hoàn thành ít nhất một bài kiểm tra để kích hoạt tính năng so sánh!")
        return

    # Lọc theo bài test
    filter_type = st.selectbox(
        "Chọn loại bài test muốn xem lại:",
        ["Tất cả bài kiểm tra", "Test tình huống thực tế (20 câu)", "Test Rosenberg (RSES)", "Test DASS-21"]
    )

    type_mapping = {
        "Test tình huống thực tế (20 câu)": "roleplay_20",
        "Test Rosenberg (RSES)": "rses_10",
        "Test DASS-21": "dass_21"
    }

    filtered_history = history
    if filter_type != "Tất cả bài kiểm tra":
        filtered_history = [h for h in history if h["test_type"] == type_mapping[filter_type]]

    if not filtered_history:
        st.warning(f"Chưa có dữ liệu bài test cho mục '{filter_type}'.")
        return

    # Hiển thị bảng so sánh
    st.markdown(f"<h3 style='color: #e11d48;'>📋 Danh Sách Các Lần Đo ({len(filtered_history)} lần):</h3>", unsafe_allow_html=True)
    
    table_data = []
    for idx, item in enumerate(filtered_history):
        t_type = item["test_type"]
        type_name = "20 Tình huống Peer Echoes" if t_type == "roleplay_20" else ("Rosenberg (RSES)" if t_type == "rses_10" else "DASS-21")
        
        table_data.append({
            "Lần đo": f"#{idx+1}",
            "Loại bài test": type_name,
            "Áp lực Học tập": f"{round(item['score_study'])}%" if t_type == "roleplay_20" else "-",
            "Áp lực Mạng xã hội": f"{round(item['score_social'])}%" if t_type == "roleplay_20" else "-",
            "Áp lực Chung / Tổng điểm": f"{round(item['score_general'])}" + ("%" if t_type == "roleplay_20" else " điểm"),
            "Thời gian ghi nhận": item["created_at"]
        })

    st.table(table_data)

    # Nếu có từ 2 lần làm bài roleplay_20 trở lên -> Phân tích so sánh tiến trình
    roleplay_runs = [h for h in filtered_history if h["test_type"] == "roleplay_20"]
    if len(roleplay_runs) >= 2:
        first = roleplay_runs[0]
        latest = roleplay_runs[-1]
        
        diff_study = round(latest["score_study"] - first["score_study"])
        diff_social = round(latest["score_social"] - first["score_social"])
        diff_general = round(latest["score_general"] - first["score_general"])

        st.markdown("""
        <div class="custom-card" style="background: #f0fdf4; border: 2px solid #86efac; margin-top: 20px;">
            <h3 style="color: #16a34a; margin-top: 0;">✨ Đánh Giá Tiến Bộ Giữa Lần Đầu Tiên Và Lần Gần Nhất:</h3>
        """, unsafe_allow_html=True)
        
        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1:
            st.metric("Áp lực Học tập", f"{round(latest['score_study'])}%", f"{diff_study}%", delta_color="inverse")
        with col_s2:
            st.metric("Áp lực Mạng xã hội", f"{round(latest['score_social'])}%", f"{diff_social}%", delta_color="inverse")
        with col_s3:
            st.metric("Áp lực Chung", f"{round(latest['score_general'])}%", f"{diff_general}%", delta_color="inverse")

        if diff_general <= 0:
            st.markdown("<p style='color: #15803d; font-weight: bold; font-size: 15.5px;'>🎉 Rất tuyệt vời! Mức độ áp lực chung của bạn đang có xu hướng giảm bớt. Hãy tiếp tục duy trì những thói quen học tập lành mạnh!</p>", unsafe_allow_html=True)
        else:
            st.markdown("<p style='color: #b91c1c; font-weight: bold; font-size: 15.5px;'>⚠️ Áp lực có dấu hiệu gia tăng so với lần đo đầu tiên. Hãy trò chuyện thêm với Chatbot AI để nhận bài tập thư giãn và chia sẻ cùng thầy cô nhé!</p>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

