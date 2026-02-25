import streamlit as st
import google.generativeai as genai
import time

# 1. Cấu hình trang và chèn CSS Trang trí
st.set_page_config(page_title="LingoAI - Học Đa Ngôn Ngữ", page_icon="🌍", layout="centered")

# CSS Customization cho hiệu ứng Glassmorphism và Dark Mode
st.markdown("""
<style>
    /* Đổi màu nền toàn trang thành dải gradient xanh tím */
    .stApp {
        background: linear-gradient(135deg, #0b132b 0%, #1c2541 50%, #3a506b 100%);
        color: white;
    }
    
    /* Trang trí khung chứa Tab Đăng nhập / Đăng ký */
    div[data-testid="stTabs"] {
        background: rgba(255, 255, 255, 0.05);
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-top: 20px;
    }

    /* Đổi màu chữ của các tab */
    button[data-baseweb="tab"] {
        color: #a1a1aa !important;
        font-size: 1.1rem;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: white !important;
        font-weight: bold;
    }

    /* Chỉnh nút bấm mượt mà hơn */
    .stButton>button {
        background: linear-gradient(90deg, #6a11cb 0%, #2575fc 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(37, 117, 252, 0.4);
    }
    
    /* Chỉnh màu tiêu đề */
    h1, h2, h3, p {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# 2. Xử lý API Key (Nhớ cấu hình trong .streamlit/secrets.toml)
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction="Bạn là gia sư ngôn ngữ AI thân thiện. Hỗ trợ người dùng học ngoại ngữ (Anh, Nhật, Hàn, Việt), giải thích ngữ pháp và sửa lỗi."
    )
except KeyError:
    pass # Bỏ qua lỗi hiển thị nếu chưa nhập key để test UI trước

# Khởi tạo state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'messages' not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Chào bạn! Mình là LingoAI Tutor. Bạn muốn luyện tập ngôn ngữ nào hôm nay?"}]

# 3. Giao diện Đăng nhập / Đăng ký mới
def login_page():
    st.markdown("<h1 style='text-align: center; margin-bottom: 0;'>🌟 LingoAI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8 !important;'>Để ngôn ngữ không còn là trở ngại</p>", unsafe_allow_html=True)
    
    # Khung tabs
    tab1, tab2 = st.tabs(["🔑 Đăng nhập", "✨ Đăng ký"])
    
    with tab1:
        st.markdown("### Mừng bạn trở lại!")
        email = st.text_input("Email của bạn", placeholder)
