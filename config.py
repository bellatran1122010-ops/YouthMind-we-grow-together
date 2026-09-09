# -*- coding: utf-8 -*-
"""
Cấu hình giao diện và hằng số hệ thống cho YouthMind
Tông màu: Hồng pastel dịu ngọt, mượt mà, bo tròn, nền hồng pastel, chữ đen, font Times New Roman
"""

# Bảng màu chủ đạo của ứng dụng
THEME_COLORS = {
    "primary": "#ff4757",        # Hồng thắm rạng rỡ
    "primary_hover": "#ff6b81",  # Hồng san hô
    "secondary": "#ff9ff3",      # Hồng phấn mềm
    "light_bg": "#ffeef2",       # Nền hồng pastel dịu ngọt
    "card_bg": "#ffffff",        # Nền thẻ trắng sáng
    "card_border": "#ffd1dc",    # Viền hồng nhạt
    "card_shadow": "rgba(255, 105, 180, 0.12)", # Đổ bóng hồng mịn
    "text_main": "#000000",      # Đen tiêu chuẩn
    "text_muted": "#374151",     # Xám đậm đọc dễ
    "accent_green": "#2ed573",   # Xanh ngọc điểm xuyết
    "accent_purple": "#9b59b6",  # Tím thanh lịch
    "accent_yellow": "#f1c40f",  # Vàng tươi
}

# 8 Màu chữ chuyên biệt cho Sổ theo dõi hằng ngày
JOURNAL_TEXT_COLORS = {
    "Màu đen": "#000000",
    "Màu hồng": "#ff3860",
    "Xanh lá": "#10b981",
    "Xanh dương": "#2563eb",
    "Màu tím": "#8b5cf6",
    "Màu nâu": "#78350f",
    "Màu đỏ": "#dc2626",
    "Màu trắng": "#ffffff",
}

# 8 Nền chủ đạo chuyên biệt cho Sổ theo dõi hằng ngày
JOURNAL_BG_THEMES = {
    "Màu trắng": {
        "bg": "#ffffff",
        "border": "#e2e8f0",
        "label": "Trắng Tinh Khôi",
        "default_text": "#000000"
    },
    "Màu hồng": {
        "bg": "#fff1f2",
        "border": "#fecdd3",
        "label": "Hồng Phấn Ngọt Ngào",
        "default_text": "#000000"
    },
    "Xanh lá": {
        "bg": "#f0fdf4",
        "border": "#bbf7d0",
        "label": "Xanh Lá Dịu Mát",
        "default_text": "#000000"
    },
    "Xanh dương": {
        "bg": "#eff6ff",
        "border": "#bfdbfe",
        "label": "Xanh Dương Yên Bình",
        "default_text": "#000000"
    },
    "Màu tím": {
        "bg": "#faf5ff",
        "border": "#e9d5ff",
        "label": "Tím Mộng Mơ",
        "default_text": "#000000"
    },
    "Màu nâu": {
        "bg": "#fdf8f6",
        "border": "#fed7aa",
        "label": "Nâu Trầm Ấm",
        "default_text": "#000000"
    },
    "Màu đỏ": {
        "bg": "#fef2f2",
        "border": "#fecaca",
        "label": "Đỏ Nhạt Tràn Đầy Năng Lượng",
        "default_text": "#000000"
    },
    "Màu đen": {
        "bg": "#1e293b",
        "border": "#334155",
        "label": "Đêm Trầm Tĩnh (Dark Mode)",
        "default_text": "#f8fafc"
    },
}

# Danh mục thẻ Diễn đàn
FORUM_TAGS = [
    "Tất cả chủ đề",
    "#ÁpLựcHọcTập",
    "#SoSánhBạnBè",
    "#MạngXãHội",
    "#KỳVọngGiaĐình",
    "#GócĐộngLực",
    "#TâmSựThầmKín",
    "#KỹNăngCânBằng"
]

