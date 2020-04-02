#! /usr/bin/env python
# encoding: utf-8

from flask import Blueprint, current_app, request, jsonify, redirect, url_for, flash
from flask import render_template
from flask_login import current_user
from .models import Question, Answer, Comment
from ..dbs import db

qa = Blueprint('qa', __name__, url_prefix='')


@qa.route('/add')
def add_question():
    return render_template('qa/ask_question.html')


@qa.route('/question', methods=['POST', 'GET'])
def question_info():
    try:
        if request.method == 'POST':
            if not current_user.is_authenticated:
                return jsonify(status='error', info='You are not login')
            question_instance = Question.query.filter(Question.name == request.form['title']).first()
            if question_instance:
                return jsonify(status='error', info=u'该问题已经发表')
            else:
                question_instance = Question()
                question_instance.author_id = current_user.id
                question_instance.name = request.form['title']
                question_instance.content = request.form['content']

                db.session.add(question_instance)
                db.session.commit()
                return jsonify(status='success', info='question create successfully')

        else:
            question_list = Question.query.filter().all()
            return render_template('qa/questions.html', qss=question_list)

    except Exception as e:
        current_app.logger.error(e)
        flash('Unknown system error: %s' % e, 'error')
        return redirect(url_for('qa.index'))


@qa.route('/<int:question_id>', methods=['POST', 'GET'])
def questions(question_id):
    try:
        if request.method == 'GET':
            question_instance = Question.query.filter(Question.id == question_id).first()
            if question_instance:
                return render_template('qa/question_detail.html', qs=question_instance)
            flash('Question not exist')
            return redirect(url_for('qa.index'))
        else:
            # 编辑Question
            pass

    except Exception as e:
        current_app.logger.error(e)
        return redirect(url_for('qa.index'))


@qa.route('/<int:question_id>/answer', methods=['POST'])
def add_answer(question_id):
    try:
        if not current_user.is_authenticated:
            return jsonify(status='error', info='You are not login')
        question_instance = Question.query.filter(Question.id == question_id).first()
        if not question_instance:
            return jsonify(status='error', info='Question not existing')
        else:
            if request.form['rtype'] == '1':
                """
                回答问题
                """
                answer_instance = Answer()
                answer_instance.content = request.form['content']
                answer_instance.author_id = current_user.id
                answer_instance.question_id = question_id
                question_instance.answers_count += 1
                db.session.add(question_instance)
                db.session.add(answer_instance)
            elif request.form['rtype'] == '2':
                """
                评论回答
                """
                answer_instance = Answer.query.filter(Answer.id == request.form['rid']).first()
                if not answer_instance:
                    return jsonify(status='error', info='Answer not existing')
                comment_instance = Comment()
                comment_instance.content = request.form['content']
                comment_instance.author_id = current_user.id
                comment_instance.answer_id = answer_instance.id
                answer_instance.comments_count += 1
                db.session.add(answer_instance)
                db.session.add(comment_instance)

            else:
                return jsonify(status='error', info='Wrong request type')
            db.session.commit()
            return jsonify(status='success', info='reply successfully')
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(status='error', info='add answer failed')


@qa.route('/<title>')
@qa.route('/', defaults={'title': None})
def index(title):
    return render_template('qa/index.html', current_user=current_user)
