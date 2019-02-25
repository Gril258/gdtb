#base module - config load, db handler,
import os
import json
import socket
from . import database
import hashlib
class config():
    """docstring for config"""
    def __init__(self):
        self.json = self.get_config() 


    def get_config(self):
        """doc"""
        config_dir = os.path.dirname(os.path.abspath(__file__))
        with open("%s/config/config.json" % (config_dir), "r") as f:
            return json.load(f)
		

class user():
    """main authentication method class"""
    def __init__(self):
        self.config = config().json
        self.id = None
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
        return ret

    def update_user(self):
        cur = self.reactor_db.connection.cursor()
        q = "UPDATE users SET name = %s, md5_password = %s, email = %s WHERE id = %s"
        if self.id is not None and self.name is not None:
            cur.execute(q, (self.name, self.md5_password, self.email, self.user_id))
            self.reactor_db.connection.commit()
            self.user_id = cur.fetchone()[0]
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
                self.id = r[0]
                self.name = r[1]
                self.md5_password = r[2] 
                self.email = r[3]
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