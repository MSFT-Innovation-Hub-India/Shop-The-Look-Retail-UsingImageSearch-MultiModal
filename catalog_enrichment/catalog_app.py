from flask import Flask, request, jsonify, render_template_string
from generate_captions import process_dataset
import os

app = Flask(__name__)

UPLOAD_HTML = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Upload CSV</title>
</head>
<body>
    <h1>Upload a CSV file for Catalog Enrichment</h1>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit" value="Upload">
    </form>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(UPLOAD_HTML)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and file.filename.endswith('.csv'):
        try:
            file_path = os.path.join("/tmp", file.filename)
            file.save(file_path)
            df = process_dataset(file_path)
            result = df.to_dict(orient='records')
            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return jsonify({"error": "Invalid file format, only CSV files are allowed"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5329)
