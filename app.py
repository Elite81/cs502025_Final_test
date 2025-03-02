from flask import Flask, render_template, url_for, request, jsonify, session
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy 
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from sqlalchemy.orm import sessionmaker
from werkzeug.security import check_password_hash
from models import * 
from sqlalchemy import create_engine
import secrets

# Create a session
# session = Session(bind=engine)

app = Flask(__name__)
# engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
# Session = sessionmaker(engine)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
# app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.secret_key = secrets.token_hex(64)
db = SQLAlchemy(model_class=Base)
db.init_app(app)
migrate = Migrate(app, db)

@app.context_processor
def subject_variables():
    subjects = []
    stages =[]
    
    all_current_subjects = db.session.execute(db.select(Subjects)).scalars().all()
    for subject in all_current_subjects:
        subjects.append(subject.name)

    all_current_stages = db.session.execute(db.select(Stages)).scalars().all()
    for stage in all_current_stages:
        stages.append(stage.name)
    return dict(subjects=subjects, stages=stages)

@app.route("/userIdSubjetId", methods=["GET", "POST"])
def stageIdSubjetId():
    data = request.get_json()
    stage = data['stage']
    subject_name = data['subject']
    stage = db.session.execute(db.select(Stages).filter_by(name=stage)).scalars().first()
    subject = db.session.execute(db.select(Subjects).filter_by(name=subject_name)).scalars().first()
    subjectId = subject.id
    stageId = stage.id
    print(subjectId)
    print(stageId)
    return jsonify({"stageId":stageId, "subjectId":subjectId})

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
                    session["user_id"] = user.id
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

@app.route("/new-question", methods=["POST"])
def new_questions():
    json_data = request.get_json()

    print(json_data)

    if not json_data:
        return jsonify({"error": "Invalid JSON data"}), 400
    
    elif not session.get("user_id"):
        return jsonify({"error": "User not authenticaed"})
    
    print(json_data["subjectId"])
    print("Hello")
    
    try:
        with db.session.begin():
            question_list = []
            option_list = []

            for i in range(len(json_data["questions"])):

                new_question = Questions(
                    subject_id = int(json_data["subjectId"]),
                    question_text = json_data["questions"][i],
                    answer_text = json_data["answers"][i],
                    answer_explained = json_data["answerExplain"][i],
                    question_type=False,
                    teacher_id = session.get("user_id")
                )
                print(new_questions)
                
                db.session.add(new_question)
                question_list.append(new_question)
            db.session.flush()  

            for q_index, question in enumerate(question_list):
                options = json_data["options"][q_index]
                print(options)

                if not isinstance(options, list):
                    return jsonify({"error":f"option for quetion {q_index}are invalid" })

                print(f"This is the Options: {options}")
                
                for option_text in options:
                    print(f"Adding option for Q{q_index}: {option_text}")
                    option_list.append(Options(question_id=question.id, question_options=option_text))

            db.session.bulk_save_objects(option_list)
        print("data saved with success")
        return jsonify({"message": "data saved with success"}), 201

# question=question,
    except Exception as e:
        db.session.rollback()
        print(f"Erreor: {e}")
        return jsonify({"error":str(e)}), 500

    
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print(all)