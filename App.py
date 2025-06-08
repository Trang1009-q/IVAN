from flask import Flask, request, jsonify, render_template
from datetime import date, datetime

app = Flask(__name__)

def chatbot_response(user_input):
    robot_brain = ""

    if user_input.strip() == "":
        robot_brain = "Bạn chưa nhập nội dung. Vui lòng thử lại."
    elif "hôm nay" in user_input:
        robot_brain = date.today().strftime("%d/%m/%Y")
    elif "giờ" in user_input:
        robot_brain = datetime.now().strftime("%H giờ %M phút %S giây")
    elif "tạm biệt" in user_input:
        robot_brain = "Tạm biệt Trang"
    
    # Các vấn đề liên quan đến tài khoản
    elif "quên mật khẩu" in user_input:
        robot_brain = "Bạn có thể sử dụng chức năng 'Quên mật khẩu' trên trang đăng nhập."
    elif "không thể đăng nhập" in user_input:
        robot_brain = "Tên đăng nhập của bạn có thể không đúng."
    elif "mật khẩu không hoạt động" in user_input:
        robot_brain = "Đảm bảo rằng bạn đã nhập đúng mật khẩu. Mật khẩu phân biệt chữ hoa và chữ thường."
    elif "tài khoản bị khóa" in user_input:
        robot_brain = "Tài khoản của bạn có thể bị khóa. Vui lòng liên hệ với bộ phận hỗ trợ."
    elif "không thể kết nối" in user_input:
        robot_brain = "Vui lòng kiểm tra kết nối internet và thử lại."
    
    # Đăng ký và đăng nhập
    elif "cách đăng ký" in user_input:
        robot_brain = "Vui lòng truy cập trang web của chúng tôi để điền vào mẫu đăng ký."
    elif "quy trình đăng ký" in user_input:
        robot_brain = "Điền thông tin của bạn, xác minh email và đặt mật khẩu."
    elif "cần gì để đăng ký" in user_input:
        robot_brain = "Bạn cần một địa chỉ email hợp lệ và số điện thoại."
    elif "đăng ký có miễn phí không" in user_input:
        robot_brain = "Có, việc đăng ký hoàn toàn miễn phí."
    elif "đăng ký mất bao lâu" in user_input:
        robot_brain = "Quá trình đăng ký chỉ mất vài phút nếu bạn có đủ thông tin."
    elif "có thể đăng ký nhiều tài khoản không" in user_input:
        robot_brain = "Không, mỗi người chỉ có thể có một tài khoản."

    # Hỗ trợ sử dụng hệ thống ELearning
    elif "cách gửi bài tập" in user_input:
        robot_brain = "Giáo viên có thể tạo bài tập và học sinh có thể gửi bài tập thông qua mục 'Bài tập' trên hệ thống."
    elif "cách chấm điểm" in user_input:
        robot_brain = "Giáo viên có thể chấm điểm bài làm của học sinh trực tiếp trên hệ thống."
    elif "cách xem lịch học" in user_input:
        robot_brain = "Bạn có thể xem lịch học trong mục 'Lịch trình' trên hệ thống."
    elif "cách tham gia lớp học trực tuyến" in user_input:
        robot_brain = "Bạn cần vào mục 'Lớp học' và nhấn vào liên kết tham gia lớp học trực tuyến."
    elif "cách tải tài liệu" in user_input:
        robot_brain = "Tài liệu có thể được tải xuống từ mục 'Tài liệu' trên hệ thống."
    
    # Các vấn đề về phụ huynh
    elif "cách theo dõi tiến độ học tập của con" in user_input:
        robot_brain = "Phụ huynh có thể theo dõi tiến độ học tập của con thông qua mục 'Báo cáo học tập' trên hệ thống."
    elif "cách liên hệ giáo viên" in user_input:
        robot_brain = "Bạn có thể gửi tin nhắn trực tiếp đến giáo viên qua mục 'Liên lạc' trên hệ thống."
    elif "cách nhận thông báo" in user_input:
        robot_brain = "Bạn sẽ nhận thông báo qua email hoặc trên hệ thống khi có cập nhật mới."

    else:
        robot_brain = "Xin lỗi, tôi chưa có thông tin về điều này."

    return robot_brain

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chatbot", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    response = chatbot_response(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    import os
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)

