from flask import Flask
from utils.g_drive_service import GoogleDriveService
from io import BytesIO
from googleapiclient.http import MediaIoBaseUpload, MediaInMemoryUpload
from datetime import datetime
from flask import request, jsonify
import base64
import qrcode
import io

service=GoogleDriveService().build()

def getFileListFromGDrive():
    selected_fields="files(id,name,webViewLink)"
    g_drive_service=GoogleDriveService().build()
    list_file=g_drive_service.files().list(fields=selected_fields).execute()
    return {"files":list_file.get("files")}

def uploadJSON(file): #Funcion para guardar un archivo en google drive
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
            "parents": ["1m6h1aZAqPh-vgtMw0sQtEM3RIlEoAFdC"],  # Se guardara en la carpeta imagenes_novedad, se usa el id de la carpeta

        }

        returned_fields = "id, name, mimeType, webViewLink, exportLinks"
    
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
        qr_code_image = qrcode.make(f"http://127.0.0.1:5000/info_activo/{id_activo_hex}")  # Generar el código QR con la URL que que redirigira
        qr_code_io = io.BytesIO()  # Crear un objeto BytesIO para guardar la imagen en memoria
        qr_code_image.save(qr_code_io)

        media_body = MediaInMemoryUpload(qr_code_io.getvalue(), mimetype="image/png", resumable=True)

        created_at = datetime.now().strftime("%Y%m%d%H%M%S")
        file_metadata = {
            "name": f"codigo_qr_{created_at}.png",
            "parents": ["1os7McQE069GqnfzlgAjMYC0fQZnaM9bn"],  # ID de la carpeta en Google Drive donde deseas guardar las imágenes
            }

        returned_fields = "id, name, mimeType, webViewLink, exportLinks"

        upload_response = service.files().create(
                body=file_metadata,
                media_body=media_body,
                fields=returned_fields
            ).execute()

        return upload_response
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado :", "error" : str(e)})