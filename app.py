from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(500), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.id} - {self.title}"

@app.route('/', methods=['GET','POST'])
def hello_world():
    # return 'Hello, World!'
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        todo = ToDo(title = title, desc = desc)
        db.session.add(todo)
        db.session.commit()

    allToDo = ToDo.query.all()
    return render_template('index.html', allToDo=allToDo)


@app.route('/update/<int:id>', methods=['GET','POST']) 
def update(id):
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        todo = ToDo.query.filter_by(id=id).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo = ToDo.query.filter_by(id=id).first()
    return render_template('update.html', todo=todo)

@app.route('/delete/<int:id>')
def delete(id):
    delete = ToDo.query.filter_by(id=id).first()
    db.session.delete(delete)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

