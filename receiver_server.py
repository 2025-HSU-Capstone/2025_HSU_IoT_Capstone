
from flask import Flask, request

app = Flask(__name__)

@app.route('/receive-env', methods=['POST'])
def receive():
    data = request.get_json()
    print("🌱 수신된 데이터:", data)
    return {"message": "받았어요!"}

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5001)

