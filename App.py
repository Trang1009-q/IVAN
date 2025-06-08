import os
import re
import unicodedata
from flask import Flask, request, jsonify, render_template
from datetime import date, datetime
from difflib import get_close_matches

app = Flask(__name__)

# -------------------------
# TIỀN XỬ LÝ & TIỆN ÍCH
# -------------------------

def normalize_text(text):
    """Chuẩn hóa: bỏ dấu, thường hóa, loại ký tự đặc biệt"""
    text = unicodedata.normalize("NFD", text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    text = re.sub(r"[^\w\s]", "", text)
    return text.lower().strip()

# -------------------------
# DỮ LIỆU TỪ KHÓA & PHẢN HỒI
# -------------------------

KEYWORD_RESPONSES = {
    # Thời gian & ngày tháng
    "giờ": [
        "mấy giờ", "giờ hiện tại", "bây giờ là mấy giờ", "thời gian", "giờ"
    ],
    "hôm nay": [
        "hôm nay là ngày gì", "ngày bao nhiêu", "thứ mấy", "hôm nay", "ngày hôm nay"
    ],
    "tạm biệt": [
        "tạm biệt", "bye", "chào nhé", "hẹn gặp lại", "tạm biệt bạn"
    ],

    # Tài khoản
    "quên mật khẩu": [
        "quên mật khẩu", "lấy lại mật khẩu", "reset password", "mất mật khẩu", "không nhớ mật khẩu"
    ],
    "không thể đăng nhập": [
        "không thể đăng nhập", "lỗi đăng nhập", "không vào được", "đăng nhập không thành công"
    ],
    "mật khẩu không hoạt động": [
        "mật khẩu không đúng", "password bị sai", "không hoạt động", "lỗi mật khẩu"
    ],
    "tài khoản bị khóa": [
        "tài khoản bị khóa", "bị khóa", "không đăng nhập được vì bị khóa"
    ],
    "không thể kết nối": [
        "mất kết nối", "không thể kết nối", "kết nối lỗi", "lỗi mạng"
    ],

    # Đăng ký
    "cách đăng ký": [
        "cách đăng ký", "đăng ký như thế nào", "tạo tài khoản", "làm sao để đăng ký"
    ],
    "quy trình đăng ký": [
        "quy trình đăng ký", "các bước đăng ký", "hướng dẫn tạo tài khoản"
    ],
    "cần gì để đăng ký": [
        "cần gì để đăng ký", "đăng ký cần thông tin gì", "đăng ký cần chuẩn bị gì"
    ],
    "đăng ký có miễn phí không": [
        "đăng ký có mất tiền không", "có miễn phí không", "đăng ký miễn phí không"
    ],
    "đăng ký mất bao lâu": [
        "đăng ký mất bao lâu", "mất bao lâu để đăng ký", "đăng ký nhanh không"
    ],
    "có thể đăng ký nhiều tài khoản không": [
        "có thể có nhiều tài khoản không", "đăng ký nhiều lần được không", "tài khoản thứ hai"
    ],

    # Elearning - học tập
    "cách gửi bài tập": [
        "nộp bài tập", "gửi bài", "cách nộp bài", "gửi bài tập"
    ],
    "cách chấm điểm": [
        "chấm điểm", "giáo viên chấm như thế nào", "đánh giá bài tập"
    ],
    "cách xem lịch học": [
        "xem lịch học", "lịch học hôm nay", "lịch học ở đâu"
    ],
    "cách tham gia lớp học trực tuyến": [
        "tham gia lớp học", "vào học online", "lớp học trực tuyến"
    ],
    "cách tải tài liệu": [
        "tải tài liệu", "download tài liệu", "tải xuống tài liệu"
    ],

    # Phụ huynh
    "cách theo dõi tiến độ học tập của con": [
        "tiến độ học tập", "xem kết quả học", "phụ huynh theo dõi con", "báo cáo học tập"
    ],
    "cách liên hệ giáo viên": [
        "liên hệ giáo viên", "gửi tin nhắn cho giáo viên", "liên lạc thầy cô"
    ],
    "cách nhận thông báo": [
        "nhận thông báo", "xem thông báo", "thông báo mới", "cập nhật thông báo"
    ]
}

RESPONSES = {
    "giờ": lambda: datetime.now().strftime("%H giờ %M phút %S giây"),
    "hôm nay": lambda: date.today().strftime("%d/%m/%Y"),
    "tạm biệt": "Tạm biệt Trang",

    "quên mật khẩu": "Bạn có thể sử dụng chức năng 'Quên mật khẩu' trên trang đăng nhập.",
    "không thể đăng nhập": "Tên đăng nhập của bạn có thể không đúng.",
    "mật khẩu không hoạt động": "Đảm bảo rằng bạn đã nhập đúng mật khẩu. Mật khẩu phân biệt chữ hoa và chữ thường.",
    "tài khoản bị khóa": "Tài khoản của bạn có thể bị khóa. Vui lòng liên hệ với bộ phận hỗ trợ.",
    "không thể kết nối": "Vui lòng kiểm tra kết nối internet và thử lại.",

    "cách đăng ký": "Vui lòng truy cập trang web của chúng tôi để điền vào mẫu đăng ký.",
    "quy trình đăng ký": "Điền thông tin của bạn, xác minh email và đặt mật khẩu.",
    "cần gì để đăng ký": "Bạn cần một địa chỉ email hợp lệ và số điện thoại.",
    "đăng ký có miễn phí không": "Có, việc đăng ký hoàn toàn miễn phí.",
    "đăng ký mất bao lâu": "Quá trình đăng ký chỉ mất vài phút nếu bạn có đủ thông tin.",
    "có thể đăng ký nhiều tài khoản không": "Không, mỗi người chỉ nên có một tài khoản.",

    "cách gửi bài tập": "Giáo viên có thể tạo bài tập và học sinh gửi bài thông qua mục 'Bài tập' trên hệ thống.",
    "cách chấm điểm": "Giáo viên có thể chấm điểm bài làm trực tiếp trên hệ thống.",
    "cách xem lịch học": "Bạn có thể xem lịch học trong mục 'Lịch trình' trên hệ thống.",
    "cách tham gia lớp học trực tuyến": "Bạn cần vào mục 'Lớp học' và nhấn vào liên kết tham gia.",
    "cách tải tài liệu": "Tài liệu có thể được tải từ mục 'Tài liệu' trên hệ thống.",

    "cách theo dõi tiến độ học tập của con": "Phụ huynh theo dõi tiến độ học tập qua mục 'Báo cáo học tập'.",
    "cách liên hệ giáo viên": "Bạn có thể gửi tin nhắn trực tiếp qua mục 'Liên lạc'.",
    "cách nhận thông báo": "Bạn sẽ nhận thông báo qua email hoặc hệ thống khi có cập nhật mới."
}

DEFAULT_RESPONSE = "Xin lỗi, tôi chưa có thông tin về điều này."
EMPTY_INPUT_RESPONSE = "Bạn chưa nhập nội dung. Vui lòng thử lại."

# -------------------------
# CHATBOT XỬ LÝ ĐẦU VÀO
# -------------------------

def chatbot_response(user_input):
    user_input_raw = user_input.strip()
    if not user_input_raw:
        return EMPTY_INPUT_RESPONSE

    user_input_norm = normalize_text(user_input_raw)

    for key, variants in KEYWORD_RESPONSES.items():
        for variant in variants:
            if variant in user_input_norm:
                response = RESPONSES.get(key)
                return response() if callable(response) else response

    all_variants = [v for values in KEYWORD_RESPONSES.values() for v in values]
    closest = get_close_matches(user_input_norm, all_variants, n=1, cutoff=0.6)

    if closest:
        for key, variants in KEYWORD_RESPONSES.items():
            if closest[0] in variants:
                response = RESPONSES.get(key)
                return response() if callable(response) else response

    return DEFAULT_RESPONSE

# -------------------------
# ROUTES FLASK
# -------------------------

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chatbot", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    response = chatbot_response(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
