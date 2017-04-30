import os

import sys
from flask import Flask, jsonify
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.utils import secure_filename, redirect
import sqlite3
import sql
import random

import ML

TITLES = ["", ""]
DESCS = ["", ""]

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
UPLOAD_FOLDER = "static"
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.databese = "sample.db"


def insert(future, present, past):
    conn = sqlite3.connect(app.databese)
    cur = conn.cursor()
    cur.execute("INSERT INTO {} ({},{},{}) VALUES (?, ?, ?)".format(sql.TABLE_NAME,
                                                                    sql.FUTURE_IMG_COLUMN,
                                                                    sql.PRESENT_IMG_COLUMN,
                                                                    sql.PAST_IMG_COLUMN), (future, present, past))
    conn.commit()
    conn.close()


def get_data():
    conn = sqlite3.connect(app.databese)
    cur = conn.cursor()
    cur.execute("SELECT * FROM {}".format(sql.TABLE_NAME))
    data = cur.fetchall()
    conn.close()
    return data


@app.route('/', methods=['GET'])
def home():
    x = str(random.randint(1, 5))
    first_img = "static/imgs/{}-1.jpg".format(x)
    second_img = "static/imgs/{}-2.jpg".format(x)
    return render_template("index.html", first_img = first_img, second_img = second_img)


@app.route('/ml', methods=['GET'])
def ml():
    before_image = request.args.get('before_image')
    after_image = request.args.get('after_image')
    before_date = request.args.get('before_date')
    after_date = request.args.get('after_date')
    required_year = request.args.get('required_year')
    (predictions, ratio, before, after) = ML.final(before_image, after_image, before_date, after_date, required_year)
    data = {"prediction": predictions, "ratio": ratio, "before": before, "after": after}
    return jsonify(data)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file1 = request.files.get('file')
        file2 = request.files.get('file2')
        if file1.filename == '' or file2.filename == '':
            return jsonify({'status': "fail", "error": "no file selected", "code": 444})
        filename = ""
        filename2 = ""
        if file1 and allowed_file(file1.filename):
            filename = secure_filename(file1.filename)
            file1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        if file2 and allowed_file(file2.filename):
            filename2 = secure_filename(file2.filename)
            file2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))

        (predict, ratio, before, after) = ML.final(UPLOAD_FOLDER + "/" + filename, UPLOAD_FOLDER + "/" + filename2)
        # c.execute("INSERT INTO {} ({}, {}, {})  VALUES ( ?, ?, ?);"
        #           .format(sql.TABLE_NAME, sql.PAST_IMG_COLUMN, sql.PRESENT_IMG_COLUMN, sql.FUTURE_IMG_COLUMN),
        #           (filename, filename2, str(predict)))
        return render_template('report.html', predict=predict,
                               ratio=ratio, past=UPLOAD_FOLDER + "/" + filename,
                               present=UPLOAD_FOLDER + "/" + filename2, before=before, after=after)
    return render_template('form.html')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    port = 5050
    app.run(host='0.0.0.0', port=port)

# INSERT INTO reports (past_img, present_img, future)  VALUES ( xxxxx,yyyyyyyyyy ,zzzzzzzzzz )
