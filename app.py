import streamlit as st
import google.generativeai as genai
import time

# Cấu hình trang
st.set_page_config(page_title="LingoAI - Học Đa Ngôn Ngữ", page_icon="🌍", layout="centered")

# Lấy API Key từ Streamlit Secrets an toàn
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # Khởi tạo model AI với chỉ thị đóng vai giáo viên ngôn ngữ
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction="Bạn là một gia sư ngôn ngữ AI thân thiện, chuyên môn cao. Bạn hỗ trợ người dùng học Tiếng Anh, Tiếng Nhật, Tiếng Hàn và Tiếng Việt. Hãy giải thích ngữ pháp ngắn gọn, dễ hiểu, luôn đưa ra ví dụ thực tế và sửa lỗi sai cho người dùng nếu có."
    )
except KeyError:
    st.error("Chưa cấu hình GEMINI_API_KEY trong Secrets.")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'messages' not in st.session_state:
    # Lời chào mặc định của AI khi mở khung chat
    st.session_state.messages = [{"role": "assistant", "content": "Chào bạn! Mình là LingoAI Tutor. Bạn muốn luyện tập ngôn ngữ nào hôm nay?"}]

def login_page():
    st.title("🌍 LingoAI")
    st.markdown("Nền tảng học Tiếng Nhật, Hàn, Anh & Tiếng Việt tích hợp AI")
    
    tab1, tab2 = st.tabs(["Đăng nhập", "Đăng ký"])
    
    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Mật khẩu", type="password", key="login_pass")
        if st.button("Đăng nhập ngay", type="primary", use_container_width=True):
            if email and password: 
                st.session_state.logged_in = True
                st.session_state.user_name = "Bùi Khánh Hà" 
                st.rerun()
            else:
                st.error("Vui lòng nhập đầy đủ email và mật khẩu!")
                
    with tab2:
        new_name = st.text_input("Họ và tên")
        new_email = st.text_input("Email")
        new_pass = st.text_input("Mật khẩu", type="password")
        if st.button("Tạo tài khoản", use_container_width=True):
            st.success("Đăng ký thành công! Vui lòng chuyển sang tab Đăng nhập.")

def main_app():
    with st.sidebar:
        st.title(f"Xin chào, {st.session_state.user_name}! 👋")
        st.markdown("**Đang học:** Tiếng Nhật (Mục tiêu: N3)")
        st.divider()
        if st.button("🚪 Đăng xuất"):
            st.session_state.logged_in = False
            st.session_state.messages = [{"role": "assistant", "content": "Chào bạn! Mình là LingoAI Tutor. Bạn muốn luyện tập ngôn ngữ nào hôm nay?"}]
            st.rerun()
            
    st.title("🤖 LingoAI Tutor")

    # In ra lịch sử chat
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Nhận câu hỏi mới từ người dùng
    if prompt := st.chat_input("VD: Phân biệt wa và ga trong tiếng Nhật..."):
        # 1. Hiển thị tin nhắn người dùng
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # 2. Gọi API Gemini để lấy câu trả lời
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            try:
                # Gửi toàn bộ lịch sử hội thoại để AI hiểu ngữ cảnh (trừ lời chào đầu nếu cần)
                chat_history = []
                for m in st.session_state.messages[:-1]: # Không lấy câu hỏi hiện tại
                    role = "user" if m["role"] == "user" else "model"
                    chat_history.append({"role": role, "parts": [m["content"]]})
                
                chat = model.start_chat(history=chat_history)
                response = chat.send_message(prompt, stream=True)
                
                full_response = ""
                # Tạo hiệu ứng gõ chữ (stream)
                for chunk in response:
                    full_response += chunk.text
                    message_placeholder.markdown(full_response + "▌")
                    time.sleep(0.02)
                
                message_placeholder.markdown(full_response)
                
                # 3. Lưu câu trả lời thật vào lịch sử
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
            except Exception as e:
                st.error(f"Lỗi kết nối AI: {e}")

if not st.session_state.logged_in:
    login_page()
else:
    main_app()
