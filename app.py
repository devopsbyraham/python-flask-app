from flask import Flask, jsonify
import os

app = Flask(__name__)
version = os.environ.get('APP_VERSION', '2.0.0')

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "version": version}), 200

@app.route('/')
def home():
    return jsonify({"message": "THIS IS APP V-2.0"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
