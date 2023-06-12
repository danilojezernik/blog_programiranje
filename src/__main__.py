import os

from bson import ObjectId
from flask import Flask, render_template, request, redirect, flash
import datetime

from werkzeug.utils import secure_filename

from src import db

UPLOAD_FOLDER = 'static/blog'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
def get_index():
    return render_template('index.html')


@app.route("/avtor")
def get_avtor():
    return render_template('avtor.html')


@app.route("/blog")
def get_blog():
    objave = db.this.objave.find()
    return render_template('blog.html', objave=objave)


@app.route("/blog/<_id>", methods=['GET', 'POST'])
def get_blog_id(_id):
    post = db.this.objave.find_one({'_id': ObjectId(_id)})
    return render_template('blog_id.html', objava=post)


@app.route("/arhiv")
def get_arhiv():
    return render_template('arhiv.html', arhiv_objave=db.this.objave.find())


@app.route("/login")
def get_login():
    return render_template('login.html')


@app.route("/admin", methods=['GET', 'POST'])
def get_admin():
    if request.method == 'POST':
        vsebina = request.form['vsebina']
        opis = request.form['opis']
        podnaslov = request.form['podnaslov']
        naslov = request.form['naslov']
        ustvarjeno = datetime.datetime.now()

        if 'image' in request.files:
            image = request.files['image']
            if image.filename != '':
                if allowed_file(image.filename):
                    filename = secure_filename(image.filename)
                    image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                else:
                    flash('Allowed image types are -> png, jpg, jpeg, gif')
                    return redirect(request.url)
            else:
                filename = None
        else:
            filename = None

        inserted_id = db.this.objave.insert_one(
            {
                'vsebina': vsebina,
                'opis': opis,
                'podnaslov': podnaslov,
                'naslov': naslov,
                'ustvarjeno': ustvarjeno.strftime("%Y-%m-%d %H:%M:%S"),
                'image_filename': filename
            }
        ).inserted_id
        return redirect('/blog/{}'.format(inserted_id))

    return render_template('admin.html')


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404


if __name__ == '__main__':
    db.drop()
    db.seed()
    app.run(host='0.0.0.0', port='8001', debug=True)
