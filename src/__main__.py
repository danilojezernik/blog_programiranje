from bson import ObjectId
from flask import Flask, render_template, request

from src import db

app = Flask(__name__)


@app.route("/")
def get_index():
    return render_template('index.html')


@app.route("/avtor")
def get_avtor():
    return render_template('avtor.html')


@app.route("/blog")
def get_blog():
    objave = db.this.objave.find().limit(5)
    return render_template('blog.html', objave=objave)


@app.route("/blog/<_id>")
def get_blog_id(_id):
    return render_template('blog_id.html', objava=db.this.objave.find_one(ObjectId(_id)))


@app.route("/arhiv")
def get_arhiv():
    return render_template('arhiv.html', arhiv_objave=db.this.objave.find())


@app.route("/kontakt")
def get_kontakt():
    return render_template('kontakt.html')


@app.route("/admin")
def get_admin():
    return render_template('admin.html')


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404


if __name__ == '__main__':
    db.drop()
    db.seed()
    app.run(host='0.0.0.0', port='8001', debug=True)
