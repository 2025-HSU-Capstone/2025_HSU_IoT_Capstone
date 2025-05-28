from flask import Flask, request, jsonify
import json
import subprocess
import os

app = Flask(__name__)

SENSOR_SCRIPT = "RaspberryPi_last.py"  # 센서 제어 루프 파일 경로

# ✅ POST 요청으로 env.json 저장 + 자동 실행
@app.route("/set_env", methods=["POST"])
def set_env():
    try:
        env_data = request.get_json()

        # env.json 저장
        with open("env.json", "w", encoding="utf-8") as f:
            json.dump(env_data, f, ensure_ascii=False, indent=2)
        print("✅ env.json 저장 완료")

        # 이미 실행 중인 루프가 있다면 종료하도록 하고 싶으면 PID 추적 필요 (지금은 단순 실행)
        print("🚀 센서 제어 루프 실행 중...")
        subprocess.Popen(["python3", SENSOR_SCRIPT])

        return jsonify({"message": "env.json saved and loop started"}), 200
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
