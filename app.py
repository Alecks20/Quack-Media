from flask import Flask, request, jsonify, send_from_directory
import os
import traceback
import random
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
UPLOAD_FOLDER = 'library'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
AUTH_KEY = os.environ["AUTH_KEY"]

@app.route('/upload', methods=['POST'])
def upload_file():
  try:
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    if 'Authorization' not in request.headers or request.headers['Authorization'] != f"Bearer {AUTH_KEY}":
        return jsonify({'error': 'Unauthorized'}), 401
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file:
        filename = str(random.randint(1000000, 9999999999999999)) + ".jpg"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'success': 'File uploaded successfully', 'filename': filename})
  except Exception:
      print(traceback.format_exc)

@app.route('/uploads/<filename>', methods=['GET'])
def get_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(host="0.0.0.0",debug=True)

