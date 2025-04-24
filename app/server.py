from flask import Flask,request, jsonify,session
from flask_cors import CORS
from utils.app import process_user_input
from routers.data_routes import data_routes
import logging
import os
import tempfile
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from gtts import gTTS

app = Flask(__name__)
import secrets
app.secret_key = secrets.token_hex(32)  # Generates a secure random 32-byte key
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
app.register_blueprint(data_routes)
@app.route('/members')
def members():
    return {"members": ["Member1", "Member2", "Member3"]}


if __name__ == '__main__':
    app.run(debug=True)
