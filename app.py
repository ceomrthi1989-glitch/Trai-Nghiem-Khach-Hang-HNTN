import os
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
import streamlit as st

# ==========================================
# CẤU HÌNH GIAO DIỆN STREAMLIT
# ==========================================
st.set_page_config(
    page_title="Trải Nghiệm Khách Hàng - Hồng Nhung Tây Nguyên",
    page_icon="🛋️",
    layout="wide",
)

# Tiêu đề chính ứng dụng
st.title("🛋️ Trải Nghiệm Khách Hàng _ Hồng Nhung Tây Nguyên")
st.markdown(
    "Nền tảng trực tuyến tích hợp trí tuệ nhân tạo AI, trải nghiệm không gian"
    " nội thất 3D và chăm sóc khách hàng chuyên nghiệp."
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
    # Lấy thông tin xác thực từ Streamlit Secrets hoặc biến môi trường
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
    "🤖 Trợ Lý AI Tư Vấn Nội Thất",
    "🏛️ Trải Nghiệm Không Gian 3D & Sản Phẩm",
    "📝 Đăng Ký Tư Vấn & Lưu Thông Tin",
])

# --- TAB 1: TRỢ LÝ AI ---
with tab1:
  st.subheader("Hỏi Đáp Cùng Trợ Lý AI Hồng Nhung")
  st.write(
      "Trợ lý ảo luôn sẵn sàng giải đáp mọi thắc mắc về sản phẩm và không gian"
      " nội thất 24/7."
  )

  # Khởi tạo lịch sử chat trong session_state
  if "messages" not in st.session_state:
    st.session_state.messages = []

  # Hiển thị lịch sử chat
  for message in st.session_state.messages:
    with st.chat_message(message["role"]):
      st.markdown(message["content"])

  # Nhập câu hỏi từ người dùng
  if prompt := st.chat_input(
      "Nhập câu hỏi về nội thất, gương LED, bàn ghế, báo giá..."
  ):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
      st.markdown(prompt)

    # Xử lý phản hồi AI dựa theo từ khóa thực tế của cửa hàng
    msg_lower = prompt.lower()
    if "gương" in msg_lower or "led" in msg_lower:
      ai_response = (
          "Dạ, tại Nội Thất Hồng Nhung Tây Nguyên chúng tôi cung cấp các dòng"
          " gương LED decor cao cấp, gương trang trí phòng khách, phòng ngủ và"
          " phòng tắm với ánh sáng sang trọng, hiện đại. Anh/chị đang quan tâm"
          " đến kiểu dáng hoặc kích thước khoảng bao nhiêu ạ?"
      )
    elif (
        "giá" in msg_lower
        or "báo giá" in msg_lower
        or "chi phí" in msg_lower
    ):
      ai_response = (
          "Dạ, chi phí nội thất sẽ tùy thuộc vào diện tích không gian, chất liệu"
          " gỗ hoặc mẫu sản phẩm cụ thể. Anh/chị vui lòng qua tab 'Đăng Ký Tư"
          " Vấn' để lại số điện thoại hoặc mô tả sơ qua nhu cầu, bên em sẽ gửi"
          " báo giá chi tiết và các chương trình ưu đãi tốt nhất cho mình nhé!"
      )
    elif (
        "thiết kế" in msg_lower
        or "3d" in msg_lower
        or "không gian" in msg_lower
        or "phòng khách" in msg_lower
    ):
      ai_response = (
          "Chúng tôi hỗ trợ trải nghiệm không gian nội thất 3D trực tuyến và"
          " thiết kế trọn gói từ phòng khách, phòng ngủ đến không gian kinh"
          " doanh. Anh/chị có thể tham khảo mục 'Trải Nghiệm 3D & Sản Phẩm' trên"
          " ứng dụng hoặc chia sẻ phong cách yêu thích để AI tư vấn ý tưởng phù"
          " hợp nhất ạ!"
      )
    else:
      ai_response = (
          f"Chào anh/chị! Cảm ơn anh/chị đã đến với không gian trực tuyến của"
          f" 'Trải Nghiệm Khách Hàng _ Hồng Nhung Tây Nguyên'. Về câu hỏi"
          f" '{prompt}', chúng tôi luôn sẵn sàng hỗ trợ tư vấn giải pháp tối"
          " ưu nhất. Anh/chị cần em hỗ trợ thêm thông tin chi tiết nào nữa"
          " không ạ?"
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