# Chuẩn CSS giao diện toàn cục
APP_CUSTOM_CSS = """
<style>
    /* 1. Nền hồng pastel toàn trang và phông chữ Times New Roman cho văn bản */
    html, body, .stApp {
        background-color: #ffeef2 !important;
        color: #000000 !important;
        font-family: 'Times New Roman', Times, serif;
        font-size: 16px !important;
    }

    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown, .stText, [data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"] span {
        font-family: 'Times New Roman', Times, serif !important;
        color: #000000 !important;
    }

    /* 2. QUAN TRỌNG: Bảo vệ biểu tượng Material Symbols (icon con mắt hiển thị mật khẩu, icon nút) không bị đè font */
    [data-testid="stIconMaterial"], 
    [class*="material-symbols"], 
    [class*="MaterialSymbols"], 
    .material-symbols-rounded,
    .material-symbols-outlined,
    span[data-testid="stIconMaterial"],
    button span[data-testid="stIconMaterial"] {
        font-family: 'Material Symbols Rounded', 'Material Icons', sans-serif !important;
        font-weight: normal !important;
        font-style: normal !important;
        text-transform: none !important;
        letter-spacing: normal !important;
        font-size: 20px !important;
        display: inline-block !important;
        line-height: 1 !important;
    }

    /* 3. SỬA LỖI MÀU SỐ TRONG LỊCH DATEPICKER THÀNH MÀU TRẮNG (Ảnh 3) */
    div[data-baseweb="calendar"], 
    div[data-baseweb="calendar"] * {
        color: #ffffff !important;
    }
    div[data-baseweb="calendar"] [role="gridcell"],
    div[data-baseweb="calendar"] [role="gridcell"] > div,
    div[data-baseweb="calendar"] [role="gridcell"] span,
    div[data-baseweb="calendar"] button,
    div[data-baseweb="popover"] [role="gridcell"] *,
    div[data-baseweb="popover"] [aria-roledescription="calendar"] * {
        color: #ffffff !important;
    }

    /* 4. SỬA LỖI CHỮ TRẮNG TRONG KHUNG CHAT INPUT NỀN ĐEN (Ảnh 4) */
    div[data-testid="stChatInput"] {
        border: 2px solid #ff4757 !important;
        border-radius: 18px !important;
    }
    div[data-testid="stChatInput"] textarea,
    div[data-testid="stChatInput"] input,
    div[data-testid="stChatInputTextArea"] {
        color: #ffffff !important;
        background-color: transparent !important;
        font-family: 'Times New Roman', Times, serif !important;
        font-size: 16px !important;
    }
    div[data-testid="stChatInput"] textarea::placeholder {
        color: #cbd5e1 !important;
    }

    /* 5. SỬA BỘ CHỌN SELECTBOX NỀN TRẮNG, CHỮ ĐEN, VIỀN HỒNG (Ảnh 2) */
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1.5px solid #fbcfe8 !important;
        border-radius: 12px !important;
    }
    div[data-baseweb="select"] span {
        color: #000000 !important;
    }
    div[data-baseweb="select"] svg {
        fill: #ff4757 !important;
    }
    div[data-baseweb="popover"] ul li {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    div[data-baseweb="popover"] ul li:hover {
        background-color: #ffe4e6 !important;
        color: #ff4757 !important;
    }

    /* 6. Quy chuẩn kích thước Heading */
    h1, .stHeading h1 {
        font-size: 34px !important;
        font-weight: 700 !important;
        color: #ff3366 !important;
        margin-bottom: 12px !important;
        letter-spacing: 0.3px;
    }

    h2, .stHeading h2 {
        font-size: 26px !important;
        font-weight: 700 !important;
        color: #e11d48 !important;
        margin-top: 18px !important;
        margin-bottom: 10px !important;
    }

    h3, .stHeading h3 {
        font-size: 21px !important;
        font-weight: 700 !important;
        color: #be123c !important;
    }

    /* 7. Khối thẻ bo tròn (Cards) và viền bóng chuyển màu */
    .custom-card {
        background: #ffffff;
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 20px;
        border: 1.5px solid #ffd1dc;
        box-shadow: 0 8px 24px rgba(255, 105, 180, 0.12);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .custom-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 28px rgba(255, 105, 180, 0.18);
    }

    /* Card nổi bật gradient hồng mềm */
    .pink-hero-card {
        background: linear-gradient(135deg, #fff0f5 0%, #ffe4e6 50%, #ffd1dc 100%);
        border-radius: 24px;
        padding: 28px;
        margin-bottom: 24px;
        border: 2px solid #ffb3c1;
        box-shadow: 0 10px 30px rgba(255, 71, 87, 0.15);
    }

    /* 8. Tùy biến các ô nhập liệu (Inputs & Textarea) */
    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1.5px solid #fbcfe8 !important;
        border-radius: 12px !important;
        font-family: 'Times New Roman', Times, serif !important;
        font-size: 16px !important;
        padding: 10px 14px !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.03) !important;
    }

    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #ff4757 !important;
        box-shadow: 0 0 0 3px rgba(255, 71, 87, 0.2) !important;
    }

    /* 9. Nút bấm (Buttons) với sắc hồng tươi sáng và bo tròn */
    .stButton > button {
        background: linear-gradient(135deg, #ff4757 0%, #ff6b81 100%) !important;
        color: #ffffff !important;
        font-family: 'Times New Roman', Times, serif !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 10px 24px !important;
        box-shadow: 0 5px 15px rgba(255, 71, 87, 0.35) !important;
        transition: all 0.25s ease !important;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #ff6b81 0%, #ff4757 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(255, 71, 87, 0.45) !important;
    }

    /* 10. Top Navbar tùy biến đỉnh cao */
    .top-navbar-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #ffffff;
        padding: 16px 24px;
        border-radius: 20px;
        border: 2px solid #ffd1dc;
        box-shadow: 0 6px 20px rgba(255, 105, 180, 0.12);
        margin-bottom: 20px;
    }

    .streak-badge {
        background: linear-gradient(135deg, #ff9f43, #ee5253);
        color: white;
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 15px;
        box-shadow: 0 4px 10px rgba(238, 82, 83, 0.3);
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }

    /* 11. Tùy biến thanh điều hướng radio buttons thành các tab hồng rõ chữ */
    div[data-testid="stRadio"] > div[role="radiogroup"] {
        display: flex !important;
        flex-wrap: wrap !important;
        gap: 10px !important;
        background: #ffffff;
        padding: 10px 14px;
        border-radius: 18px;
        border: 1.5px solid #ffd1dc;
        box-shadow: 0 4px 14px rgba(255, 105, 180, 0.08);
    }

    div[data-testid="stRadio"] > div[role="radiogroup"] > label {
        background: #fff0f3 !important;
        border: 1.5px solid #fecdd3 !important;
        border-radius: 12px !important;
        padding: 8px 16px !important;
        margin: 0 !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
    }

    div[data-testid="stRadio"] > div[role="radiogroup"] > label:hover {
        background: #ffe4e6 !important;
        border-color: #ff4757 !important;
    }

    div[data-testid="stRadio"] > div[role="radiogroup"] > label[data-checked="true"],
    div[data-testid="stRadio"] > div[role="radiogroup"] > label:has(input:checked) {
        background: linear-gradient(135deg, #ff4757 0%, #ff6b81 100%) !important;
        border-color: #ff4757 !important;
        box-shadow: 0 4px 12px rgba(255, 71, 87, 0.35) !important;
    }

    div[data-testid="stRadio"] > div[role="radiogroup"] > label[data-checked="true"] p,
    div[data-testid="stRadio"] > div[role="radiogroup"] > label:has(input:checked) p {
        color: #ffffff !important;
        font-weight: bold !important;
    }

    div[data-testid="stRadio"] > div[role="radiogroup"] > label p {
        font-size: 15px !important;
        font-weight: 600 !important;
        color: #000000 !important;
        margin: 0 !important;
    }

    div[data-testid="stRadio"] > div[role="radiogroup"] > label > div:first-child {
        display: none !important;
    }

    /* 12. Căn chỉnh thanh cuộn hồng */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #fff0f3;
    }
    ::-webkit-scrollbar-thumb {
        background: #ff8fa3;
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #ff4d6d;
    }

    /* Ẩn bớt viền mặc định Streamlit thừa */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
"""
