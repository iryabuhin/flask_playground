from flask import render_template, redirect, request, flash, url_for
from app import app, db, imgs
from app.db_models import User, Task
from app.forms import RegistrationForm, LoginForm, TaskSubmitForm
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime
from config import uploads_dir
import os


# TODO add the ability to allow users to set reminders on their tasks
# TODO allow users add images or other files to their tasks


@login_required
@app.route('/index')
@app.route('/', methods=['GET'])
def index():
    task_submit_form = TaskSubmitForm()

    if current_user.is_authenticated:
        tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.timestamp.desc()).all()
    else:
        flash('You have to log in to view your tasks!', category='danger')
        tasks = []

    return render_template('index.html', tasks=tasks, task_submit_form=task_submit_form)


@login_required
@app.route('/add', methods=['POST'])
def add_task():
    form = TaskSubmitForm()
    if form.validate_on_submit():
        if form.image.data:
            img_filename = imgs.save(form.image.data)
            img_url = imgs.url(img_filename)
        else:
            img_url = ''

        task = Task(name=form.text.data, timestamp=datetime.utcnow(), completed=False,
                    user_id=current_user.id, img_url=img_url)
        db.session.add(task)
        db.session.commit()
        flash('Task added!', category='warning')
        return redirect('/')


# TODO test "delete" and "edit" functions, add the "completed" function
@login_required
@app.route('/delete_task/<int:id>', methods=['GET'])
def delete_task(id):
    task = Task.query.filter_by(id=id).first_or_404()
    print()
    filename = task.img_url
    full_path_to_img = os.path.join(uploads_dir, filename[filename.find('images'):]).replace('/', '\\')
    try:
        os.remove(full_path_to_img)
    except Exception as e:
        print(f'Cant remove image {full_path_to_img}: {e}')

    db.session.delete(task)
    db.session.commit()

    flash(f'Task "{task.name} was removed"', category='danger')
    return redirect('/')


@login_required
@app.route('/completed/<int:id>')
def completed(id):
    task = Task.query.filter_by(id=id).first_or_404()
    task.completed = True
    db.session.add(task)
    db.session.commit()
    db.session.close()
    return redirect('/')


@login_required
@app.route('/edit/<int:id>', methods=['POST'])
def edit(id):
    new_name = request.form.get('new_name')
    task = Task.query.filter_by(id=id).first()
    task.name = new_name
    db.session.add(task)
    db.session.commit()
    flash('Task name successfully edited!', category='success')
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def register_user():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successfully completed!', category='success')
        print('=' * 60)
        print(f'USER REGISTERED: {user.username} | {user.email}, {user.first_name} {user.last_name}')
        print('=' * 60)
        return redirect('/')

    return render_template('register_form.html', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in!', category='warning')
        flash('If you wish to change user, press the "Logout" button', category='warning')
        return redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Incorrect username! Please try again!', category='warning')
            return redirect('/')
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = '/'
        return redirect(next_page)
    return render_template('login.html', form=form)


@login_required
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect('/')
