#-*- coding:utf-8 -*-
import sys
import os

reload(sys)
sys.setdefaultencoding('utf-8')

from flask import Flask, render_template_string, redirect,render_template
basedir = os.path.abspath(os.path.dirname(__file__))
from sqlalchemy import create_engine, MetaData
from flask.ext.login import UserMixin, LoginManager, \
    login_user, logout_user
from flask.ext.blogging import SQLAStorage, BloggingEngine

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"  # for WTF-forms and login
app.config["BLOGGING_URL_PREFIX"] = "/blog"
app.config["BLOGGING_SITENAME"] ="天天learning"
app.config["BLOGGING_SITEURL"] = "http://zhangliangchun.com"

# extensions
engine = create_engine('sqlite:///' + os.path.join(basedir, 'data.db'))
meta = MetaData()
sql_storage = SQLAStorage(engine, metadata=meta)
blog_engine = BloggingEngine(app, sql_storage)
login_manager = LoginManager(app)
meta.create_all(bind=engine)

# user class for providing authentication
class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

    def get_name(self):
        return "天天learning"  # typically the user's name

@login_manager.user_loader
@blog_engine.user_loader
def load_user(user_id):
    return User(user_id)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/hardtoguess/")
def login():
    user = User("zlc")
    login_user(user)
    return redirect("/blog")

@app.route("/logout/")
def logout():
    logout_user()
    return redirect("/")

@app.route("/contact/")
def contact():
    return render_template("contact.html")

@app.errorhandler(404)
def page_not_found(error):
	return render_template('404.html'),404
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, use_reloader=True)
