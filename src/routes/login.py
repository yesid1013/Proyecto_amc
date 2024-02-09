from flask import Blueprint
from flask_cors import cross_origin
from controllers import LoginController

login = Blueprint('login', __name__,url_prefix='/api/v1')

@cross_origin()
@login.route('/login', methods=['POST'])
def login_normal():
    return LoginController.login()

@cross_origin()
@login.route('/login_google', methods=['POST'])
def login_google():
    return LoginController.login_google()