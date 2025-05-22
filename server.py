# server.py

from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route('/env', methods=['GET'])
def get_env():
    try:
        with open('env.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data), 200
    except FileNotFoundError:
        return jsonify({'error': 'env.json not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
