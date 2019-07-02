import os
from flask import Flask, render_template, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from pixelate import pixelate, NeedleSizes, YarnSizes
from generate_instructions import generate_instructions
from get_color_link import get_color_link

UPLOAD_FOLDER = 'input'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])

app = Flask(__name__)
app.secret_key = 'A0Z85gc3/g/gHH!jmN]LWX/,?RT'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        size = request.form['size']
        yarn_type = request.form['yarn_type']

        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return original image template, that template has js that makes a request for pixelate stuff
            output, colors = pixelate(os.path.join(app.config['UPLOAD_FOLDER'], filename), yarn_type, size)
            instructions = generate_instructions(output, colors)
            color_link = get_color_link(colors)
            return render_template('instructions.html', src=url_for('uploaded_file', filename=filename), output=output, instructions=instructions, colors=colors, needle_size=NeedleSizes[yarn_type], color_link=color_link, gauge=int(YarnSizes[yarn_type].value))
    return render_template('form.html')


@app.route('/input/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

# @app.route('/instructions')
# def pattern(filename, output, instructions, colors, needle_size, color_link):
#     return render_template('instructions.html', src=url_for('uploaded_file', filename=filename), output=output, instructions=instructions, colors=colors, needle_size=needle_size, color_link=color_link)
