import os
from io import BytesIO
from flask import Flask, request, render_template, send_file, flash, redirect, url_for
from PIL import Image
from mcjerseyskin import apply_jersey

app = Flask(__name__)
app.secret_key = os.urandom(24)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        skin_file = request.files.get('skin')
        jersey_file = request.files.get('jersey')
        if not skin_file or not allowed_file(skin_file.filename):
            flash('❗ Please upload a valid skin image.')
            return redirect(request.url)
        if not jersey_file or not allowed_file(jersey_file.filename):
            flash('❗ Please upload a valid jersey image.')
            return redirect(request.url)

        skin = Image.open(skin_file.stream).convert("RGBA")
        jersey = Image.open(jersey_file.stream).convert("RGBA")
        result = apply_jersey(skin, jersey)

        buf = BytesIO()
        result.save(buf, format='PNG')
        buf.seek(0)
        return send_file(buf, mimetype='image/png',
                         download_name='composited_skin.png',
                         as_attachment=True)

    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
