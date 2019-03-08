#base module - config load, db handler,
import os
import json
import socket
from . import database
import hashlib


class config():
    class __config():
        """docstring for config"""
        def __init__(self):
            self.json = self.load_from_file()
            self.overrride_from_env()
    
    
        def load_from_file(self):
            """doc"""
            config_dir = os.path.dirname(os.path.abspath(__file__))
            with open("%s/config/config.json" % (config_dir), "r") as f:
                return json.load(f)
    
        def overrride_from_env(self):
            # this is is dynamic (not part of config.json)
            if os.getenv("SERVER_URL") is not None:
                server_url = os.getenv("SERVER_URL")
                print("Registering SERVER_URL=%s" % (server_url))
                self.json['server']['url'] = server_url
            elif os.getenv("HOST") is not None and os.getenv("PORT") is not None:
                server_url = "%s:%s" % (os.getenv("HOST"), os.getenv("PORT"))
                print("Registering SERVER_URL=%s" % (server_url))
                self.json['server']['url'] = server_url
            else:
                server_url = "%s:%s" % (self.json['server']['host'], self.json['server']['port'])
                print("Registering SERVER_URL=%s" % (server_url))
                self.json['server']['url'] = server_url
    
            # this is part of config.json
            if os.getenv("HOST") is not None:
                self.json['server']['host'] = os.getenv("HOST")
            if os.getenv("PORT") is not None:
                self.json['server']['port'] = os.getenv("PORT")
            if os.getenv("DB_HOST") is not None:
                self.json['database']['host'] = os.getenv("DB_HOST")
            if os.getenv("DB_PORT") is not None:
                self.json['database']['port'] = os.getenv("DB_PORT")

    instance = None
    def __new__(cls): # __new__ always a classmethod
        if not config.instance:
            config.instance = config.__config()
        return config.instance
    def __getattr__(self, name):
        return getattr(self.instance, name)
    def __setattr__(self, name):
        return setattr(self.instance, name)

class user():
    """main authentication method class"""
    def __init__(self):
        self.config = config().json
        self.user_id = None
        self.name = None
        self.md5_password = None
        self.email = None
        self.reactor_db = database.connection(self.config['database']['name'], self.config['database']['host'], self.config['database']['user'], self.config['database']['password'], self.config['database']['port'])
        self.reactor_db.connect()

    def encrypt_password(self, password):
        md5_password = hashlib.md5(password.encode('utf-8')).hexdigest()
        return md5_password

    def create_user(self):
        cur = self.reactor_db.connection.cursor()
        q = "WITH cte AS(INSERT INTO users (name, md5_password, email) VALUES (%s, %s, %s)RETURNING id) SELECT * FROM cte"
        if self.name is not None and self.md5_password is not None:
            cur.execute(q, (self.name, self.md5_password, self.email))
            self.reactor_db.connection.commit()
            self.user_id = cur.fetchone()[0]
            return True
        else:
            return False

    def list_user(self):
        response = {}
        ret = []
        cur = self.reactor_db.connection.cursor()
        q = "SELECT id, name, email FROM users"
        cur.execute(q, (self.name, self.md5_password, self.email))
        res = cur.fetchall()
        for r in res:
            t = {}
            t['id'] = r[0]
            t['name'] = r[1]
            t['email'] = r[2]
            ret.append(t)
        response['list'] = ret
        return response

    def update_user(self):
        cur = self.reactor_db.connection.cursor()
        q = "UPDATE users SET name = %s, md5_password = %s, email = %s WHERE id = %s"
        if self.user_id is not None and self.name is not None:
            cur.execute(q, (self.name, self.md5_password, self.email, self.user_id))
            self.reactor_db.connection.commit()
            return True
        else:
            return False

    def delete_user(self):
        cur = self.reactor_db.connection.cursor()
        q = "DELETE FROM users WHERE id = %s"
        if self.user_id is not None:
            cur.execute(q, (self.user_id,))
            self.reactor_db.connection.commit()
            return True
        else:
            return False

    def authenticate(self, name, password):
        auth_name = name
        auth_md5_password = self.encrypt_password(password)
        print(auth_name)
        print(self.name)
        print(password)
        print(auth_md5_password)
        if auth_name == self.name:
        	if self.md5_password == auth_md5_password:
        		return True
        return False

    def load_user_by_name(self, name):
        cur = self.reactor_db.connection.cursor()
        q = "SELECT id, name, md5_password, email FROM users WHERE name = %s"
        cur.execute(q, (name,))
        r = cur.fetchone()
        if r is not None:
            if r[1] == name:
                self.user_id = r[0]
                self.name = r[1]
                self.md5_password = r[2]
                self.email = r[3]
                return True
        return False

    def create_table(self):
        cur = self.reactor_db

