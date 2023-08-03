from flask import Flask
from utils.g_drive_service import GoogleDriveService
from io import BytesIO
from googleapiclient.http import MediaIoBaseUpload
from datetime import datetime
from flask import request, jsonify
import base64

service=GoogleDriveService().build()

def getFileListFromGDrive():
    selected_fields="files(id,name,webViewLink)"
    g_drive_service=GoogleDriveService().build()
    list_file=g_drive_service.files().list(fields=selected_fields).execute()
    return {"files":list_file.get("files")}

def uploadJSON(file):
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