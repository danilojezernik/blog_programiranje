import base64
import os
from io import BytesIO

import flask
from PIL import Image
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


# BLOG all
@app.route("/blog")
def get_blog():
    page = int(request.args.get('page', 1))
    objave = list(db.this.objave.find().sort('_id', -1))
    page_objave, total_pages = db.objave_page(objave, page)

    return render_template('blog.html', route="/blog", objave_nakljucne=objave[-1:], objave=page_objave,
                           kategorije=count_kategorije(objave), tagi=count_tagi(objave),
                           page=page, total_pages=total_pages)


# FIND ONE Blog by ID
@app.route("/blog/<_id>", methods=['GET', 'POST'])
def get_blog_id(_id):
    post = db.this.objave.find_one({'_id': ObjectId(_id)})
    return render_template('blog_id.html', objava=post)


@app.route('/search', methods=['POST'])
def search():
    search = request.form['search']

    page = int(request.args.get('page', 1))
    objave = list(db.this.objave.find().sort('_id', -1))

    najdene = []
    for o in objave:
        for key in o:
            if key in ['_id', 'ustvarjeno']:
                continue
            if o[key] is not None and search in o[key]:
                najdene.append(o)
                break

    page_objave, total_pages = db.objave_page(najdene, page)
    return render_template("blog.html", route="/search", objave=page_objave, objave_nakljucne=objave[-1:],
                           kategorije=count_kategorije(objave), tagi=count_tagi(objave),
                           page=page, total_pages=total_pages)


# KATEGORIJE
@app.route("/blog/kategorije/<kategorija>", methods=['GET'])
def get_blog_kategorija(kategorija):
    page = int(request.args.get('page', 1))
    objave = list(db.this.objave.find().sort('_id', -1))

    najdene = []
    for o in objave:
        if kategorija in o['kategorije']:
            najdene.append(o)

    page_objave, total_pages = db.objave_page(najdene, page)

    return render_template('blog.html', route=f"/blog/kategorije/{kategorija}", objave_nakljucne=objave[-1:],
                           objave=page_objave, kategorije=count_kategorije(objave), tagi=count_tagi(objave),
                           page=page, total_pages=total_pages)


# TAGI
@app.route("/blog/tagi/<tag>", methods=['GET'])
def get_blog_tag(tag):
    page = int(request.args.get('page', 1))
    objave = list(db.this.objave.find().sort('_id', -1))

    najdene = []
    for o in objave:
        if tag in o['tagi']:
            najdene.append(o)

    page_objave, total_pages = db.objave_page(najdene, page)

    return render_template('blog.html', route=f"/blog/tagi/{tag}", objave=page_objave, objave_nakljucne=objave[-1:],
                           tagi=count_tagi(objave), kategorije=count_kategorije(objave),
                           page=page, total_pages=total_pages)


# DELETE Blog post by ID
@app.route('/blog/delete/<_id>')
def delete_blog(_id):
    db.this.objave.delete_one({'_id': ObjectId(_id)})
    return redirect(url_for('get_admin'))


# DELETE Many Blog posts by ID
@app.route('/blog/delete', methods=['POST'])
def delete_blog_many():
    selected_posts = request.form.getlist('izbrane_izbrisi')
    db.this.objave.delete_many({'_id': {'$in': [ObjectId(_id) for _id in selected_posts]}})
    return redirect(url_for('get_admin'))


# EDIT Blog post by ID
@app.route('/blog/edit/<_id>', methods=['GET', 'POST'])
def edit_blog(_id):
    post = list(db.this.objave.find({'_id': ObjectId(_id)}))[0]

    if request.method == 'POST':
        vsebina = request.form['vsebina']
        opis = request.form['opis']
        podnaslov = request.form['podnaslov']
        naslov = request.form['naslov']
        tag = request.form['tagi'].split()
        kategorije = request.form['kategorije'].split()
        ustvarjeno = datetime.datetime.now()
        imageData = None

        if 'image' in request.files:
            image = request.files['image']
            if image.filename != '':
                if allowed_file(image.filename):

                    image = request.files['image']
                    image_string = base64.b64encode(image.read())

                    imageData = f"data:image/png;base64,{image_string.decode()}"
                else:
                    return redirect(request.url)
        db.this.objave.update_one(
            {'_id': ObjectId(_id)},
            {
                '$set': {
                    'vsebina': vsebina,
                    'opis': opis,
                    'podnaslov': podnaslov,
                    'naslov': naslov,
                    'tagi': tag,
                    'ustvarjeno': ustvarjeno,
                    'kategorije': kategorije,
                    'slika': imageData
                }
            }
        )
        return redirect(url_for('get_admin'))

    post['tagi'] = " ".join(post['tagi'])
    post['kategorije'] = " ".join(post['kategorije'])
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
        tag = request.form['tagi'].split()
        kategorije = request.form['kategorije'].split()
        ustvarjeno = datetime.datetime.now()
        imageData = None

        if 'image' in request.files:
            image = request.files['image']
            if image.filename != '':
                if allowed_file(image.filename):

                    image = request.files['image']
                    image_string = base64.b64encode(image.read())

                    imageData = f"data:image/png;base64,{image_string.decode()}"
                else:
                    return redirect(request.url)
        inserted_id = db.this.objave.insert_one(
            {
                'vsebina': vsebina,
                'opis': opis,
                'podnaslov': podnaslov,
                'naslov': naslov,
                'tagi': tag,
                'ustvarjeno': ustvarjeno,
                'kategorije': kategorije,
                'slika': imageData
            }
        ).inserted_id

        return redirect('/blog/{}'.format(inserted_id))

    return render_template('admin.html', objave=objave)


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404


if __name__ == '__main__':
    # db.drop()
    # db.seed()
    app.run(host='0.0.0.0', port=env.PORT, debug=True)
