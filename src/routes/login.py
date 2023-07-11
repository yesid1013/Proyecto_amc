from flask import Blueprint
from flask_cors import cross_origin
from controllers import LoginController

login = Blueprint('login', __name__)

@cross_origin()
@login.route('/login', methods=['POST'])
def login_normal():
    return LoginController.login()