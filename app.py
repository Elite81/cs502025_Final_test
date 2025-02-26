from flask import Flask, render_template, url_for, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy 
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from sqlalchemy.orm import sessionmaker, Session
from werkzeug.security import check_password_hash
from models import * 
from sqlalchemy import create_engine

# Create a session
# session = Session(bind=engine)

app = Flask(__name__)
# engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
# Session = sessionmaker(engine)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
db = SQLAlchemy(model_class=Base)
db.init_app(app)
migrate = Migrate(app, db)

@app.context_processor
def inject_variables():
    subjects = []
    stages =[]
    
    all_current_subjects = db.session.execute(db.select(Subjects)).scalars().all()
    for subject in all_current_subjects:
        subjects.append(subject.name)

    all_current_stages = db.session.execute(db.select(Stages)).scalars().all()
    for stage in all_current_stages:
        stages.append(stage.name)
    return dict(subjects=subjects, stages=stages)





@app.route("/")
def home():
    
    
    return render_template("base.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        message = "Invalid username or password"
        print(username, password)

        if username and password:
            user = db.session.query(User).filter_by(username=username.lower()).first()
            print(user)
            try:
                if user and check_password_hash(user._password, password):
                    return render_template("base.html")
                
            except AttributeError:
                return render_template("login.html", message=message)
            
        return render_template("login.html", message=message)
    
    else:
        return render_template("login.html")


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
        print(new_user)
        db.session.add(new_user)
        db.session.commit()
        return url_for("login")
    


@app.route("/questions", methods=["GET", "POST"])
def questions():

    return render_template("questions.html")




@app.route("/class", methods=["GET", "POST"])
def stages():
    if request.method == 'POST':
        new_stage = request.form.get("stage", "")
        available_stages = db.session.execute(db.select(Stages)).scalars().all()
        
        if new_stage:
            for stage in available_stages:
                if new_stage.title() == stage.name:
                    return render_template("stage.html", message="Sorry, Stage Already exist")
            new_stage = new_stage.split()
            new_stage = " ".join([new_stage[0].title(), new_stage[1].upper()])
            new_stage = Stages(name=new_stage)
            db.session.add(new_stage)
            db.session.commit()
        return render_template("stage.html")
    
    else:
        return render_template("stage.html")
    

@app.route("/subject", methods=["GET", "POST"])
def subjects():
    if request.method == 'GET':
        return render_template("subject.html")
    else:
        new_subject = request.form.get("subject", "")

        if new_subject:
           all_current_subjects = db.session.execute(db.select(Subjects)).scalars().all()
           for subject in all_current_subjects:
            if new_subject.title() == subject.name:
                return render_template("subject.html", message="Subject already Available")
            
            new_subject = Subjects(name=new_subject.title())
            db.session.add(new_subject)
            db.session.commit()
        return render_template("subject.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print(all)