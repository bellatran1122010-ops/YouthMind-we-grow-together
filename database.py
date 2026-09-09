# -*- coding: utf-8 -*-
"""
Hệ thống Quản trị Cơ sở dữ liệu SQLite cho Peer Pressure Assistant
Đảm bảo tính toàn vẹn dữ liệu, mã hóa mật khẩu, phân quyền và lưu trữ bảo mật
"""

import sqlite3
import hashlib
import json
import os
from datetime import datetime, date, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), "peer_pressure.db")

def get_connection():
    """Tạo và cấu hình kết nối SQLite"""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password: str) -> str:
    """Mã hóa mật khẩu bằng SHA-256 kèm salt cố định"""
    salt = "peer_pressure_secure_salt_2026"
    return hashlib.sha256((password + salt).encode("utf-8")).hexdigest()

def init_db():
    """Khởi tạo toàn bộ cấu trúc bảng nếu chưa tồn tại"""
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Bảng Người dùng
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        full_name TEXT NOT NULL,
        school TEXT,
        student_class TEXT,
        achievements TEXT,
        streak_count INTEGER DEFAULT 1,
        last_login_date TEXT,
        created_at TEXT
    )
    """)

    # 2. Bảng Kết quả Bài kiểm tra (Roleplay 20 câu, RSES, DASS-21)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS test_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        test_type TEXT NOT NULL,
        score_study REAL DEFAULT 0,
        score_social REAL DEFAULT 0,
        score_general REAL DEFAULT 0,
        subscores_json TEXT,
        detailed_analysis TEXT,
        created_at TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)

    # 3. Bảng Sổ điểm danh tâm trạng
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mood_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        mood TEXT NOT NULL,
        energy_level INTEGER DEFAULT 3,
        note TEXT,
        logged_date TEXT NOT NULL,
        created_at TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)

    # 4. Bảng Thời khóa biểu cá nhân
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS timetables (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        day_of_week TEXT NOT NULL,
        date_str TEXT,
        morning_schedule TEXT,
        afternoon_schedule TEXT,
        notes TEXT,
        updated_at TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)

    # 5. Bảng Việc cần làm (To-Do List)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS todos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        task_text TEXT NOT NULL,
        priority TEXT DEFAULT 'Bình thường',
        is_done INTEGER DEFAULT 0,
        created_at TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)

    # 6. Bảng Sổ theo dõi hằng ngày (Nhật kí Daily)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS daily_journals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        journal_date TEXT NOT NULL,
        title TEXT NOT NULL,
        raw_content TEXT NOT NULL,
        text_color TEXT DEFAULT 'Màu đen',
        bg_color TEXT DEFAULT 'Màu trắng',
        is_bold INTEGER DEFAULT 0,
        is_italic INTEGER DEFAULT 0,
        is_underline INTEGER DEFAULT 0,
        is_highlight INTEGER DEFAULT 0,
        created_at TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)

    # 7. Bảng Kho tài liệu chung (Do host đăng tải)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS public_documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        category TEXT NOT NULL,
        description TEXT,
        file_content_text TEXT,
        file_name TEXT,
        file_size_kb REAL,
        download_count INTEGER DEFAULT 0,
        created_at TEXT
    )
    """)

    # 8. Bảng Tài liệu của bạn (Học sinh tự tải lên ở chế độ Private)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        file_name TEXT NOT NULL,
        file_path TEXT NOT NULL,
        file_type TEXT NOT NULL,
        file_size_kb REAL,
        note TEXT,
        uploaded_at TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)

    # 9. Bảng Diễn đàn học đường (Bài đăng tâm sự)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS forum_posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        is_anonymous INTEGER DEFAULT 0,
        author_name TEXT,
        tag TEXT NOT NULL,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        likes_count INTEGER DEFAULT 0,
        created_at TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)

    # 10. Bảng Thả tim bài viết
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS forum_likes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        created_at TEXT,
        UNIQUE(post_id, user_id),
        FOREIGN KEY (post_id) REFERENCES forum_posts (id),
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)

    # 11. Bảng Bình luận diễn đàn
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS forum_comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        author_name TEXT,
        is_anonymous INTEGER DEFAULT 0,
        content TEXT NOT NULL,
        created_at TEXT,
        FOREIGN KEY (post_id) REFERENCES forum_posts (id),
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)

    # 12. Bảng Tin nhắn riêng tư 1-1
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS private_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender_id INTEGER NOT NULL,
        receiver_id INTEGER NOT NULL,
        message_text TEXT,
        media_path TEXT,
        media_type TEXT,
        is_read INTEGER DEFAULT 0,
        created_at TEXT,
        FOREIGN KEY (sender_id) REFERENCES users (id),
        FOREIGN KEY (receiver_id) REFERENCES users (id)
    )
    """)

    conn.commit()

    # Nạp sẵn tài liệu chung chất lượng cao nếu bảng trống
    seed_public_documents(conn)

    conn.close()

def seed_public_documents(conn):
    """Nạp sẵn bộ tài liệu tâm lý học & kỹ năng học tập chuẩn từ nghiên cứu khoa học"""
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as cnt FROM public_documents")
    if cursor.fetchone()["cnt"] == 0:
        docs = [
            (
                "Cẩm Nang Giải Mã Và Vượt Qua Áp Lực So Sánh Đồng Lứa (Peer Comparison)",
                "Tâm Lý Học Đường",
                "Phân tích bản chất của bẫy so sánh 24/7 trên mạng xã hội và phương pháp chuyển dịch từ 'So sánh ngang' sang 'So sánh dọc' với chính mình.",
                """# CẨM NANG VƯỢT QUA ÁP LỰC ĐỒNG LỨA (PEER PRESSURE)
