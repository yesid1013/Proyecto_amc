from flask import Flask
from utils.g_drive_service import GoogleDriveService
from io import BytesIO
from googleapiclient.http import MediaIoBaseUpload, MediaInMemoryUpload
from datetime import datetime
from flask import request, jsonify
import base64
import qrcode
import io
import os
import firebase_admin
from firebase_admin import credentials, storage
# Obtener la ruta al directorio actual
current_directory = os.path.dirname(os.path.realpath(__file__))

# Construir la ruta completa al archivo credentials.json
credentials_path = os.path.join(current_directory, "../utils/serviceAccountKey.json")

cred = credentials.Certificate(credentials_path)
firebase_admin.initialize_app(cred, {'storageBucket': 'storage-amc.appspot.com'})



service=GoogleDriveService().build()


def getFileListFromGDrive():
    selected_fields="files(id,name,webViewLink)"
    g_drive_service=GoogleDriveService().build()
    list_file=g_drive_service.files().list(fields=selected_fields).execute()
    return {"files":list_file.get("files")}

def uploadFile(file,id_folder): #Funcion para guardar un archivo en google drive
    try:

        file_name = file["name"]
        file_content_base64 = file["content"]

        # Decodifica el contenido del archivo desde Base64
        file_content = base64.b64decode(file_content_base64)

        buffer_memory = BytesIO(file_content)

        media_body = MediaIoBaseUpload(buffer_memory, mimetype=file["mimeType"], resumable=True)

        created_at = datetime.now().strftime("%Y%m%d%H%M%S")
        file_metadata = {
            "name": f"{file_name} ({created_at})",
            "parents": [id_folder],  # Se guardara en una carpeta especifica, se usa el id de la carpeta

        }

        returned_fields = "id, name, mimeType, webViewLink, webContentLink"
    
        upload_response = service.files().create(
            body=file_metadata, 
            media_body=media_body,  
            fields=returned_fields
        ).execute()

        return upload_response
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado :", "error" : str(e)})
    
def uploadQR(id_activo_hex):
    try:
        qr_code_image = qrcode.make(f"http://192.168.20.26:4200/qractivo/{id_activo_hex}")  # Generar el código QR con la URL que que redirigira
        qr_code_io = io.BytesIO()  # Crear un objeto BytesIO para guardar la imagen en memoria
        qr_code_image.save(qr_code_io)

        created_at = datetime.now().strftime("%Y%m%d%H%M%S")
        folder_name = "qr_codes"  # Nombre de la carpeta en Firebase Storage
        file_name = f"{folder_name}/codigo_qr_{created_at}.png"

         # Subir el código QR a Firebase Storage
        bucket = storage.bucket()
        blob = bucket.blob(file_name)
        blob.upload_from_string(qr_code_io.getvalue(), content_type='image/png')

         # Obtener la URL del código QR almacenado
        # url_firebase_storage = blob.path


        return file_name
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado :", "error" : str(e)})