class task():
    """main authentication method class"""
    def __init__(self):
        self.config = config().json
        self.task_id = None
        self.name = None
        self.status = None
        self.data = None
        self.options = None
        self.module = None
        self.reactor_db = database.connection(self.config['database']['name'], self.config['database']['host'], self.config['database']['user'], self.config['database']['password'], self.config['database']['port'])
        self.reactor_db.connect()

    def create_task(self):
        cur = self.reactor_db.connection.cursor()
        q = "WITH cte AS(INSERT INTO reactor (name, status, module, options, data) VALUES (%s, %s, %s, %s, %s) RETURNING id) SELECT * FROM cte"
        if self.name is not None and self.status is not None:
            cur.execute(q, (self.name, self.status, self.module, self.options, self.data))
            self.reactor_db.connection.commit()
            self.task_id = cur.fetchone()[0]
            return True
        else:
            return False

    def list_task(self):
        response = {}
        ret = []
        cur = self.reactor_db.connection.cursor()
        q = "SELECT id, name, status, data, options, module FROM reactor"
        cur.execute(q)
        res = cur.fetchall()
        for r in res:
            t = {}
            t['id'] = r[0]
            t['name'] = r[1]
            t['status'] = r[2]
            t['data'] = r[3]
            t['options'] = r[4]
            t['module'] = r[5]
            ret.append(t)
        response['list'] = ret
        return response

    def update_task(self):
        cur = self.reactor_db.connection.cursor()
        q = "UPDATE reactor SET name = %s, status = %s, data = %s, options = %s, module = %s WHERE id = %s"
        if self.task_id is not None and self.name is not None:
            cur.execute(q, (self.name, self.status, self.data, self.options, self.module, self.task_id))
            self.reactor_db.connection.commit()
            return True
        else:
            return False


    def delete_task(self):
        cur = self.reactor_db.connection.cursor()
        q = "DELETE FROM reactor WHERE id = %s"
        if self.task_id is not None:
            cur.execute(q, (self.task_id,))
            self.reactor_db.connection.commit()
            return True
        else:
            return False


    def load_task_by_name(self, name):
        cur = self.reactor_db.connection.cursor()
        q = "SELECT id, name, status, data, options, module FROM users WHERE name = %s"
        cur.execute(q, (name,))
        r = cur.fetchone()
        if r is not None:
            if r[1] == name:
                self.id = r[0]
                self.name = r[1]
                self.status = r[2]
                self.data = r[3]
                self.options = r[4]
                self.module = r[5]
                return True
        return False

class server(object):
    """handle server registration into reactor database"""
    def __init__(self):
        self.config = config().json
        self.hostname = socket.gethostname()
        self.machine_type = 'labrat'
        self.machine_id = 1
        self.machine_env = 'test'
        self.machine_location = 'krut'
        self.reactor_db = database.connection(self.config['database']['name'], self.config['database']['host'], self.config['database']['user'], self.config['database']['password'], self.config['database']['port'])
        self.reactor_db.connect()
        self.core_stack = []
        self.active_slot = []

    def __del__(self):
        #self.unregister_core()
        #self.unregister()
        pass

    def __enter__(self):
        self.register()
        return self

    def __exit__(self, *args, **kwargs):
        self.unregister_core()
        self.unregister()
        pass

    def get_status(self):
        cur = self.reactor_db.connection.cursor()
        q = "SELECT status FROM server WHERE hostname = %s"
        cur.execute(q, (self.hostname, ))
        self.status = cur.fetchone()[0]
        return self.status


    def set_status(self):
        cur = self.reactor_db.connection.cursor()
        q = "UPDATE server SET status=%s WHERE hostname = %s"
        cur.execute(q (self.status, self.hostname))
        self.reactor_db.connection.commit()
        return "done"

    def register(self):
        self.status = 'registered'
        cur = self.reactor_db.connection.cursor()
        q = "WITH cte AS(INSERT INTO server (hostname, machine_type, machine_id, machine_env, machine_location, status) VALUES (%s, %s, %s, %s, %s, %s)RETURNING id) SELECT * FROM cte"
        cur.execute(q, (self.hostname, self.machine_type, self.machine_id, self.machine_env, self.machine_location, self.status))
        self.reactor_db.connection.commit()
        self.server_id = cur.fetchone()[0]
        return self.server_id

    def register_core(self, core_id, core_obj):
        cur = self.reactor_db.connection.cursor()
        q = "WITH cte AS(INSERT INTO reactor_server_slot (core_id, server_id) VALUES (%s, %s)RETURNING id) SELECT * FROM cte"
        cur.execute(q, (core_id, self.server_id))
        self.reactor_db.connection.commit()
        slot_id = cur.fetchone()[0]
        core_obj.slot_id = slot_id
        self.active_slot.append(core_obj)
        return slot_id

    def unregister(self):
        cur = self.reactor_db.connection.cursor()
        q = "DELETE FROM server WHERE hostname = %s"
        cur.execute(q, (self.hostname,))
        self.reactor_db.connection.commit()
        return 'done'

    def unregister_core(self):
        cur = self.reactor_db.connection.cursor()
        q = "DELETE FROM reactor_server_slot WHERE server_id = %s"
        cur.execute(q, (self.server_id,))
        self.reactor_db.connection.commit()
        return 'done'