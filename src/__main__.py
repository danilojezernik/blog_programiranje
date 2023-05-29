from bson import ObjectId
from flask import Flask, render_template

from src import db

app = Flask(__name__)


@app.route("/")
def get_index():
    return render_template('index.html')


@app.route("/blog")
def get_blog():
    return render_template('blog.html', objave=db.this.objave.find())


@app.route("/blog/<_id>")
def get_blog_id(_id):
    return render_template('blog_id.html', objava=db.this.objave.find_one(ObjectId(_id)))


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404

if __name__ == '__main__':
    # db.drop()
    # db.seed()
    app.run(host='0.0.0.0', port='8001', debug=True)