## 1. Bản chất áp lực đồng trang lứa thời đại số
Trong thế giới số hiện nay, mạng xã hội tạo ra ảo tưởng về một cuộc sống hoàn hảo không tì vết. Bạn thấy điểm 10, chứng chỉ ngoại ngữ, giải thưởng của bạn bè xuất hiện liên tục.
Tuy nhiên, đó chỉ là 'Lát cắt đẹp nhất' (Highlight Reel) chứ không phản ánh toàn bộ khó khăn phía sau.

## 2. Công thức chuyển dịch tư duy:
- Chuyển từ 'So sánh ngang': So bì thành tích của mình với người khác.
- Sang 'So sánh dọc': Đo lường sự tiến bộ của bản thân so với chính mình ngày hôm qua (chỉ cần tiến bộ 1% mỗi ngày).

## 3. Ba hành động tức thì khi thấy áp lực:
1. Dừng lướt mạng xã hội: Thực hiện quy tắc 10 phút Digital Detox khi cảm thấy tim đập nhanh hoặc tự ti.
2. Viết ra 3 điều bạn đã nỗ lực làm tốt trong tuần qua.
3. Nhớ rằng: Tốc độ phát triển của mỗi cá nhân là một đường chạy độc bản, không phải cuộc đua cùng vạch xuất phát.""",
                "cam_nang_peer_pressure.md",
                14.5,
                0,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ),
            (
                "Phương Pháp Quản Trị Thời Gian Pomodoro & Ma Trận Eisenhower Cho Học Sinh THPT",
                "Kỹ Năng Học Tập",
                "Bí kíp học sâu, tập trung cao độ, hạn chế kiệt sức (Burnout) và sắp xếp bài tập theo thứ tự ưu tiên khoa học.",
                """# CHIẾN LƯỢC HỌC TẬP THÔNG MINH - HẠN CHẾ KIỆT SỨC
## 1. Phương pháp Pomodoro cải tiến:
- 25 phút học tập tập trung 100% (không điện thoại, không thông báo).
- 5 phút nghỉ ngơi vận động nhẹ hoặc uống nước.
- Sau 4 chu kỳ: Nghỉ dài 15-20 phút.

## 2. Ma trận Eisenhower trong xử lý bài tập:
- Nhóm 1 (Khẩn cấp & Quan trọng): Bài tập nộp ngày mai, ôn thi kỳ thi sắp tới -> Làm ngay lập tức.
- Nhóm 2 (Không khẩn cấp nhưng Quan trọng): Ôn luyện kiến thức dài hạn, đọc sách, rèn luyện sức khỏe -> Lên lịch cố định.
- Nhóm 3 (Khẩn cấp nhưng Không quan trọng): Các cuộc gọi, tin nhắn phiền nhiễu -> Ủy quyền hoặc giải quyết nhanh.
- Nhóm 4 (Không khẩn cấp & Không quan trọng): Lướt mạng xã hội vô thức -> Giảm thiểu tối đa.""",
                "quan_ly_thoi_gian_eisenhower.md",
                12.0,
                0,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ),
            (
                "Bài Tập Tinh Thần: Kỹ Thuật Hít Thở 4-7-8 & Neo Cảm Xúc Giảm Lo Âu Trước Kỳ Thi",
                "Thực Hành Tinh Thần",
                "Hướng dẫn từng bước thực hành kỹ thuật thở 4-7-8 và phương pháp nhận diện 5 giác quan (Grounding 5-4-3-2-1) để cắt cơn hoảng loạn tức thì.",
                """# BÀI TẬP TINH THẦN GIẢM CĂNG THẲNG TỨC THÌ
