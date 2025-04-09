from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Cho phép gọi API từ bất kỳ đâu (kể cả GPT)

# Access tokens cố định cho API gốc 1Office
ACCESS_TOKEN_LIST = "82616878267f5d7c3bc8f2101911486"
ACCESS_TOKEN_DETAIL = "82616878267f5d7c3bc8f2101911486"

# === Endpoint: Lấy danh sách nhân sự ===
@app.route("/api/hr", methods=["GET"])
def get_personnel():
    filters = request.args.get("filters", "")
    limit = request.args.get("limit", "30")  # Giới hạn số bản ghi (mặc định 30)
    
    params = {
        "access_token": ACCESS_TOKEN_LIST,
        "filters": filters,
        "limit": limit
    }

    try:
        res = requests.get(
            "https://innojsc.1office.vn/api/personnel/profile/gets",
            params=params
        )
        res.raise_for_status()
        return jsonify(res.json()), res.status_code
    except requests.RequestException as e:
        return jsonify({"error": "Lỗi gọi API 1Office", "details": str(e)}), 500

# === Endpoint: Lấy chi tiết nhân sự ===
@app.route("/api/hr-detail", methods=["GET"])
def get_detail():
    code = request.args.get("code")
    if not code:
        return jsonify({"error": "Thiếu mã nhân sự"}), 400

    params = {
        "access_token": ACCESS_TOKEN_DETAIL,
        "code": code
    }

    try:
        res = requests.get(
            "https://innojsc.1office.vn/api/personnel/profile/item",
            params=params
        )
        res.raise_for_status()
        return jsonify(res.json()), res.status_code
    except requests.RequestException as e:
        return jsonify({"error": "Lỗi gọi API 1Office", "details": str(e)}), 500

# === Khởi chạy ứng dụng ===
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
