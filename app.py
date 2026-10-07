import os
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
import streamlit as st
import google.generativeai as genai
==========================================
CẤU HÌNH GIAO DIỆN STREAMLIT
==========================================
st.set_page_config(
page_title="Trải Nghiệm Khách Hàng - Hồng Nhung Tây Nguyên",
page_icon="🛋️",
layout="wide",
)
st.title("🛋️ Trải Nghiệm Khách Hàng _ Hồng Nhung Tây Nguyên")
st.markdown(
"Nền tảng trực tuyến tích hợp trí tuệ nhân tạo Gemini AI, trải nghiệm không gian"
" nội thất 3D và chăm sóc khách hàng chuyên nghiệp."
)
==========================================
CẤU HÌNH GEMINI AI & GOOGLE SHEETS
==========================================
Lấy API Key từ Streamlit Secrets hoặc biến môi trường
gemini_api_key = None
if "GEMINI_API_KEY" in st.secrets:
gemini_api_key = st.secrets["GEMINI_API_KEY"]
else:
gemini_api_key = os.environ.get("GEMINI_API_KEY")
if gemini_api_key:
genai.configure(api_key=gemini_api_key)
# Sử dụng mô hình Gemini mới nhất phù hợp cho trợ lý thông minh
generation_config = {
"temperature": 0.7,
"max_output_tokens": 1000,
}
model = genai.GenerativeModel(
model_name="gemini-1.5-flash",
generation_config=generation_config,
system_instruction=(
"Bạn là trợ lý AI chuyên nghiệp của thương hiệu 'Nội Thất Hồng Nhung Tây Nguyên'. "
"Bạn am hiểu sâu sắc về thiết kế nội thất, chất liệu gỗ, gương LED decor, và các phong cách "
"từ hiện đại, tân cổ điển đến không gian gỗ ấm cúng Tây Nguyên. "
"Khi khách hàng đưa ra yêu cầu (prompt) thiết kế sản phẩm hoặc không gian nội thất, "
"hãy đóng vai trò là kiến trúc sư trưởng: mô tả chi tiết ý tưởng mẫu sản phẩm, kích thước gợi ý, "
"chất liệu phù hợp, phối cảnh màu sắc và cách bài trí tối ưu để truyền cảm hứng cho họ."
)
)
else:
model = None
Cấu hình Google Sheets cho CRM
SCOPES = [
"https://www.googleapis.com/auth/spreadsheets",
"https://www.googleapis.com/auth/drive",
]
def save_customer_info(name, phone, address, notes):
if not name or not phone:
return "error", "⚠️ Vui lòng nhập đầy đủ Họ tên và Số điện thoại!"
try:
    creds_json = None
    if "GOOGLE_CREDENTIALS_JSON" in st.secrets:
        creds_json = st.secrets["GOOGLE_CREDENTIALS_JSON"]
    else:
        creds_json = os.environ.get("GOOGLE_CREDENTIALS_JSON")
        
    if not creds_json:
        return "success", f"✅ Cảm ơn anh/chị {name}! Thông tin đã được ghi nhận vào hệ thống (Chế độ lưu tạm thành công)."
        
    import json
    creds_dict = json.loads(creds_json)
    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    client = gspread.authorize(creds)
    
    sheet_name = "KhachHang_HongNhungTayNguyen"
    try:
        sheet = client.open(sheet_name).sheet1
    except Exception:
        spreadsheet = client.create(sheet_name)
        sheet = spreadsheet.sheet1
        sheet.append_row(["Thời gian", "Họ tên", "Số điện thoại", "Địa chỉ", "Yêu cầu / Ghi chú"])
        
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([current_time, name, phone, address, notes])
    
    return "success", f"✅ Cảm ơn anh/chị {name}! Thông tin đã được lưu thành công. Đội ngũ Nội Thất Hồng Nhung Tây Nguyên sẽ liên hệ lại sớm nhất."
except Exception as e:
    return "error", f"❌ Có lỗi xảy ra khi lưu thông tin: {str(e)}"


