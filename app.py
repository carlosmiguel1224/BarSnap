from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from pipelinetest4 import *  # image_to_results()


load_dotenv()

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv("API_KEY_GOOGLE")
EXPECTED_SECRET = os.getenv("API_AUTH_SECRET")

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/api/process-image', methods=['POST'])
def process_image():
    client_secret = request.headers.get("X-APP-SECRET")
    if client_secret != EXPECTED_SECRET:
        return jsonify({"error": "Unauthorized"}), 401

    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image = request.files['image']
    if image.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    filename = secure_filename(image.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(filepath)

    # Try to load user ingredients from form data
    user_ingredients = []
    if 'ingredients' in request.form:
        try:
            user_ingredients = json.loads(request.form['ingredients'])
            if not isinstance(user_ingredients, list):
                raise ValueError("ingredients must be a list")
        except Exception as e:
            return jsonify({"error": f"Invalid ingredients format: {str(e)}"}), 400

    try:
        # Pass user ingredients into image_to_results()
        results = image_to_results(filepath, API_KEY, user_ingredients)

        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        os.remove(filepath)  # Clean up temp file

# ---- Run the server ----
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)