## 1. Kỹ thuật thở 4-7-8 (Tiến sĩ Andrew Weil):
- Bước 1: Thở hết không khí trong phổi ra bằng miệng.
- Bước 2: Hít vào nhẹ nhàng bằng mũi trong 4 giây.
- Bước 3: Giữ hơi thở sâu trong 7 giây.
- Bước 4: Thở ra từ từ bằng miệng phát ra tiếng gió trong 8 giây.
- Lặp lại chu kỳ 4 lần để kích hoạt hệ thần kinh phó giao cảm, làm dịu nhịp tim và xoa dịu bộ não.

## 2. Kỹ thuật neo tâm 5-4-3-2-1 khi bị choáng ngợp:
- 5 vật bạn nhìn thấy xung quanh.
- 4 vật bạn có thể chạm vào.
- 3 âm thanh bạn nghe thấy.
- 2 mùi bạn có thể ngửi.
- 1 điều tốt đẹp bạn thầm cảm ơn về chính mình.""",
                "bai_tap_tho_4_7_8.md",
                10.2,
                0,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ),
            (
                "Tái Cấu Trúc Nhận Thức (Cognitive Reframing) Về 'Kỳ Vọng Bố Mẹ' Và 'Điểm Số'",
                "Tâm Lý Học Đường",
                "Cách đối thoại hòa nhã với gia đình, tách biệt giá trị cá nhân khỏi điểm số bài thi để bảo vệ sức khỏe tâm thần.",
                """# TÁI CẤU TRÚC NHẬN THỨC VỀ KỲ VỌNG VÀ ĐIỂM SỐ
## 1. Điểm số là một 'Thước đo tiến độ', không phải 'Bản án nhân cách'
Điểm kiểm tra phản ánh sự hiểu bài của một thời điểm cụ thể, nó không đo được lòng nhân ái, sự kiên trì, khả năng sáng tạo hay tương lai của bạn.

## 2. Cách đối thoại với kỳ vọng của cha mẹ:
- Lắng nghe sự lo lắng ẩn sau lời thúc giục: Cha mẹ thường lo sợ con cái vất vả trong tương lai.
- Trình bày kế hoạch rõ ràng: Thay vì cãi lại, hãy cho cha mẹ thấy thời gian biểu và mục tiêu cụ thể bạn đang thực hiện.
- Học cách nói: 'Con cảm ơn sự quan tâm của bố mẹ, con đang nỗ lực hết sức và cũng cần một khoảng nghỉ để tinh thần minh mẫn hơn.'""",
                "tai_cau_truc_nhan_thuc.md",
                11.8,
                0,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        ]
        cursor.executemany("""
        INSERT INTO public_documents (title, category, description, file_content_text, file_name, file_size_kb, download_count, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, docs)
        conn.commit()

# ==================== CÁC HÀM XÁC THỰC & NGƯỜI DÙNG ====================

