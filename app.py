from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#http://flask.pocoo.org/
#http://flask-sqlalchemy.pocoo.org/2.1/

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@127.0.0.1/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    finished = db.Column(db.INT)
    post_date = db.Column(db.DATETIME)

    def __init__(self, title):
        self.title = title
        self.finished = 0
        self.post_date = datetime.now()

    def __repr__(self):
        return '<Todo %r>' % self.title


@app.route('/')
def index():
    todos = Todo.query.all()
    return render_template('index.html', site_name="TODO List", todos=todos)


@app.route('/todo/new', methods=['POST'])
def add():
    todo = Todo(request.form['title'])
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/todo/<int:id>/edit')
def edit(id):
    todo = Todo.query.filter_by(id=id).first()
    return render_template('edit.html', site_name="TODO List", todo=todo)


@app.route('/todo/<int:id>/save', methods=['POST'])
def save(id):
    todo = Todo.query.filter_by(id=id).first()
    todo.title = request.form['title']
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/todo/<int:id>/delete')
def delete(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/todo/<int:id>/finish/<int:finished>')
def finish(id, finished):
    todo = Todo.query.filter_by(id=id).first()
    todo.finished = finished
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
