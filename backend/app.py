from flask import Flask, request, jsonify
from flask_cors import CORS  # For handling CORS issues
from chatbot_model import IntentClassifier
import os
from PIL import Image
import io

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Initialize the IntentClassifier
classifier = IntentClassifier()

# Folder where uploaded files will be stored
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Allowed file extensions (image, text, etc.)
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Get the user's message from the request
        user_input = request.json.get("message", "")
        if not user_input:
            return jsonify({"error": "No message provided"}), 400

        # Predict the response using the classifier
        response = classifier.predict_intent(user_input)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Check if the file is part of the request
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        
        if file and allowed_file(file.filename):
            # Save the file to the server
            filename = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filename)

            # Process the file based on its type (image, text, etc.)
            if filename.endswith(('jpg', 'jpeg', 'png', 'gif')):
                # Open image using PIL for analysis (you can add custom image analysis here)
                img = Image.open(filename)
                img.show()  # For now, just display the image
                return jsonify({"response": "Image successfully uploaded and analyzed."})
            
            if filename.endswith(('txt', 'pdf')):
                # For text files, read the content
                with open(filename, 'r') as f:
                    file_content = f.read()
                return jsonify({"response": f"Text file successfully uploaded. First 100 characters: {file_content[:100]}..."})
            
            return jsonify({"error": "Unsupported file type"}), 400
        else:
            return jsonify({"error": "File not allowed"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
