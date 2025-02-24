from flask import Flask, render_template, url_for, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy 
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from sqlalchemy.orm import sessionmaker
from models import * 
from sqlalchemy import create_engine


app = Flask(__name__)
# engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
# Session = sessionmaker(engine)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
db = SQLAlchemy(model_class=Base)
db.init_app(app)
migrate = Migrate(app, db)






@app.route("/")
def home():
    return render_template("base.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        return render_template("login.html")
    else:
        return url_for("home")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    
    else:
        first_name = request.form.get("first_name", "")
        last_name = request.form.get("last_name", "")
        gender = request.form.get("gender", "")
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        email_address = request.form.get("email_address", "")
        new_user = User(first_name=first_name, last_name=last_name, username=username, gender=gender.upper(), password=password, email_address=email_address)
        db.session.add(new_user)
        db.session.commit()
        return url_for("login")



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print(all)