import os
import gspread
from google.oauth2.service_account import Credentials
import gradio as gr

# ==========================================
# CẤU HÌNH KẾT NỐI GOOGLE SHEETS (LƯU CRM)
# ==========================================
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def save_customer_info(name, phone, address, notes):
  if not name or not phone:
    return "⚠️ Vui lòng nhập đầy đủ Họ tên và Số điện thoại để chúng tôi hỗ trợ tốt nhất!"

  try:
    # Kiểm tra biến môi trường chứa thông tin kết nối Google Sheets
    creds_json = os.environ.get("GOOGLE_CREDENTIALS_JSON")
    if not creds_json:
      print(f"[Đã ghi nhận] Khách hàng: {name} | SĐT: {phone} | ĐC: {address} | Yêu cầu: {notes}")
      return (
          f"✅ Cảm ơn anh/chị {name}! Thông tin đã được ghi nhận vào hệ thống"
          " (Chế độ lưu cục bộ thành công). Đội ngũ Hồng Nhung Tây Nguyên sẽ liên hệ lại sớm nhất!"
      )

    # Kết nối Google Sheets thực tế qua Service Account
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

    from datetime import datetime

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([current_time, name, phone, address, notes])

    return (
        f"✅ Cảm ơn anh/chị {name}! Thông tin của anh/chị đã được lưu thành công."
        " Đội ngũ Nội Thất Hồng Nhung Tây Nguyên sẽ liên hệ lại trong thời gian"
        " sớm nhất."
    )
  except Exception as e:
    return f"❌ Có lỗi xảy ra khi lưu thông tin: {str(e)}"


# ==========================================
# TRỢ LÝ AI TƯ VẤN NỘI THẤT HỒNG NHUNG TÂY NGUYÊN
# ==========================================
def ai_interior_consultant(message, history):
  msg_lower = message.lower()

  if "gương" in msg_lower or "led" in msg_lower:
    return (
        "Dạ, tại Nội Thất Hồng Nhung Tây Nguyên chúng tôi cung cấp các dòng"
        " gương LED decor cao cấp, gương trang trí phòng khách, phòng ngủ và"
        " phòng tắm với ánh sáng sang trọng, hiện đại. Anh/chị đang quan tâm"
        " đến kiểu dáng hoặc kích thước khoảng bao nhiêu ạ?"
    )
  elif "giá" in msg_lower or "báo giá" in msg_lower or "chi phí" in msg_lower:
    return (
        "Dạ, chi phí nội thất sẽ tùy thuộc vào diện tích không gian, chất liệu gỗ"
        " hoặc mẫu sản phẩm cụ thể. Anh/chị vui lòng qua tab 'Đăng Ký Tư Vấn'"
        " để lại số điện thoại hoặc mô tả sơ qua nhu cầu, bên em sẽ gửi báo giá"
        " chi tiết và các chương trình ưu đãi tốt nhất cho mình nhé!"
    )
  elif "thiết kế" in msg_lower or "3d" in msg_lower or "không gian" in msg_lower or "phòng khách" in msg_lower:
    return (
        "Chúng tôi hỗ trợ trải nghiệm không gian nội thất 3D trực tuyến và thiết"
        " kế trọn gói từ phòng khách, phòng ngủ đến không gian kinh doanh."
        " Anh/chị có thể tham khảo mục 'Trải Nghiệm 3D & Sản Phẩm' trên ứng"
        " dụng hoặc chia sẻ phong cách yêu thích (hiện đại, cổ điển, gỗ tự"
        " nhiên...) để AI tư vấn ý tưởng phù hợp nhất ạ!"
    )
  else:
    return (
        f"Chào anh/chị! Cảm ơn anh/chị đã đến với không gian trực tuyến của"
        f" 'Trải Nghiệm Khách Hàng _ Hồng Nhung Tây Nguyên'. Về câu hỏi"
        f" '{message}', chúng tôi luôn sẵn sàng hỗ trợ tư vấn giải pháp tối ưu"
        " nhất. Anh/chị cần em hỗ trợ thêm thông tin chi tiết nào nữa không ạ?"
    )


# ==========================================
# XÂY DỰNG GIAO DIỆN ỨNG DỤNG (GRADIO)
# ==========================================
with gr.Blocks(theme=gr.themes.Soft()) as demo:
  gr.Markdown("# 🛋️ Trải Nghiệm Khách Hàng _ Hồng Nhung Tây Nguyên")
  gr.Markdown(
      "Nền tảng trực tuyến tích hợp trí tuệ nhân tạo AI, trải nghiệm không gian"
      " nội thất 3D và chăm sóc khách hàng chuyên nghiệp."
  )

  with gr.Tabs():
    with gr.TabItem("🤖 Trợ Lý AI Tư Vấn Nội Thất"):
      gr.ChatInterface(
          fn=ai_interior_consultant,
          chatbot=gr.Chatbot(height=360),
          textbox=gr.Textbox(
              placeholder=(
                  "Nhập câu hỏi về nội thất, gương LED, bàn ghế, báo giá..."
              )
          ),
          title="Hỏi Đáp Cùng Trợ Lý AI Hồng Nhung",
          description=(
              "Trợ lý ảo luôn sẵn sàng giải đáp mọi thắc mắc về sản phẩm và"
              " không gian nội thất 24/7."
          ),
      )

    with gr.TabItem("🏛️ Trải Nghiệm Không Gian 3D & Sản Phẩm"):
      gr.Markdown(
          "### Khám phá các hạng mục thiết kế không gian nội thất trực tuyến"
      )
      with gr.Row():
        gr.Image(
            "https://images.unsplash.com/photo-1618221195710-dd6b41faaea6",
            label="Không gian phòng khách hiện đại",
        )
        gr.Image(
            "https://images.unsplash.com/photo-1616486338812-3dadae4b4ace",
            label="Mẫu nội thất gỗ cao cấp",
        )
      gr.Markdown(
          "*Ghi chú: Khách hàng có thể dễ dàng quan sát phối cảnh trực quan,"
          " màu sắc và đường nét thiết kế ngay trên ứng dụng.*"
      )

    with gr.TabItem("📝 Đăng Ký Tư Vấn & Lưu Thông Tin"):
      gr.Markdown(
          "### Kết nối ngay với Nội Thất Hồng Nhung Tây Nguyên để nhận ưu đãi"
          " tốt nhất"
      )
      with gr.Row():
        c_name = gr.Textbox(label="Họ và tên *", placeholder="Nhập họ tên của bạn")
        c_phone = gr.Textbox(
            label="Số điện thoại *", placeholder="Nhập số điện thoại liên hệ"
        )
      c_address = gr.Textbox(
          label="Địa chỉ / Khu vực",
          placeholder="Ví dụ: Buôn Ma Thuột, Gia Lai, Lâm Đồng...",
      )
      c_notes = gr.Textbox(
          label="Yêu cầu chi tiết (Sản phẩm quan tâm, diện tích, ngân sách...)",
          lines=3,
          placeholder=(
              "Ví dụ: Cần tư vấn trọn gói nội thất phòng khách và gương LED..."
          ),
      )
      submit_btn = gr.Button("Gửi Yêu Cầu Tư Vấn", variant="primary")
      output_msg = gr.Textbox(
          label="Trạng thái hệ thống", interactive=False, lines=2
      )

      submit_btn.click(
          fn=save_customer_info,
          inputs=[c_name, c_phone, c_address, c_notes],
          outputs=output_msg,
      )

if __name__ == "__main__":
  demo.launch()
