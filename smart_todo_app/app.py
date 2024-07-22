from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import create_db


# initialize app
app = Flask(__name__)

# Direct SQLALCHEMY to connect to mysql database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/Tasks_app'
# Disable modification tracking for SQLALCHEMY 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Initialize SQLALCHEMY with flask app 
db = SQLAlchemy(app)


class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    goal = db.Column(db.String(100))
    done = db.Column(db.Boolean, default=False)

#create route
@app.route('/')
def welcome():
    #Display all the contents of the task table and pass result to htmljj template
    errand_list = Tasks.query.all()
    return render_template("index.html", errand_list=errand_list)

@app.route("/add", methods=["POST"])
def add():
    goal = request.form.get("goal")
    new_entry = Tasks(goal=goal, done=False)
    db.session.add(new_entry)
    db.session.commit()
    return redirect(url_for("welcome"))

@app.route("/update/<int:errand_id>")
def update(errand_id):
    errand = Tasks.query.filter_by(id=errand_id).first()
    if errand:
        errand.done = not errand.done
        db.session.commit()
    return redirect(url_for("welcome"))

@app.route("/delete/<int:errand_id>")
def delete(errand_id):
    errand = Tasks.query.filter_by(id=errand_id).first()
    if errand:
        db.session.delete(errand)
        db.session.commit()
    return redirect(url_for("welcome"))


if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("Database tables created successfully")
    app.run(debug=True)