from flask import Flask, render_template, request, send_from_directory
from kohd_glyphs import generate_kohd_word
import os

app = Flask(__name__)
CACHE_DIR = 'static/pngs'
os.makedirs(CACHE_DIR, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    png_paths = []
    if request.method == 'POST':
        sentence = request.form['sentence']
        words = sentence.upper().split()
        for word in words:
            filepath = f"{CACHE_DIR}/{word}.png"
            if not os.path.exists(filepath):
                generate_kohd_word(word, filepath)
            png_paths.append(filepath)
    return render_template('index.html', images=png_paths)

@app.route('/static/pngs/<filename>')
def serve_image(filename):
    return send_from_directory(CACHE_DIR, filename)
