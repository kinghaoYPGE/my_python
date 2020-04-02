from datetime import datetime

from sqlalchemy import Column

from ..dbs import db


class Question(db.Model):
    """
    Question模型
    """
    __tablename__ = 'questions'

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(128), nullable=False)
    content = Column(db.Text(1024))
    answers_count = Column(db.Integer, default=0)
    create_time = Column(db.DateTime, default=datetime.now)
    # 一对多双向关联
    author_id = Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    author = db.relationship('User', backref=db.backref('questions', lazy='dynamic'),
                             uselist=False)


class Answer(db.Model):
    """
    回答模型
    """
    __tablename__ = 'answers'

    id = Column(db.Integer, primary_key=True)
    content = Column(db.Text(1024))
    comments_count = Column(db.Integer, default=0)
    create_time = Column(db.DateTime, default=datetime.now)
    author_id = Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    author = db.relationship('User', backref=db.backref('answers', lazy='dynamic'),
                             uselist=False)
    question_id = Column(db.Integer, db.ForeignKey('questions.id'))
    question = db.relationship('Question', backref=db.backref('answers', lazy='dynamic'),
                               uselist=False)


class Comment(db.Model):
    __tablename__ = 'comments'
    id = Column(db.Integer, primary_key=True)
    content = Column(db.Text(1024))
    create_time = Column(db.DateTime, default=datetime.now)
    author_id = Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    author = db.relationship('User', backref=db.backref('comments', lazy='dynamic'),
                             uselist=False)
    answer_id = Column(db.Integer, db.ForeignKey('answers.id'))
    answer = db.relationship('Answer', backref=db.backref('answers', lazy='dynamic'),
                             uselist=False)
