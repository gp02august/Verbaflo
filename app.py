from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
from werkzeug.utils import secure_filename
import os
import openai
import PyPDF2
from dotenv import load_dotenv
import time
from openai.error import RateLimitError

app = Flask(__name__)

# Load OpenAI API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Path to store uploaded files
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allow only PDFs
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for handling file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return redirect(url_for('generate_resume', filename=filename))
    return 'Invalid file type'

# Route to generate HTML resume
@app.route('/generate/<filename>', methods=['GET'])
def generate_resume(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    # Extract text from PDF
    try:
        with open(file_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            text = ''
            for page in reader.pages:
                text += page.extract_text()
    except Exception as e:
        return f'Error reading PDF file: {e}'

    # Call OpenAI API to convert text to HTML resume
    max_retries = 5
    for attempt in range(max_retries):
        try:
            response = openai.Completion.create(
                model="gpt-3.5-turbo",  # Use the appropriate model
                prompt=f"Convert the following resume into an HTML format:\n\n{text}",
                max_tokens=1500
            )
            html_resume = response['choices'][0]['text']
            break
        except RateLimitError:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                return jsonify({"error": "Rate limit exceeded. Please try again later."}), 429
        except Exception as e:
            return jsonify({"error": f"An error occurred: {e}"}), 500

    # Save the generated HTML
    html_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename.replace('.pdf', '.html'))
    try:
        with open(html_file_path, 'w') as html_file:
            html_file.write(html_resume)
    except Exception as e:
        return f'Error saving HTML file: {e}'

    return send_file(html_file_path, as_attachment=True)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