def register_user(username, password, full_name=None, school="", student_class="", achievements=""):
    """Đăng ký tài khoản học sinh mới (chỉ bắt buộc username và password)"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        today_str = date.today().strftime("%Y-%m-%d")
        pwd_hash = hash_password(password)
        actual_name = full_name.strip() if (full_name and full_name.strip()) else username
        cursor.execute("""
        INSERT INTO users (username, password_hash, full_name, school, student_class, achievements, streak_count, last_login_date, created_at)
        VALUES (?, ?, ?, ?, ?, ?, 1, ?, ?)
        """, (username, pwd_hash, actual_name, school or "", student_class or "", achievements or "", today_str, now_str))
        conn.commit()
        user_id = cursor.lastrowid
        
        # Khởi tạo sẵn thời khóa biểu mẫu 7 ngày cho học sinh
        days = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"]
        for d in days:
            cursor.execute("""
            INSERT INTO timetables (user_id, day_of_week, date_str, morning_schedule, afternoon_schedule, notes, updated_at)
            VALUES (?, ?, '', 'Học chính khóa trên lớp', 'Tự học & ôn tập', 'Giữ tinh thần tích cực', ?)
            """, (user_id, d, now_str))
        conn.commit()
        return True, "Đăng ký tài khoản thành công!"
    except sqlite3.IntegrityError:
        return False, "Tên đăng nhập đã tồn tại trên hệ thống. Vui lòng chọn tên khác!"
    except Exception as e:
        return False, f"Đã có lỗi xảy ra: {str(e)}"
    finally:
        conn.close()

def authenticate_user(username, password):
    """Đăng nhập và tự động cập nhật chuỗi đăng nhập (streak)"""
    conn = get_connection()
    cursor = conn.cursor()
    pwd_hash = hash_password(password)
    cursor.execute("SELECT * FROM users WHERE username = ? AND password_hash = ?", (username, pwd_hash))
    user = cursor.fetchone()
    
    if not user:
        conn.close()
        return None, "Sai tên đăng nhập hoặc mật khẩu!"

    user_dict = dict(user)
    today = date.today()
    today_str = today.strftime("%Y-%m-%d")
    last_date_str = user_dict.get("last_login_date")
    current_streak = user_dict.get("streak_count") or 1

    if last_date_str:
        try:
            last_date = datetime.strptime(last_date_str, "%Y-%m-%d").date()
            diff = (today - last_date).days
            if diff == 1:
                # Đăng nhập vào ngày kế tiếp liên tục -> Tăng streak
                current_streak += 1
            elif diff > 1:
                # Bị ngắt quãng -> Reset streak về 1
                current_streak = 1
            # Nếu diff == 0: cùng một ngày, giữ nguyên streak
        except Exception:
            current_streak = 1
    else:
        current_streak = 1

    cursor.execute("""
    UPDATE users SET streak_count = ?, last_login_date = ? WHERE id = ?
    """, (current_streak, today_str, user_dict["id"]))
    conn.commit()
    conn.close()

    user_dict["streak_count"] = current_streak
    user_dict["last_login_date"] = today_str
    return user_dict, "Đăng nhập thành công!"

def get_user_by_id(user_id):
    """Lấy thông tin người dùng theo ID"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None

def get_all_users_except(user_id):
    """Lấy danh sách các học sinh khác để kết bạn / nhắn tin riêng"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, full_name, school, student_class FROM users WHERE id != ? ORDER BY full_name ASC", (user_id,))
    users = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return users

# ==================== KẾT QUẢ BÀI TEST & LỊCH SỬ ====================

def save_test_result(user_id, test_type, score_study, score_social, score_general, subscores_dict, detailed_analysis):
    """Lưu kết quả kiểm tra vào CSDL"""
    conn = get_connection()
    cursor = conn.cursor()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
    INSERT INTO test_results (user_id, test_type, score_study, score_social, score_general, subscores_json, detailed_analysis, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (user_id, test_type, score_study, score_social, score_general, json.dumps(subscores_dict, ensure_ascii=False), detailed_analysis, now_str))
    conn.commit()
    test_id = cursor.lastrowid
    conn.close()
    return test_id

def get_user_test_history(user_id, test_type=None):
    """Lấy lịch sử làm bài test của học sinh (không fake data)"""
    conn = get_connection()
    cursor = conn.cursor()
    if test_type:
        cursor.execute("""
        SELECT * FROM test_results WHERE user_id = ? AND test_type = ? ORDER BY created_at ASC
        """, (user_id, test_type))
    else:
        cursor.execute("""
        SELECT * FROM test_results WHERE user_id = ? ORDER BY created_at ASC
        """, (user_id,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def get_latest_test_result(user_id, test_type=None):
    """Lấy kết quả test mới nhất của học sinh"""
    conn = get_connection()
    cursor = conn.cursor()
    if test_type:
        cursor.execute("""
        SELECT * FROM test_results WHERE user_id = ? AND test_type = ? ORDER BY id DESC LIMIT 1
        """, (user_id, test_type))
    else:
        cursor.execute("""
        SELECT * FROM test_results WHERE user_id = ? ORDER BY id DESC LIMIT 1
        """, (user_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

# ==================== ĐIỂM DANH TÂM TRẠNG ====================

def log_mood(user_id, mood, energy_level, note):
    """Ghi nhận tâm trạng hôm nay"""
    conn = get_connection()
    cursor = conn.cursor()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    today_str = date.today().strftime("%Y-%m-%d")
    
    # Kiểm tra xem hôm nay đã điểm danh chưa, nếu có thì cập nhật
    cursor.execute("SELECT id FROM mood_logs WHERE user_id = ? AND logged_date = ?", (user_id, today_str))
    existing = cursor.fetchone()
    if existing:
        cursor.execute("""
        UPDATE mood_logs SET mood = ?, energy_level = ?, note = ?, created_at = ? WHERE id = ?
        """, (mood, energy_level, note, now_str, existing["id"]))
    else:
        cursor.execute("""
        INSERT INTO mood_logs (user_id, mood, energy_level, note, logged_date, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, mood, energy_level, note, today_str, now_str))
    conn.commit()
    conn.close()

