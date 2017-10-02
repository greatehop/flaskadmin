import os
import os.path as op
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#from wtforms import validators

import flask_admin as admin
from flask_admin.contrib import sqla
#from flask_admin.contrib.sqla import filters


app = Flask(__name__)
app.config['SECRET_KEY'] = '123456790'
app.config['DATABASE_FILE'] = 'appdb.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_FILE']
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class Server(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(15), index=True, unique=True)
    desc = db.Column(db.String(120))
    state = db.Column(db.Boolean, default=True, nullable=False)


@app.route('/')
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'

admin = admin.Admin(app, name='Manager', template_mode='bootstrap3')
admin.add_view(sqla.ModelView(Server, db.session))


if __name__ == '__main__':

    app_dir = op.realpath(os.path.dirname(__file__))
    database_path = op.join(app_dir, app.config['DATABASE_FILE'])
    if not os.path.exists(database_path):
        db.create_all()

    app.run(debug=True)
