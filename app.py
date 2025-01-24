from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai
import os
import tempfile

app = Flask(__name__)
CORS(app)

# Configure Gemini API
genai.configure(api_key="AIzaSyBtpKzAxx2pwMQ1eMO_jtRxk28rRaglVc0")

# Define the / route to serve the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Define the /predict route to handle the image upload
@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    try:
        # Save the file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            image_path = temp_file.name
            image_file.save(image_path)

        # Run analysis using Gemini API
        uploaded_file = genai.upload_file(path=image_path, display_name="Uploaded Image")
        model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")
        prompt = "give me only descriptiopn of book only in one line."
        response = model.generate_content([uploaded_file, prompt])

        # Clean up temporary file
        os.remove(image_path)

        if response and response.text:
            return jsonify({"result": response.text}), 200
        else:
            return jsonify({"error": "Failed to analyze the image."}), 500

    except Exception as e:
        return jsonify({"error": f"Error processing image: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