def get_user_mood_history(user_id, limit=30):
    """Lấy lịch sử tâm trạng của học sinh"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM mood_logs WHERE user_id = ? ORDER BY logged_date ASC LIMIT ?
    """, (user_id, limit))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def get_today_mood(user_id):
    """Lấy tâm trạng của ngày hôm nay"""
    conn = get_connection()
    cursor = conn.cursor()
    today_str = date.today().strftime("%Y-%m-%d")
    cursor.execute("SELECT * FROM mood_logs WHERE user_id = ? AND logged_date = ?", (user_id, today_str))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

# ==================== THỜI KHÓA BIỂU & TO-DO ====================

def get_user_timetable(user_id):
    """Lấy toàn bộ lịch học của học sinh"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM timetables WHERE user_id = ? ORDER BY id ASC", (user_id,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def update_timetable_entry(entry_id, morning, afternoon, notes):
    """Cập nhật một mục trong thời khóa biểu"""
    conn = get_connection()
    cursor = conn.cursor()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
    UPDATE timetables SET morning_schedule = ?, afternoon_schedule = ?, notes = ?, updated_at = ? WHERE id = ?
    """, (morning, afternoon, notes, now_str, entry_id))
    conn.commit()
    conn.close()

def get_user_todos(user_id):
    """Lấy danh sách việc cần làm"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM todos WHERE user_id = ? ORDER BY is_done ASC, id DESC", (user_id,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def add_todo(user_id, task_text, priority):
    """Thêm việc cần làm mới"""
    conn = get_connection()
    cursor = conn.cursor()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
    INSERT INTO todos (user_id, task_text, priority, is_done, created_at)
    VALUES (?, ?, ?, 0, ?)
    """, (user_id, task_text, priority, now_str))
    conn.commit()
    conn.close()

def toggle_todo(todo_id, is_done):
    """Đánh dấu hoàn thành hoặc chưa hoàn thành"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE todos SET is_done = ? WHERE id = ?", (1 if is_done else 0, todo_id))
    conn.commit()
    conn.close()

def delete_todo(todo_id):
    """Xóa một việc cần làm"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    conn.commit()
    conn.close()

# ==================== SỔ THEO DÕI HẰNG NGÀY (NHẬT KÍ) ====================

def save_daily_journal(user_id, journal_date, title, raw_content, text_color, bg_color, is_bold, is_italic, is_underline, is_highlight):
    """Lưu trang nhật ký mới"""
    conn = get_connection()
    cursor = conn.cursor()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
    INSERT INTO daily_journals (user_id, journal_date, title, raw_content, text_color, bg_color, is_bold, is_italic, is_underline, is_highlight, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (user_id, journal_date, title, raw_content, text_color, bg_color, 1 if is_bold else 0, 1 if is_italic else 0, 1 if is_underline else 0, 1 if is_highlight else 0, now_str))
    conn.commit()
    conn.close()

def get_user_journals(user_id):
    """Lấy danh sách các trang nhật ký của học sinh"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM daily_journals WHERE user_id = ? ORDER BY journal_date DESC, id DESC", (user_id,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def delete_journal(journal_id, user_id):
    """Xóa một bài nhật ký"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM daily_journals WHERE id = ? AND user_id = ?", (journal_id, user_id))
    conn.commit()
    conn.close()

# ==================== KHO TÀI LIỆU ====================

def get_public_documents():
    """Lấy danh sách tài liệu chung do host chia sẻ"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM public_documents ORDER BY id ASC")
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def increment_public_doc_download(doc_id):
    """Tăng số lượt tải tài liệu"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE public_documents SET download_count = download_count + 1 WHERE id = ?", (doc_id,))
    conn.commit()
    conn.close()

def save_user_document(user_id, title, file_name, file_path, file_type, file_size_kb, note):
    """Lưu thông tin tài liệu cá nhân học sinh tải lên"""
    conn = get_connection()
    cursor = conn.cursor()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
    INSERT INTO user_documents (user_id, title, file_name, file_path, file_type, file_size_kb, note, uploaded_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (user_id, title, file_name, file_path, file_type, file_size_kb, note, now_str))
    conn.commit()
    conn.close()

