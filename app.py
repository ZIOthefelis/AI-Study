import streamlit as st
import google.generativeai as genai
import time

# 1. Cấu hình trang và chèn CSS Trang trí
st.set_page_config(page_title="LingoAI - Học Đa Ngôn Ngữ", page_icon="🌍", layout="centered")

# CSS Customization cho hiệu ứng Glassmorphism và Dark Mode
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0b132b 0%, #1c2541 50%, #3a506b 100%);
        color: white;
    }
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
    button[data-baseweb="tab"] {
        color: #a1a1aa !important;
        font-size: 1.1rem;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: white !important;
        font-weight: bold;
    }
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
    h1, h2, h3, p {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# 2. Xử lý API Key
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction="Bạn là gia sư ngôn ngữ AI thân thiện. Hỗ trợ người dùng học ngoại ngữ (Anh, Nhật, Hàn, Việt), giải thích ngữ pháp và sửa lỗi."
    )
except KeyError:
    pass 

# Khởi tạo state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'messages' not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Chào bạn! Mình là LingoAI Tutor. Bạn muốn luyện tập ngôn ngữ nào hôm nay?"}]

# 3. Giao diện Đăng nhập / Đăng ký
def login_page():
    st.markdown("<h1 style='text-align: center; margin-bottom: 0;'>🌟 LingoAI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8 !important;'>Để ngôn ngữ không còn là trở ngại</p>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔑 Đăng nhập", "✨ Đăng ký"])
    
    with tab1:
        st.markdown("### Mừng bạn trở lại!")
        email = st.text_input("Email của bạn", placeholder="ví dụ: hello@lingoai.com", key="login_email")
        password = st.text_input("Mật khẩu", type="password", placeholder="••••••••", key="login_pass")
        
        st.write("") 
        if st.button("Đăng nhập vào hệ thống", use_container_width=True):
            if email and password: 
                st.session_state.logged_in = True
                st.session_state.user_name = "Học viên" 
                st.rerun()
            else:
                st.error("Vui lòng điền đủ thông tin!")
                
    with tab2:
        st.markdown("### Bắt đầu hành trình mới!")
        new_name = st.text_input("Họ và tên của bạn", placeholder="Tên hiển thị")
        new_email = st.text_input("Email đăng ký", placeholder="ví dụ: hello@lingoai.com")
        new_pass = st.text_input("Mật khẩu mới", type="password", placeholder="••••••••")
        
        st.write("") 
        if st.button("Tạo tài khoản ngay", use_container_width=True):
            st.success("Tạo tài khoản thành công! Hãy chuyển sang tab Đăng nhập.")

# 4. Giao diện App chính
def main_app():
    with st.sidebar:
        st.title(f"Xin chào, {st.session_state.user_name}! 👋")
        st.markdown("**Đang học:** Tiếng Nhật (N3)")
        st.divider()
        if st.button("🚪 Đăng xuất"):
            st.session_state.logged_in = False
            st.rerun()
            
    st.title("🤖 LingoAI Tutor")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Hỏi AI bất kỳ điều gì về ngôn ngữ..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            try:
                chat_history = [{"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]} for m in st.session_state.messages[:-1]]
                chat = model.start_chat(history=chat_history)
                response = chat.send_message(prompt, stream=True)
                
                full_response = ""
                for chunk in response:
                    full_response += chunk.text
                    message_placeholder.markdown(full_response + "▌")
                    time.sleep(0.02)
                message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"Lỗi kết nối AI: {e}")

# QUAN TRỌNG: Đây là đoạn code bị thiếu khiến web không hiện gì
if not st.session_state.logged_in:
    login_page()
else:
    main_app()
