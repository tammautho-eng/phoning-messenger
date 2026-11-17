import streamlit as st
import datetime
import time

st.set_page_config(page_title="Phoning Messenger", page_icon="💬", layout="centered")

if "user1" not in st.session_state:
    st.session_state.user1 = {"name": "Ban", "avatar": "👤", "status": "Dang hoat dong"}
if "user2" not in st.session_state:
    st.session_state.user2 = {"name": "Ban Than", "avatar": "🧑‍🤝‍🧑", "status": "Dang hoat dong"}
if "avatars" not in st.session_state:
    st.session_state.avatars = ["👤", "🧑‍🤝‍🧑", "😊", "😎", "🐱"]
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"sender": "Ban Than", "avatar": "🧑‍🤝‍🧑", "msg": "Alo e, vo app test thu ne!", "time": "14:30"}
    ]
if "current_role" not in st.session_state:
    st.session_state.current_role = "user1"

if st.session_state.current_role == "user1":
    current_user = st.session_state.user1
    other_user = st.session_state.user2
else:
    current_user = st.session_state.user2
    other_user = st.session_state.user1

st.sidebar.title("⚙️ Cài đặt Phoning")
st.sidebar.write(f"Đang dùng nick: **{current_user['avatar']} {current_user['name']}**")

if st.sidebar.button(f"🔄 Chuyển sang nick [{other_user['name']}]"):
    if st.session_state.current_role == "user1":
        st.session_state.current_role = "user2"
    else:
        st.session_state.current_role = "user1"
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader("✏️ Đổi thông tin cá nhân")
new_name = st.sidebar.text_input("Tên hiển thị mới", value=current_user["name"])
new_avatar = st.sidebar.selectbox("Chọn Avatar mới", st.session_state.avatars)

if st.sidebar.button("💾 Cập nhật hồ sơ"):
    old_name = current_user["name"]
    current_user["name"] = new_name
    current_user["avatar"] = new_avatar
    for item in st.session_state.chat_history:
        if item["sender"] == old_name:
            item["sender"] = new_name
            item["avatar"] = new_avatar
    st.sidebar.success("Đã cập nhật thành công!")
    st.rerun()

st.title("💬 PHONING MESSENGER")
st.write(f"Trò chuyện giữa **{st.session_state.user1['avatar']} {st.session_state.user1['name']}** & **{st.session_state.user2['avatar']} {st.session_state.user2['name']}**")
st.markdown("---")

st.subheader("📜 Khung Chat")
chat_container = st.container(height=350)
with chat_container:
    if not st.session_state.chat_history:
        st.info("(Chưa có tin nhắn nào)")
    for item in st.session_state.chat_history:
        st.markdown(f"**`{item['time']}` {item['avatar']} {item['sender']}:** {item['msg']}")

with st.form(key="chat_form", clear_on_submit=True):
    user_msg = st.text_input("Nhập tin nhắn của bạn:")
    submit_btn = st.form_submit_button("📤 Gửi tin nhắn")
    if submit_btn and user_msg.strip() != "":
        now = datetime.datetime.now().strftime("%H:%M")
        st.session_state.chat_history.append({
            "sender": current_user["name"],
            "avatar": current_user["avatar"],
            "msg": user_msg,
            "time": now
        })
        st.rerun()

st.markdown("---")
st.subheader("📞 Tính năng gọi")
col1, col2 = st.columns(2)
with col1:
    if st.button("📞 Gọi thoại"):
        with st.spinner(f"Đang gọi thoại cho {other_user['name']}..."):
            time.sleep(2)
        now = datetime.datetime.now().strftime("%H:%M")
        st.session_state.chat_history.append({
            "sender": current_user["name"],
            "avatar": current_user["avatar"],
            "msg": "[GỌI THOẠI - Đã kết thúc]",
            "time": now
        })
        st.rerun()
with col2:
    if st.button("📹 Gọi Video"):
        with st.spinner(f"Đang gọi video cho {other_user['name']}..."):
            time.sleep(2)
        now = datetime.datetime.now().strftime("%H:%M")
        st.session_state.chat_history.append({
            "sender": current_user["name"],
            "avatar": current_user["avatar"],
            "msg": "[GỌI VIDEO - Đã kết thúc]",
            "time": now
        })
        st.rerun()
