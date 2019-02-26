# basic flask router configuration
from flask import Flask, jsonify, request, render_template, send_from_directory, Response
import os
import json
import app.views


flask_object = Flask(__name__)

class Wapi(Flask):
    """docstring for AdminRouter"""
    def __init__(self, fc=None):
        super().__init__(__name__)
        self.config.from_pyfile(fc)
        print(self.config)
        self.debug = True
        self.root = "/admin"
        #print(self.config)
        print(self)
        #print(self.view_functions)
        if self.config['ENABLE_ADMIN'] == True:
            msg = []
            msg.append(self.enable_admin())
            msg.append(self.enable_login())
            msg.append(self.enable_static())
            msg.append(self.enable_user())
            for m in msg:
                print(m)
        self.reload()

    def reload(self):
        self.run(host=self.config['HOST'])

    def enable_admin(self):
        url = "%s" % self.root
        print("adding route %s" % url)
        view = app.views.admin.AdminView.as_view('admin')
        self.add_url_rule('/admin/', view_func=view, methods=['GET',])
        return "Admin Module loaded"

    def enable_static(self):
        print("adming route for /static")
        static_view = app.views.static.StaticView.as_view('static_file')
        self.add_url_rule('/static/<path:path>', view_func=static_view, methods=['GET',])
        return "Static Module loaded"
        
    def enable_login(self):
        url = "/login"
        print("adding route %s" % url)
        view = app.views.admin.LoginView.as_view('login')
        self.add_url_rule(url, view_func=view, methods=['GET', 'POST'])
        return "Login Module loaded"

    def enable_user(self):
        url = "/user"
        print("adding route %s" % url)
        user_view = app.views.admin.UserView.as_view('user_api')
        self.add_url_rule('/user/', defaults={'user_id': None}, view_func=user_view, methods=['GET',])
        self.add_url_rule('/user/', view_func=user_view, methods=['POST',])
        self.add_url_rule('/user/<int:user_id>', view_func=user_view, methods=['GET', 'PUT', 'DELETE'])
        return "User Module loaded"

    def enable_task(self):
        url = "/task"
        print("adding route %s" % url)
        view = app.views.admin.UserView.as_view('task_api')
        self.add_url_rule('/task/', defaults={'task_id': None}, view_func=view, methods=['GET',])
        self.add_url_rule('/task/', view_func=view, methods=['POST',])
        self.add_url_rule('/task/<int:user_id>', view_func=view, methods=['GET', 'PUT', 'DELETE'])
