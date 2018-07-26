# -*- coding: utf-8 -*-
"""app views."""
from alayatodo import app, db
from alayatodo.models import Todo, User
from flask import (
    redirect,
    render_template,
    request,
    session,
    jsonify,
    flash
)
from alayatodo.utils import clean_field
from alayatodo.constants import DONE, NOT_DONE


@app.route('/')
def home():
    with app.open_resource('../README.md', mode='r') as f:
        readme = "".join(l.decode('utf-8') for l in f)
        return render_template('index.html', readme=readme)


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_POST():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(
        username=username,
        password=password
    ).first()

    if user:
        session['user'] = {'username': user.username, 'id': user.id}
        session['logged_in'] = True
        return redirect('/todo')

    flash("Invalid credentials!")
    return redirect('/login')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    return redirect('/')


@app.route('/todo/<id>', methods=['GET'])
def todo(id):
    todo = Todo.query.filter_by(
        id=id,
        user=session['user']['id']
    ).first()

    if not todo:
        flash("Todo not found")
        return redirect("/todo")

    return render_template('todo.html', todo=todo)


@app.route('/todo', methods=['GET'])
@app.route('/todo/', methods=['GET'])
def todos():
    if not session.get('logged_in'):
        return redirect('/login')

    todos = Todo.query.filter_by(user=session['user']['id'])
    return render_template('todos.html', todos=todos)


@app.route('/todo', methods=['POST'])
@app.route('/todo/', methods=['POST'])
def todos_POST():
    if not session.get('logged_in'):
        return redirect('/login')

    description = clean_field(request.form.get('description', ' '))

    if description:
        todo = Todo(session['user']['id'], description)
        db.session.delete(todo)
        db.session.commit()

        flash("Todo added succesfully.")
    else:
        flash("Description is required.")

    return redirect('/todo')


@app.route('/todo/<id>', methods=['POST'])
def todo_delete(id):
    if not session.get('logged_in'):
        return redirect('/login')

    todo = Todo.query.filter_by(
        id=id,
        user=session['user']['id']
    ).first()

    if todo:
        db.session.delete(todo)
        db.session.commit()

        flash("Todo deleted succesfully.")
    else:
        flash("Todo not found.")

    return redirect('/todo')


@app.route('/todo/complete/<id>', methods=['POST'])
def todo_complete(id):
    if not session.get('logged_in'):
        return redirect('/login')

    todo = Todo.query.filter_by(
        id=id,
        user=session['user']['id']
    ).first()

    # fail first approach
    # TODO: use flag to not repeat code?
    if not todo:
        flash("Todo not found")
        return redirect('/todo')

    if todo.completed == NOT_DONE:
        todo.completed = DONE
        db.session.add(todo)
        db.session.commit()

        message = "{todo_name}: marked as done.".format(
            todo_name=todo.description
        )
        flash(message)

    return redirect('/todo')


@app.route('/todo/<id>/json', methods=['GET'])
def todo_json(id):
    if not session.get('logged_in'):
        return redirect('/login')

    todo = Todo.query.filter_by(
        id=id,
        user=session['user']['id']
    ).first()
    data = {
        'message': 'OK',
        'status_code': 200,
        'results': []
    }

    if not todo:
        data['status_code'] = 404
        data['message'] = 'Not Found'
    else:
        data['results'].append({key: todo[key] for key in todo.keys()})

    return jsonify(data)
