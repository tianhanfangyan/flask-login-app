#! /usr/bin/env python
#! coding:utf-8

import optparse
from flask import Flask, request, jsonify
from flask_login import LoginManager, login_required, login_user, UserMixin, logout_user


# 初始化一个flask的app实例
app = Flask(__name__)

# config
app.config.update(
    SECRET_KEY = 'nyheFs1RdvWu8O8',
)

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# 登录基于用户，需要定义User类
class User(UserMixin):
    pass

# 简单验证
users = [
    {'id':1, 'username': 'Tom', 'password': '01234'},
    {'id':2, 'username': 'Ben', 'password': '56789'}
]


def query_user(username):
    for user in users:
        if username == user['username']:
            return user


@login_manager.unauthorized_handler
def unauthorized():
    response = {'status': -1, 'msg': 'You are not login in'}
    return jsonify(response)


@login_manager.user_loader
def load_user(user_id):
    curr_user = User()
    curr_user.id = user_id

    return curr_user


@app.route('/login', methods=['POST'])
def login():
    body = request.get_json(force=True)
    username = body["username"]
    password = body["password"]

    user = query_user(username)

    if user is not None and user['password'] == password:
        curr_user = User()
        curr_user.id = user['id']
        login_user(curr_user)
        body = {'status': 0, 'msg': 'Login successful, password is valid'}
    else:
        body = {'status': -1, 'msg': 'Login failed, password is invalid'}

    return jsonify(body)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    body = {'status': 0, 'msg': 'Logged out successful'}
    return jsonify(body)

if __name__ == '__main__':
    parser = optparse.OptionParser()

    parser.add_option('--host', action='store', type='string', default='0.0.0.0', dest='host')
    parser.add_option('-p', '--port', action='store', type='int', default='9001', dest='port')

    opt, args = parser.parse_args()

    server_host = opt.host
    server_port = opt.port

    app.run(host=server_host, port=server_port, debug=False)
