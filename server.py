from werkzeug.utils import secure_filename
import os
from flask import Flask, request, render_template
import requests
from flask_restful import reqparse, abort, Api, Resource
import pandas as pd
import json

UPLOAD_FOLDER = "./upload/"
ALLOWED_EXTENSIONS = {'xlsx'}

app = Flask(__name__)
api = Api(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/handle_form', methods=['POST'])
def handle_form():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(
            app.config['UPLOAD_FOLDER'], filename))

        # snippet to read code below
        file.stream.seek(0)  # seek to the beginning of file
        # myfile = file.file  # will point to tempfile itself
        w = pd.read_excel(UPLOAD_FOLDER+filename)
        #       budget_dict = {}
        wb = w.columns
        n = {}
        y = {}

        for i in range(len(w[wb[1]])):
            for j in wb:
                y[j] = str(w[j][i])
            n[str(i)] = y
        n = json.dumps(n, skipkeys=True, ensure_ascii=False, indent=4)

        return n
    else:
        return "wrong"


if __name__ == '__main__':
    app.run(debug=True)
