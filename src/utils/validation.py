from jsonschema import validate, ValidationError, SchemaError

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
    
    except SchemaError as e:
        return str(e)
    

def validation_empresa(json):
    try:
        schema = {"type": "object",
        "properties":{
            "nombre": {"type": "string"},
            "telefono" : {"type" : "string","maxLength": 10},
            "direccion" : {"type" : "string"}
        },
        "required": ["nombre"],
        }

        validate(json,schema=schema)
        return True
    
    except ValidationError as e:
        return str(e)
    
    except SchemaError as e:
        return str(e)

        
        