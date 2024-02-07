import os
import glob
from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_from_directory, abort, render_template
from werkzeug.utils import secure_filename
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

import competition_driver

load_dotenv()

app = Flask(__name__, static_folder='results')
auth = HTTPBasicAuth()

users = {
    "admin": generate_password_hash(os.getenv('ADMIN_PASSWORD'))
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

@app.route('/participate', methods=['POST'])
@auth.login_required
def participate():
    if 'file' not in request.files:
        return "No file part in the request.", 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file.', 400
    if not file.filename.endswith('.py'):
        return 'File type not supported.', 400
    filename = secure_filename(file.filename)
    file.save('/participations/' + filename)
    return 'File uploaded successfully.', 200

@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        return jsonify({"message": "username and password required"}), 400
    if username in users:
        return jsonify({"message": "user already exists"}), 400
    users[username] = generate_password_hash(password)
    return jsonify({"message": "user created"}), 201

@app.route('/download/<path:filename>', methods=['GET'])
def download(filename):
    try:
        return send_from_directory(app.static_folder, filename=filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)

@app.route('/download/date/<date>', methods=['GET'])
def download_date(date):
    files = glob.glob(f"{app.static_folder}/*{date}*.py")
    if not files:
        abort(404, description="No files found for the given date.")
    elif len(files) > 1:
        abort(400, description="Multiple files found for the given date. Please specify.")
    else:
        return send_from_directory(app.static_folder, filename=os.path.basename(files[0]), as_attachment=True)

@app.route('/download/datetime/<date>/<time>', methods=['GET'])
def download_datetime(date, time):
    files = glob.glob(f"{app.static_folder}/*{date}_{time}*.py")
    if not files:
        abort(404, description="No files found for the given date and time.")
    elif len(files) > 1:
        abort(400, description="Multiple files found for the given date and time. Please specify.")
    else:
        return send_from_directory(app.static_folder, filename=os.path.basename(files[0]), as_attachment=True)

@app.route('/contest', methods=['POST'])
@auth.login_required
def contest():
    if auth.current_user() != 'admin':
        return jsonify({"message": "Unauthorized"}), 403
    competition_driver.contest()
    return jsonify({"message": "Contest started"}), 200

@app.route('/participants', methods=['GET'])
def participants():
    participants = list(users.keys())[1:]
    return render_template('participants.html', participants=participants)

if __name__ == '__main__':
    app.run(debug=True)
