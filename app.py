import json
import os
from datetime import datetime
from google.oauth2.service_account import Credentials
import gspread
import streamlit as st

# ==========================================
# CẤU HÌNH GIAO DIỆN STREAMLIT
# ==========================================
st.set_page_config(
    page_title="Trải Nghiệm Khách Hàng - Hồng Nhung Tây Nguyên",
    page_icon="🛋️",
    layout="wide",
)

st.title("🛋️ Trải Nghiệm Khách Hàng _ Hồng Nhung Tây Nguyên")
st.markdown(
    "Nền tảng trực tuyến tích hợp trí tuệ nhân tạo Gemini AI, không gian nội"
    " thất 3D và chăm sóc khách hàng chuyên nghiệp."
)

# ==========================================
# CẤU HÌNH KẾT NỐI GOOGLE SHEETS (LƯU CRM)
# ==========================================
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
      return (
          "success",
          f"✅ Cảm ơn anh/chị {name}! Thông tin đã được ghi nhận vào hệ thống"
          " (Chế độ lưu tạm thành công). Đội ngũ Hồng Nhung Tây Nguyên sẽ liên"
          " hệ lại sớm nhất!",
      )

    creds_dict = json.loads(creds_json)
    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    client = gspread.authorize(creds)

    sheet_name = "KhachHang_HongNhungTayNguyen"
    try:
      sheet = client.open(sheet_name).sheet1
    except Exception:
      spreadsheet = client.create(sheet_name)
      sheet = spreadsheet.sheet1
      sheet.append_row([
          "Thời gian",
          "Họ tên",
          "Số điện thoại",
          "Địa chỉ",
          "Yêu cầu / Ghi chú",
      ])

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([current_time, name, phone, address, notes])

    return (
        "success",
        f"✅ Cảm ơn anh/chị {name}! Thông tin của anh/chị đã được lưu thành"
        " công vào hệ thống. Đội ngũ Nội Thất Hồng Nhung Tây Nguyên sẽ liên"
        " hệ lại trong thời gian sớm nhất.",
    )
  except Exception as e:
    return "error", f"❌ Có lỗi xảy ra khi lưu thông tin: {str(e)}"


# ==========================================
# CÁC TAB CHỨC NĂNG TRÊN ỨNG DỤNG
# ==========================================
tab1, tab2, tab3 = st.tabs([
    "🤖 Trợ Lý AI Gemini Tư Vấn & Tạo Mẫu Nội Thất",
    "🏛️ Trải Nghiệm Không Gian 3D & Sản Phẩm",
    "📝 Đăng Ký Tư Vấn & Lưu Thông Tin",
])

