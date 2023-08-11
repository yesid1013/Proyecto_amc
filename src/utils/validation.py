from jsonschema import validate, ValidationError, SchemaError

# schema = {"type": "object",
#     "properties":{
#         "correo": {"type": "string"},
#         "contrasena" : {"type" : "string"}
#         },
#         "required": ["correo"],
#         "required" : ["contrasena"]
#         }

def validation_login(json):
    try:
        schema = {"type": "object",
        "properties":{
            "correo": {"type": "string"},
            "contrasena" : {"type" : "string"}
        },
        "required": ["correo"],
        "required" : ["contrasena"]
        }

        validate(json,schema=schema)
        return True
    
    except ValidationError as e:
        return str(e)

        
        