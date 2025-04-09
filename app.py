from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Gắn access token tại đây
ACCESS_TOKEN_LIST = "82616878267f5d7c3bc8f2101911486"
ACCESS_TOKEN_DETAIL = "82616878267f5d7c3bc8f2101911486"

@app.route("/api/hr", methods=["GET"])
def get_personnel():
    filters = request.args.get("filters", "")

    res = requests.get(
        "https://innojsc.1office.vn/api/personnel/profile/gets",
        params={"access_token": ACCESS_TOKEN_LIST, "filters": filters}
    )

    return jsonify(res.json()), res.status_code

@app.route("/api/hr-detail", methods=["GET"])
def get_detail():
    code = request.args.get("code")
    if not code:
        return jsonify({"error": "Thiếu mã nhân sự"}), 400

    res = requests.get(
        "https://innojsc.1office.vn/api/personnel/profile/item",
        params={"access_token": ACCESS_TOKEN_DETAIL, "code": code}
    )

    return jsonify(res.json()), res.status_code

if __name__ == "__main__":
    app.run(debug=True, port=5000)
