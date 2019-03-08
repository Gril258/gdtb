from flask import views, render_template, request, make_response, redirect, url_for, jsonify
import app
import json

class AdminView(views.MethodView):
    """Main page for admin"""
    def get(self):
        config = app.base.config().json
        if 'Auth' in request.cookies:
            if request.cookies['Auth'] == 'yes':
                return render_template('AdminHome.html', SERVER_URL=config['server']['url'])
        else:
            return redirect(url_for('login'))

class LoginView(views.MethodView):
    """log in page"""
    def get(self):
        return render_template(
            'Login.html'
        )

    def post(self):
        form_user = request.form['username']
        form_password = request.form['password']
        u = app.base.user()
        u.load_user_by_name(form_user)
        if u.authenticate(form_user, form_password) == True:
            resp = make_response(redirect(url_for('admin')))
            resp.set_cookie('Auth', 'yes')
            return resp
        else:
            error = 'Invalid Credentials. Please try again.'
            return render_template(
                'Login.html',
                error = error
            )


class UserView(views.MethodView):
    """docstring for UserView"""
    def get(self, user_id):
            if user_id is None:
                # return a list of users
                u = app.base.user()
                return jsonify(**u.list_user())
            else:
                # expose a single user
                pass

    def post(self):
        # create a new user
        e = {}
        user = request.get_json()
        if 'name' in user and 'password' in user:
            u = app.base.user()
            u.name = user['name']
            u.md5_password = u.encrypt_password(user['password'])
            u.email = user['email']
            if u.create_user():
                return jsonify(**user)
            else:
                e['status'] = "Error: cannot create user"
                return jsonify(**e)
        else:
            e['status'] = "Error: wrong username or password"
            return jsonify(**e)

    def delete(self, user_id):
        # delete a single user
        if 'Auth' in request.cookies:
            if request.cookies['Auth'] == 'yes':
                u = app.base.user()
                u.user_id = user_id
                res = {}
                res['status'] = u.delete_user()
                return jsonify(**res)
        else:
            return redirect(url_for('login'))
    def put(self, user_id):
        # update a single user
        e = {}
        user = request.get_json()
        if 'name' in user and 'password' in user and 'id' in user:
            u = app.base.user()
            u.user_id = user['id']
            u.name = user['name']
            u.md5_password = u.encrypt_password(user['password'])
            u.email = user['email']
            if u.update_user():
                return jsonify(**user)
            else:
                e['status'] = "Error: cannot create user"
                return jsonify(**e)
        else:
            e['status'] = "Error: wrong username or password"
            return jsonify(**e)
        pass

class TaskView(views.MethodView):
    """docstring for UserView"""
    def get(self, task_id):
            if task_id is None:
                # return a list of users
                t = app.base.task()
                return jsonify(**t.list_task())
            else:
                # expose a single user
                pass

    def post(self):
        # create a new user
        e = {}
        task = request.get_json()
        if 'name' in task and 'module' in task:
            t = app.base.task()
            t.name = task['name']
            t.status = "ready"
            t.module = task['module']
            t.data = task['data']
            t.options = task['options']
            if t.create_task():
                return jsonify(**task)
            else:
                e['status'] = "Error: cannot create user"
                return jsonify(**e)
        else:
            e['status'] = "Error: wrong username or password"
            return jsonify(**e)

    def delete(self, task_id):
        # delete a single task
        if 'Auth' in request.cookies:
            if request.cookies['Auth'] == 'yes':
                t = app.base.task()
                t.task_id = task_id
                res = {}
                res['status'] = t.delete_task()
                return jsonify(**res)
        else:
            return redirect(url_for('login'))
    def put(self, task_id):
        # update a single user
        e = {}
        task = request.get_json()
        if 'name' in task and 'module' in task and 'id' in task:
            t = app.base.task()
            t.task_id = task_id
            t.name = task['name']
            t.status = "ready"
            t.module = task['module']
            t.data = task['data']
            t.options = task['options']
            if t.update_task():
                return jsonify(**task)
            else:
                e['status'] = "Error: cannot create user"
                return jsonify(**e)
        else:
            e['status'] = "Error: wrong username or password"
            return jsonify(**e)
        pass