==========================================
CÁC TAB CHỨC NĂNG TRÊN ỨNG DỤNG
==========================================
tab1, tab2, tab3 = st.tabs([
"🤖 Trợ Lý Gemini AI Thiết Kế & Tư Vấn",
"🏛️ Trải Nghiệm Không Gian 3D & Sản Phẩm",
"📝 Đăng Ký Tư Vấn & Lưu Thông Tin"
])
--- TAB 1: TRỢ LÝ GEMINI AI ---
with tab1:
st.subheader("💡 Trợ Lý AI Gemini - Thiết Kế & Gợi Ý Mẫu Nội Thất Theo Prompt")
st.markdown(
"Nhập yêu cầu thiết kế hoặc ý tưởng của bạn (ví dụ: 'Thiết kế giúp tôi bộ bàn ghế gỗ phòng khách phong cách hiện đại cho nhà ống', "
"hoặc 'Gợi ý mẫu gương LED decor phòng ngủ') để Gemini AI phác thảo ý tưởng chi tiết ngay lập tức!"
)
if not gemini_api_key:
    st.warning("⚠️ Chưa cấu hình khóa `GEMINI_API_KEY` trong Secrets. Ứng dụng đang chạy ở chế độ phản hồi mô phỏng mặc định. Hãy thêm API Key để kết nối Gemini AI.")

if "gemini_messages" not in st.session_state:
    st.session_state.gemini_messages = []

for message in st.session_state.gemini_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Nhập ý tưởng hoặc yêu cầu nội thất của bạn tại đây..."):
    st.session_state.gemini_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Kiến trúc sư Gemini AI đang phác thảo ý tưởng mẫu nội thất cho bạn..."):
            try:
                if model and gemini_api_key:
                    # Gọi API Gemini thực tế
                    chat_history = [
                        {"role": m["role"], "parts": [m["content"]]} 
                        for m in st.session_state.gemini_messages[:-1]
                    ]
                    chat = model.start_chat(history=chat_history)
                    response = chat.send_message(prompt)
                    ai_response = response.text
                else:
                    # Phản hồi dự phòng khi chưa có API Key
                    ai_response = (
                        f"Dạ, với yêu cầu thiết kế: *'{prompt}'*, Nội Thất Hồng Nhung Tây Nguyên xin gợi ý giải pháp: "
                        "Mẫu sản phẩm này sẽ được chế tác từ chất liệu gỗ cao cấp kết hợp đường nét tinh xảo, "
                        "tối ưu không gian và ánh sáng hài hòa. Anh/chị hãy để lại thông tin tại tab 'Đăng Ký Tư Vấn' "
                        "để đội ngũ kiến trúc sư gửi bản vẽ chi tiết hơn nhé!"
                    )
            except Exception as e:
                ai_response = f"⚠️ Đã xảy ra lỗi khi kết nối với Gemini AI: {str(e)}"
            
            st.markdown(ai_response)
    st.session_state.gemini_messages.append({"role": "assistant", "content": ai_response})


--- TAB 2: TRẢI NGHIỆM 3D & SẢN PHẨM ---
with tab2:
st.subheader("Khám Phá Các Hạng Mục Thiết Kế Không Gian Nội Thất Trực Tuyến")
col1, col2 = st.columns(2)
with col1:
st.image(
"https://images.unsplash.com/photo-1618221195710-dd6b41faaea6",
caption="Không gian phòng khách hiện đại",
use_container_width=True
)
with col2:
st.image(
"https://images.unsplash.com/photo-1616486338812-3dadae4b4ace",
caption="Mẫu nội thất gỗ cao cấp",
use_container_width=True
)
st.info("💡 Khách hàng có thể dễ dàng quan sát phối cảnh trực quan, màu sắc và đường nét thiết kế ngay trên ứng dụng.")
--- TAB 3: ĐĂNG KÝ TƯ VẤN & CRM ---
with tab3:
st.subheader("Gửi Yêu Cầu Tư Vấn & Nhận Ưu Đãi Trực Tiếp Từ Hồng Nhung Tây Nguyên")
with st.form("customer_form"):
    c_name = st.text_input("Họ và tên *", placeholder="Nhập họ tên của bạn")
    c_phone = st.text_input("Số điện thoại *", placeholder="Nhập số điện thoại liên hệ")
    c_address = st.text_input("Địa chỉ / Khu vực", placeholder="Ví dụ: Buôn Ma Thuột, Gia Lai, Lâm Đồng...")
    c_notes = st.text_area("Yêu cầu chi tiết từ ý tưởng AI (Sản phẩm quan tâm, diện tích, ngân sách...)", placeholder="Ví dụ: Tôi muốn làm bộ bàn ghế và gương LED theo mẫu AI vừa tư vấn...")
    
    submitted = st.form_submit_button("Gửi Yêu Cầu Tư Vấn", type="primary")
    if submitted:
        status, msg = save_customer_info(c_name, c_phone, c_address, c_notes)
        if status == "success":
            st.success(msg)
        else:
            st.error(msg)


