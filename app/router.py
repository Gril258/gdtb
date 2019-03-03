# basic flask router configuration
from flask import Flask, jsonify, request, render_template, send_from_directory, Response
import os
import json
import app.views


class Wapi(Flask):
    """docstring for AdminRouter"""
    def __init__(self):
        super().__init__(__name__)

        self.configure()
        self.override_config_from_env()
        self.setup_routes()

        self.reload()

    def configure(self):
        config = self.load_config_from_json()

        self.config['DEBUG'] = config['server']['debug']
        self.config['ENABLE_ADMIN'] = config['server']['enable_admin']
        self.config['HOST'] = config['server']['host']
        self.config['PORT'] = config['server']['port']
        self.config['SERVER_NAME'] = "%s:%s" % (config['server']['host'], config['server']['port'])

    def load_config_from_json(self):
        config_dir = os.path.dirname(os.path.abspath(__file__))
        with open("%s/config/config.json" % (config_dir), "r") as f:
            return json.load(f)

    def override_config_from_env(self):
        if os.getenv("HOST") is not None:
            self.config['HOST'] = os.getenv("HOST")

        if os.getenv("PORT") is not None:
            self.config['PORT'] = os.getenv("PORT")

        if os.getenv("SERVER_NAME") is not None:
            self.config['SERVER_NAME'] = os.getenv("SERVER_NAME")

    def reload(self):
        self.run(
            host=self.config['HOST'],
            port=self.config['PORT'],
            debug=self.config['DEBUG']
        )

    def setup_routes(self):
        if self.config['ENABLE_ADMIN'] == True:
            msg = []
            msg.append(self.enable_admin())
            msg.append(self.enable_login())
            msg.append(self.enable_static())
            msg.append(self.enable_user())
            msg.append(self.enable_task())
            for m in msg:
                print(m)

    def enable_admin(self):
        url = "/admin"
        print("adding route %s" % url)
        view = app.views.admin.AdminView.as_view('admin')
        self.add_url_rule(url, view_func=view, methods=['GET',])
        return "Admin Module loaded"

    def enable_static(self):
        print("adding route /static")
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
        view = app.views.admin.TaskView.as_view('task_api')
        self.add_url_rule('/task/', defaults={'task_id': None}, view_func=view, methods=['GET',])
        self.add_url_rule('/task/', view_func=view, methods=['POST',])
        self.add_url_rule('/task/<int:task_id>', view_func=view, methods=['GET', 'PUT', 'DELETE'])
