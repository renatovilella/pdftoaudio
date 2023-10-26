import os
import PyPDF2
import pyttsx3
from flask import Flask, render_template, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('process_file', filename=filename))
    return redirect(request.url)

@app.route('/process/<filename>')
def process_file(filename):
    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    text = extract_text_from_pdf(pdf_path)
    audio_file = convert_text_to_audio(text)
    return send_file(audio_file, as_attachment=True)

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)  # Change PdfFileReader to PdfReader
        for page_num in range(len(pdf_reader.pages)):  # Change numPages to pages
            text += pdf_reader.pages[page_num].extract_text()
    return text

def convert_text_to_audio(text):
    audio_file = os.path.join('audiofile', 'output.mp3')  # Save audio in 'audiofile' folder
    engine = pyttsx3.init()
    engine.save_to_file(text, audio_file)
    engine.runAndWait()
    return audio_file

if __name__ == '__main__':
    app.run()
