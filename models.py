from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, String, DateTime, Boolean, Float, Integer
from sqlalchemy import Enum as SQLAlchemyEnum
from werkzeug.security import generate_password_hash, check_password_hash
from enum import Enum
from typing import List, Optional
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime, timezone


# Avalable roles
class Role(Enum):
    TEACHER = "teacher"
    STUDENT = "student"
    ADMIN = "admin"


class Gender(Enum):
    MALE = "male"
    FEMALE = "female"


class Base(DeclarativeBase):
    pass


# The user to keep record for allthose loged in
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(64), unique=True)
    first_name: Mapped[Optional[str]] = mapped_column(String(64))
    last_name: Mapped[Optional[str]] = mapped_column(String(64))
    gender: Mapped[Gender] = mapped_column(SQLAlchemyEnum(Gender), nullable=False)
    email_address: Mapped[str] = mapped_column(String(128), unique=True)
    _password: Mapped[str] = mapped_column(String(256), nullable=False)
    role: Mapped[Role] = mapped_column(
        SQLAlchemyEnum(Role), nullable=False, default=Role.STUDENT
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
   
    @property
    #Preventing reading the password directly
    def password(self):
        raise AttributeError("Password is not readable")

    @password.setter
    #Hash the password before storing it.
    def password(self, raw_password):
        self._password = generate_password_hash(raw_password, method="pbkdf2:sha512")

    def check_password(self, password):
        #Verify the passord again stored hash.
        return check_password_hash(self._password, password)

    def __repr__(self) -> str:
        return f"User(username={self.username!r}, role={self.role!r}"


# The subjects you can have many subject as you want
class Subjects(Base):
    __tablename__ = "subjects"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), unique=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self) -> str:
        return f"Subject(id={self.id!r}), name={self.name!r}"


# Stages_available per questions
class Stages(Base):
    __tablename__ = "stages"
    id: Mapped[int] = mapped_column(primary_key=True)
    questions_id: Mapped[List["Questions"]] = relationship(
        "Questions", secondary="question_stages", back_populates="stages"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )


# Bridge Table (Question -Stages)
class QuestionStages(Base):
    __tablename__ = "question_stages"
    id: Mapped[int] = mapped_column(primary_key=True)
    questions_id: Mapped[int] = mapped_column(ForeignKey("questions.id"))
    stage_id: Mapped[int] = mapped_column(ForeignKey("stages.id"))


# Just create a quiz
class Quizzes(Base):
    __tablename__ = "quizzes"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(64), unique=True)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"), index=True)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    num_questions: Mapped[int] = mapped_column(Integer, nullable=False, default=10)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self) -> str:
        return f"{self.title!r} Quiz)"


# pool of questions set by a teacher
class Questions(Base):
    __tablename__ = "questions"
    id: Mapped[int] = mapped_column(primary_key=True)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"), index=True)
    # quiz_id: Mapped[int] = mapped_column(ForeignKey("quizzes.id"))
    stages: Mapped[List["Stages"]] = relationship(
        "Stages", secondary="question_stages", back_populates="questions_id"
    )
    question_text: Mapped[str] = mapped_column(String(512), unique=True)
    options: Mapped[List["Options"]] = relationship(
        "Options", back_populates="question"
    )
    answer_text: Mapped[str] = mapped_column(String(256))
    answer_explained: Mapped[Optional[str]] = mapped_column(String(256))
    question_type: Mapped[bool] = mapped_column(
        Boolean, default=False
    )  # MCQ or True/False
    teacher_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), index=True
    )  # Teacher who set the question
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )


class Options(Base):
    __tablename__ = "options"
    id: Mapped[int] = mapped_column(primary_key=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"), index=True)
    question: Mapped["Questions"] = relationship(
        "Questions", back_populates=("options")
    )
    question_options: Mapped[str] = mapped_column(String(256))


# This is the bridge between quiz and questions
class QuizQuestions(Base):
    __tablename__ = "quiz_questions"
    id: Mapped[int] = mapped_column(primary_key=True)
    quiz_id: Mapped[int] = mapped_column(ForeignKey("quizzes.id"), index=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"), index=True)
    answer_provided: Mapped[str] = mapped_column(String(16), default=None)
    time_taken: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )


# The result of the quiz
class QuizResult(Base):
    __tablename__ = "quiz_result"
    id: Mapped[int] = mapped_column(primary_key=True)
    quiz_questions_id: Mapped[int] = mapped_column(
        ForeignKey("quiz_questions.id"), index=True
    )
    student_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    score: Mapped[float] = mapped_column(Float, default=None)
    remarks: Mapped[str] = mapped_column(String(128))
    taken_on: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )


class StudentQuizzes(Base):
    __tablename__ = "student_quizzes"
    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    quiz_id: Mapped[int] = mapped_column(ForeignKey("quizzes.id"), index=True)
    quiz_result_id: Mapped[int] = mapped_column(ForeignKey("quiz_result.id"))

    def __repr__(self) -> str:
        return f"{self.student_id.username!r} Quiz)"
