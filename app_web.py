import streamlit as st
import streamlit.components.v1 as components
from supabase import create_client, Client
import datetime

st.set_page_config(page_title="Phoning Messenger Real-time", page_icon="💬", layout="wide")

# ==========================================
# KẾT NỐI SUPABASE CỦA BẠN (ĐÃ TỰ ĐỘNG ĐIỀN)
# ==========================================
SUPABASE_URL = "https://eiemsjazzxykzqulnvfz.supabase.co"
SUPABASE_KEY = "sb_publishable__DiTLY0wFBziCsZG..." # (Lưu ý: Nếu key dài quá, bạn thay bằng đoạn Publishable key vừa copy trên Supabase)

@st.cache_resource
def init_connection():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

try:
    supabase: Client = init_connection()
except Exception as e:
    st.error("Chưa kết nối được Database!")
    st.stop()

# ==========================================
# HỆ THỐNG ĐĂNG NHẬP
# ==========================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "user_avatar" not in st.session_state:
    st.session_state.user_avatar = "😎"

if not st.session_state.logged_in:
    st.title("💬 Chào mừng đến với PHONING MESSENGER")
    st.write("Tạo tài khoản nhanh để bắt đầu nhắn tin và gọi video với bạn bè!")
    
    with st.form("login_form"):
        name_input = st.text_input("Nhập tên hiển thị của bạn:")
        avatar_input = st.selectbox("Chọn Avatar:", ["😎", "🐱", "🐶", "🦊", "🐼", "🤖", "👻", "🌸"])
        room_input = st.text_input("Mã phòng chung (Hai người nhập giống nhau để gặp nhau):", value="phong-vip-1")
        submit_login = st.form_submit_button("🚀 Vào phòng ngay")
        
        if submit_login and name_input.strip() != "":
            st.session_state.logged_in = True
            st.session_state.user_name = name_input.strip()
            st.session_state.user_avatar = avatar_input
            st.session_state.room_id = room_input.strip()
            st.rerun()
    st.stop()

# ==========================================
# GIAO DIỆN CHÍNH
# ==========================================
st.sidebar.title("👤 Hồ sơ")
st.sidebar.markdown(f"### {st.session_state.user_avatar} {st.session_state.user_name}")
st.sidebar.info(f"🔑 Mã phòng: **{st.session_state.room_id}**")
if st.sidebar.button("🚪 Đăng xuất"):
    st.session_state.logged_in = False
    st.rerun()

st.title(f"💬 PHONING MESSENGER — Phòng: {st.session_state.room_id}")

col_chat, col_call = st.columns([1.2, 1])

# --- KHUNG CHAT ---
with col_chat:
    st.subheader("📜 Tin nhắn trực tiếp")
    
    @st.fragment(run_every=2)
    def show_messages():
        chat_box = st.container(height=420)
        with chat_box:
            try:
                response = supabase.table("messages").select("*").eq("room_id", st.session_state.room_id).order("id", desc=False).execute()
                msgs = response.data
                if not msgs:
                    st.info("Chưa có tin nhắn nào. Hãy gửi lời chào đầu tiên!")
                for m in msgs:
                    is_me = (m["sender"] == st.session_state.user_name)
                    if is_me:
                        st.markdown(f"<div style='text-align: right; background-color: #0084ff; color: white; padding: 8px 12px; border-radius: 15px; margin: 5px 0; display: inline-block; float: right; clear: both;'><b>Bạn:</b> {m['content']}</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div style='text-align: left; background-color: #3e4042; color: white; padding: 8px 12px; border-radius: 15px; margin: 5px 0; display: inline-block; float: left; clear: both;'>{m['avatar']} <b>{m['sender']}:</b> {m['content']}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.warning("Đang đồng bộ tin nhắn...")

    show_messages()

    with st.form(key="send_msg_form", clear_on_submit=True):
        c1, c2 = st.columns([4, 1])
        with c1:
            msg_text = st.text_input("Nhập tin nhắn...", label_visibility="collapsed", placeholder="Nhắn gì đó...")
        with c2:
            send_btn = st.form_submit_button("Gửi 📤")
            
        if send_btn and msg_text.strip() != "":
            supabase.table("messages").insert({
                "room_id": st.session_state.room_id,
                "sender": st.session_state.user_name,
                "avatar": st.session_state.user_avatar,
                "content": msg_text.strip()
            }).execute()
            st.rerun()

# --- GỌI VIDEO ---
with col_call:
    st.subheader("📹 Gọi Video / Thoại")
    
    if "in_call" not in st.session_state:
        st.session_state.in_call = False

    if not st.session_state.in_call:
        if st.button("📞 Bắt đầu cuộc gọi Video", type="primary", use_container_width=True):
            st.session_state.in_call = True
            st.rerun()
    else:
        if st.button("📴 Kết thúc cuộc gọi", type="secondary", use_container_width=True):
            st.session_state.in_call = False
            st.rerun()
            
        room_clean = "".join(e for e in st.session_state.room_id if e.isalnum())
        jitsi_url = f"https://meet.jit.si/PhoningMessengerRoom_{room_clean}#userInfo.displayName=%22{st.session_state.user_name}%22"
        components.iframe(jitsi_url, height=450, scrolling=False)