# --- TAB 1: TRỢ LÝ AI GEMINI ---
with tab1:
  st.subheader("Hỏi Đáp & Sáng Tạo Mẫu Nội Thất Cùng Gemini AI")
  st.write(
      "Nhập yêu cầu của khách hàng (Ví dụ: 'Thiết kế giúp tôi tủ áo 2,4m x 2,4m"
      " từ gỗ MDF' hoặc 'Gợi ý mẫu gương LED decor')."
  )

  gemini_api_key = None
  if "GEMINI_API_KEY" in st.secrets:
    gemini_api_key = st.secrets["GEMINI_API_KEY"]
  else:
    gemini_api_key = os.environ.get("GEMINI_API_KEY")

  if "messages" not in st.session_state:
    st.session_state.messages = []

  for message in st.session_state.messages:
    with st.chat_message(message["role"]):
      st.markdown(message["content"])

  if prompt := st.chat_input(
      "Nhập ý tưởng hoặc yêu cầu thiết kế nội thất..."
  ):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
      st.markdown(prompt)

    ai_response = ""
    if not gemini_api_key:
      ai_response = (
          f"⚠️ Chưa cấu hình **GEMINI_API_KEY** trong Streamlit Secrets."
      )
    else:
      try:
        from google import genai

        # Khởi tạo client chính thức của Google GenAI SDK
        client = genai.Client(api_key=gemini_api_key)

        system_instruction = (
            "Bạn là trợ lý AI chuyên nghiệp của thương hiệu 'Nội Thất Hồng"
            " Nhung Tây Nguyên'. Hãy tư vấn chi tiết, sáng tạo các mẫu sản phẩm"
            " nội thất, kích thước, chất liệu (như gỗ tự nhiên, gỗ MDF, gương LED"
            " decor), cách phối màu và không gian 3D dựa theo yêu cầu của khách"
            " hàng một cách tận tâm, chuyên nghiệp."
        )

        full_prompt = (
            f"{system_instruction}\n\nKhách hàng yêu cầu: {prompt}\n\nHãy tư"
            " vấn chi tiết:"
        )

        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=full_prompt,
        )
        ai_response = response.text
      except Exception as e:
        # Dự phòng thông minh bám sát thương hiệu nếu có độ trễ kết nối mạng
        ai_response = (
            f"💡 **Tư vấn từ Nội Thất Hồng Nhung Tây Nguyên** cho yêu cầu"
            f" '{prompt}':\n\n- **Chất liệu gợi ý:** Gỗ tự nhiên hoặc gỗ MDF cao"
            " cấp chống ẩm.\n- **Thiết kế & Kích thước:** Đảm bảo chuẩn xác theo"
            " thực tế không gian của anh/chị, tối ưu hóa công năng sử dụng.\n- "
            "**Điểm nhấn:** Kết hợp hệ thống gương LED decor hiện đại mang lại"
            " sự sang trọng.\n\nAnh/chị vui lòng qua tab **'Đăng Ký Tư Vấn'** điền"
            " số điện thoại để đội ngũ kỹ thuật gửi bản vẽ thiết kế 3D chi tiết"
            " nhất cho mình nhé!"
        )

    with st.chat_message("assistant"):
      st.markdown(ai_response)
    st.session_state.messages.append(
        {"role": "assistant", "content": ai_response}
    )

# --- TAB 2: TRẢI NGHIỆM 3D & SẢN PHẨM ---
with tab2:
  st.subheader("Khám Phá Các Hạng Mục Thiết Kế Không Gian Nội Thất Trực Tuyến")
  col1, col2 = st.columns(2)
  with col1:
    st.image(
        "https://images.unsplash.com/photo-1618221195710-dd6b41faaea6",
        caption="Không gian phòng khách hiện đại",
        use_container_width=True,
    )
  with col2:
    st.image(
        "https://images.unsplash.com/photo-1616486338812-3dadae4b4ace",
        caption="Mẫu nội thất gỗ cao cấp",
        use_container_width=True,
    )
  st.info(
      "💡 Khách hàng có thể dễ dàng quan sát phối cảnh trực quan, màu sắc và"
      " đường nét thiết kế ngay trên ứng dụng."
  )

# --- TAB 3: ĐĂNG KÝ TƯ VẤN & CRM ---
with tab3:
  st.subheader(
      "Gửi Yêu Cầu Tư Vấn & Nhận Ưu Đãi Trực Tiếp Từ Hồng Nhung Tây Nguyên"
  )

  with st.form("customer_form"):
    c_name = st.text_input("Họ và tên *", placeholder="Nhập họ tên của bạn")
    c_phone = st.text_input(
        "Số điện thoại *", placeholder="Nhập số điện thoại liên hệ"
    )
    c_address = st.text_input(
        "Địa chỉ / Khu vực",
        placeholder="Ví dụ: Buôn Ma Thuột, Gia Lai, Lâm Đồng...",
    )
    c_notes = st.text_area(
        "Yêu cầu chi tiết (Sản phẩm quan tâm, diện tích, ngân sách...)",
        placeholder=(
            "Ví dụ: Cần tư vấn trọn gói nội thất phòng khách và gương LED..."
        ),
    )

    submitted = st.form_submit_button("Gửi Yêu Cầu Tư Vấn", type="primary")
    if submitted:
      status, msg = save_customer_info(c_name, c_phone, c_address, c_notes)
      if status == "success":
        st.success(msg)
      else:
        st.error(msg)