def get_user_documents(user_id):
    """Lấy danh sách tài liệu riêng tư của học sinh"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_documents WHERE user_id = ? ORDER BY id DESC", (user_id,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def delete_user_document(doc_id, user_id):
    """Xóa tài liệu cá nhân"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT file_path FROM user_documents WHERE id = ? AND user_id = ?", (doc_id, user_id))
    row = cursor.fetchone()
    if row and os.path.exists(row["file_path"]):
        try:
            os.remove(row["file_path"])
        except Exception:
            pass
    cursor.execute("DELETE FROM user_documents WHERE id = ? AND user_id = ?", (doc_id, user_id))
    conn.commit()
    conn.close()

# ==================== DIỄN ĐÀN & NHẮN TIN RIÊNG ====================

def create_forum_post(user_id, is_anonymous, author_name, tag, title, content):
    """Đăng bài tâm sự lên diễn đàn"""
    conn = get_connection()
    cursor = conn.cursor()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
    INSERT INTO forum_posts (user_id, is_anonymous, author_name, tag, title, content, likes_count, created_at)
    VALUES (?, ?, ?, ?, ?, ?, 0, ?)
    """, (user_id, 1 if is_anonymous else 0, author_name, tag, title, content, now_str))
    conn.commit()
    conn.close()

def get_forum_posts(tag_filter=None):
    """Lấy danh sách bài đăng diễn đàn"""
    conn = get_connection()
    cursor = conn.cursor()
    if tag_filter and tag_filter != "Tất cả chủ đề":
        cursor.execute("""
        SELECT * FROM forum_posts WHERE tag = ? ORDER BY id DESC
        """, (tag_filter,))
    else:
        cursor.execute("""
        SELECT * FROM forum_posts ORDER BY id DESC
        """)
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def toggle_like_post(post_id, user_id):
    """Thả tim hoặc bỏ thả tim bài viết"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM forum_likes WHERE post_id = ? AND user_id = ?", (post_id, user_id))
    existing = cursor.fetchone()
    if existing:
        cursor.execute("DELETE FROM forum_likes WHERE id = ?", (existing["id"],))
        cursor.execute("UPDATE forum_posts SET likes_count = MAX(0, likes_count - 1) WHERE id = ?", (post_id,))
    else:
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO forum_likes (post_id, user_id, created_at) VALUES (?, ?, ?)", (post_id, user_id, now_str))
        cursor.execute("UPDATE forum_posts SET likes_count = likes_count + 1 WHERE id = ?", (post_id,))
    conn.commit()
    conn.close()

def add_forum_comment(post_id, user_id, author_name, is_anonymous, content):
    """Thêm bình luận cho bài đăng"""
    conn = get_connection()
    cursor = conn.cursor()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
    INSERT INTO forum_comments (post_id, user_id, author_name, is_anonymous, content, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (post_id, user_id, author_name, 1 if is_anonymous else 0, content, now_str))
    conn.commit()
    conn.close()

def get_post_comments(post_id):
    """Lấy các bình luận của bài viết"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM forum_comments WHERE post_id = ? ORDER BY id ASC", (post_id,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def send_private_message(sender_id, receiver_id, message_text, media_path=None, media_type=None):
    """Gửi tin nhắn riêng 1-1"""
    conn = get_connection()
    cursor = conn.cursor()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
    INSERT INTO private_messages (sender_id, receiver_id, message_text, media_path, media_type, is_read, created_at)
    VALUES (?, ?, ?, ?, ?, 0, ?)
    """, (sender_id, receiver_id, message_text, media_path, media_type, now_str))
    conn.commit()
    conn.close()

def get_conversation_messages(user1_id, user2_id):
    """Lấy cuộc hội thoại giữa 2 học sinh"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM private_messages 
    WHERE (sender_id = ? AND receiver_id = ?) OR (sender_id = ? AND receiver_id = ?)
    ORDER BY id ASC
    """, (user1_id, user2_id, user2_id, user1_id))
    rows = [dict(r) for r in cursor.fetchall()]
    
    # Đánh dấu đã đọc
    cursor.execute("""
    UPDATE private_messages SET is_read = 1 WHERE sender_id = ? AND receiver_id = ?
    """, (user2_id, user1_id))
    conn.commit()
    conn.close()
    return rows

