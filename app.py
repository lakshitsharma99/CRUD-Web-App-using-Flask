from email.policy import default
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///crud.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Crud(db.Model):
    sno = db.Column(db.Integer, primary_key = True )
    full_name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), nullable = False)
    mobile = db.Column(db.Integer, default="00", nullable = False)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.full_name} - {self.email}"

@app.route("/", methods = ['GET', 'POST'])
def hello_world():
    if request.method=="POST":
        fullname=request.form['fullname']
        email=request.form['email']
        mobile=request.form['mobile']
        todo = Crud(full_name=fullname, email=email, mobile=mobile)
        db.session.add(todo)
        db.session.commit()
    view = Crud.query.all()
    return render_template("index.html", view=view)

@app.route("/update/<int:sno>", methods = ['GET', 'POST'])
def update(sno):
    if request.method=="POST":
        fullname=request.form['fullname']
        email=request.form['email']
        mobile=request.form['mobile']
        todo = Crud.query.filter_by(sno=sno).first()
        todo.full_name=fullname
        todo.email=email
        todo.mobile=mobile
        db.session.commit()
        return redirect("/")

    todo = Crud.query.filter_by(sno=sno).first()
    return render_template("update.html", todo=todo)

@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Crud.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__=="__main__":
    app.run(debug=True)
