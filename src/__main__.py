import math
import os

import flask
from bson import ObjectId
from flask import Flask, render_template, request, redirect, flash, url_for

import datetime

from werkzeug.utils import secure_filename

from src import db, env
from src.db import count_kategorije, count_tagi, is_admin


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in env.ALLOWED_EXTENSIONS


app = Flask(__name__)

app.secret_key = env.SECRET_KEY
app.config['UPLOAD_FOLDER'] = env.UPLOAD_FOLDER


@app.route("/")
def get_index():
    return render_template('index.html')


@app.route("/avtor")
def get_avtor():
    return render_template('avtor.html')


@app.route("/blog")
def get_blog():
    page = int(request.args.get('page', 1))
    posts_per_page = 10

    total_posts = db.this.objave.count_documents({})
    total_pages = math.ceil(total_posts / posts_per_page)

    start_index = (page - 1) * posts_per_page
    end_index = start_index + posts_per_page

    objave = list(db.this.objave.find().sort('_id', -1).skip(start_index).limit(posts_per_page))

    return render_template('blog.html', objave=objave, kategorije=count_kategorije(objave), tagi=count_tagi(objave),
                           page=page, total_pages=total_pages)


# FIND ONE Blog by ID
@app.route("/blog/<_id>", methods=['GET', 'POST'])
def get_blog_id(_id):
    post = db.this.objave.find_one({'_id': ObjectId(_id)})
    return render_template('blog_id.html', objava=post)


@app.route('/search', methods=['POST'])
def search():
    search = request.form['search']
    najdene = []
    objave = list(db.this.objave.find())
    for o in objave:
        for key in o:
            if key in ['_id', 'ustvarjeno']:
                continue
            if search in o[key]:
                najdene.append(o)
                break
    return render_template("blog.html", objave=najdene, kategorije=count_kategorije(objave), tagi=count_tagi(objave))


@app.route("/blog/kategorije/<kategorija>", methods=['GET'])
def get_blog_kategorija(kategorija):
    objave = list(db.this.objave.find())
    najdene = []
    for o in objave:
        if kategorija in o['kategorije']:
            najdene.append(o)
    return render_template('blog.html', objave=najdene, kategorije=count_kategorije(objave))


@app.route("/blog/tagi/<tag>", methods=['GET'])
def get_blog_tag(tag):
    objave = list(db.this.objave.find())
    najdene = []
    for o in objave:
        if tag in o['tagi']:
            najdene.append(o)
    return render_template('blog.html', objave=najdene, tagi=count_tagi(objave))


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
        tag = request.form['tagi']
        ustvarjeno = datetime.datetime.now()
        kategorije = request.form['kategorije']

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
        db.this.objave.update_one(
            {'_id': ObjectId(_id)},
            {
                '$set': {
                    'vsebina': vsebina,
                    'opis': opis,
                    'podnaslov': podnaslov,
                    'naslov': naslov,
                    'tagi': tag,
                    'image_filename': filename,
                    'ustvarjeno': ustvarjeno,
                    'kategorije': kategorije
                }
            }
        )
        return redirect(url_for('get_blog_id', _id=_id))

    return render_template('edit_blog.html', objava=post)


@app.route("/arhiv")
def get_arhiv():
    return render_template('arhiv.html', arhiv_objave=db.this.objave.find())


@app.route("/login", methods=['POST'])
def post_login():
    ime = request.form['ime'].strip()
    geslo = request.form['geslo'].strip()
    if not is_admin(ime, geslo):
        return get_login()

    flask.session['ime'] = ime
    flask.session['geslo'] = geslo

    return redirect('/admin')


@app.route("/login")
def get_login():
    return render_template('login.html')


@app.route("/admin", methods=['GET', 'POST'])
def get_admin():
    ime = flask.session.get('ime', None)
    geslo = flask.session.get('geslo', None)

    if not is_admin(ime, geslo):
        return get_login()

    objave = db.this.objave.find()

    if request.method == 'POST':
        vsebina = request.form['vsebina']
        opis = request.form['opis']
        podnaslov = request.form['podnaslov']
        naslov = request.form['naslov']
        tag = request.form['tagi']
        kategorije = request.form['kategorije']
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
                'image_filename': filename,
                'tagi': tag,
                'ustvarjeno': ustvarjeno,
                'kategorije': kategorije
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
    app.run(host='0.0.0.0', port=8001, debug=True)
