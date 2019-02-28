from flask import views, render_template, request, make_response, redirect, url_for, jsonify
import app
import json

class AdminView(views.MethodView):
    """Main page for admin"""
    def get(self):
        config = app.base.config().json
        if 'Auth' in request.cookies:
            if request.cookies['Auth'] == 'yes':
                return render_template('AdminHome.html', SERVER_URL=config['SERVER_NAME'])
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
        pass

    def put(self, user_id):
        # update a single user
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
        pass

    def put(self, user_id):
        # update a single user
        pass