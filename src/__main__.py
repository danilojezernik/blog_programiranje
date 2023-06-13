import os

from bson import ObjectId
from flask import Flask, render_template, request, redirect, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

import datetime

from werkzeug.utils import secure_filename

from src import db, env


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in env.ALLOWED_EXTENSIONS


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = env.UPLOAD_FOLDER
app.config['SECRET_KEY'] = env.SECRET_KEY


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


# FIND ONE Blog by ID
@app.route("/blog/<_id>", methods=['GET', 'POST'])
def get_blog_id(_id):
    post = db.this.objave.find_one({'_id': ObjectId(_id)})
    return render_template('blog_id.html', objava=post)


# DELETE Blog post by ID
@app.route('/blog/delete/<_id>')
def delete_blog(_id):
    db.this.objave.delete_one({'_id': ObjectId(_id)})
    return redirect(url_for('get_admin'))


# EDIT Blog post by ID
@app.route('/blog/edit/<_id>', methods=['GET', 'POST'])
def edit_blog(_id):
    post = db.this.objave.find_one({'_id': ObjectId(_id)})

    if request.method == 'POST':
        vsebina = request.form['vsebina']
        opis = request.form['opis']
        podnaslov = request.form['podnaslov']
        naslov = request.form['naslov']

        db.this.objave.update_one(
            {'_id': ObjectId(_id)},
            {
                '$set': {
                    'vsebina': vsebina,
                    'opis': opis,
                    'podnaslov': podnaslov,
                    'naslov': naslov
                }
            }
        )

        flash('Blog post updated successfully')
        return redirect(url_for('get_blog_id', _id=_id))

    return render_template('edit_blog.html', objava=post)


@app.route("/arhiv")
def get_arhiv():
    return render_template('arhiv.html', arhiv_objave=db.this.objave.find())


@app.route("/login")
def get_login():
    return render_template('login.html')


@app.route("/admin", methods=['GET', 'POST'])
def get_admin():
    objave = db.this.objave.find()

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
                'ustvarjeno': ustvarjeno,
                'image_filename': filename
            }
        ).inserted_id

        return redirect('/blog/{}'.format(inserted_id))

    return render_template('admin.html', objave=objave)


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404


if __name__ == '__main__':
    db.drop()
    db.seed()
    app.run(host='0.0.0.0', port='8001', debug=True)
