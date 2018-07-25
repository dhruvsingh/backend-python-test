from alayatodo import app
from flask import (
    g,
    redirect,
    render_template,
    request,
    session,
    jsonify,
    flash
)
from .utils import clean_field
from .constants import DONE, NOT_DONE


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

    sql = "SELECT * FROM users WHERE username = '%s' AND password = '%s'";
    cur = g.db.execute(sql % (username, password))
    user = cur.fetchone()
    if user:
        session['user'] = dict(user)
        session['logged_in'] = True
        return redirect('/todo')

    return redirect('/login')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    return redirect('/')


@app.route('/todo/<id>', methods=['GET'])
def todo(id):
    cur = g.db.execute("SELECT * FROM todos WHERE id ='%s'" % id)
    todo = cur.fetchone()
    return render_template('todo.html', todo=todo)


@app.route('/todo', methods=['GET'])
@app.route('/todo/', methods=['GET'])
def todos():
    if not session.get('logged_in'):
        return redirect('/login')
    cur = g.db.execute("SELECT * FROM todos WHERE user_id ='%s'" % session['user']['id'])
    todos = cur.fetchall()
    return render_template('todos.html', todos=todos)


@app.route('/todo', methods=['POST'])
@app.route('/todo/', methods=['POST'])
def todos_POST():
    if not session.get('logged_in'):
        return redirect('/login')

    description = clean_field(request.form.get('description', ' '))
    if description:
        g.db.execute(
            "INSERT INTO todos (user_id, description) VALUES ('%s', '%s')"
            % (session['user']['id'], description)
        )
        g.db.commit()
        flash("Todo added succesfully.")
    return redirect('/todo')


@app.route('/todo/<id>', methods=['POST'])
def todo_delete(id):
    if not session.get('logged_in'):
        return redirect('/login')
    g.db.execute("DELETE FROM todos WHERE id ='%s'" % id)
    g.db.commit()
    flash("Todo deleted succesfully.")
    return redirect('/todo')


@app.route('/todo/complete/<id>', methods=['POST'])
def todo_complete(id):
    if not session.get('logged_in'):
        return redirect('/login')

    cur = g.db.execute(
        """
            SELECT `id`, `completed`, `description`
            FROM todos
            WHERE id ='%s' AND
            user_id = '%s'
        """ % (id, session['user']['id'])
    )
    todo = cur.fetchone()

    # fail first approach
    # TODO: use flag to not repeat code?
    if not todo:
        flash("Todo not found")
        return redirect('/todo')

    if todo['completed'] == NOT_DONE:
        g.db.execute(
            """
                UPDATE todos
                SET completed = '%s'
                WHERE id ='%s'
            """ % (DONE, id)
        )
        g.db.commit()
        message = "{todo_name}: marked as done.".format(
            todo_name=todo['description']
        )
        flash(message)

    return redirect('/todo')


@app.route('/todo/<id>/json', methods=['GET'])
def todo_json(id):
    if not session.get('logged_in'):
        return redirect('/login')

    cur = g.db.execute(
        """
            SELECT *
            FROM todos
            WHERE id ='%s'
        """ % (id,)
    )
    todo = cur.fetchone()

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
