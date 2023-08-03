from flask import Blueprint
from flask_cors import cross_origin
from controllers import GoogleDriveController

google_drive = Blueprint("google_drive", __name__)

@cross_origin()
@google_drive.route('/listar_archivos')
def listar_archivos():
    return GoogleDriveController.getFileListFromGDrive()