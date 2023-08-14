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
    
def validation_activo(json):
    try:
        schema = {
            "type": "object",
            "properties":{
                "id_primario": {"type": "string"},
                "id_secundario" : {"type" : "string"},
                "ubicacion" : {"type" : "string"},
                "tipo_de_equipo" : {"type" : "string"},
                "fabricante" : {"type" : "string"},
                "modelo" : {"type" : "string"},
                "num_serie" : {"type" : "string"},
                "datos_relevantes" : {"type" : "string"},

                "imagen_equipo" : {
                    "type": "object",
                    "properties": {
                    "name": {"type": "string"},
                    "mimeType": {"type": "string"},
                    "content": {"type": "string"}
                    },
                    "required" : ["name","mimeType","content"]
                },

                "ficha_tecnica" : {
                    "type" : "object",
                    "properties" : {
                        "name" : {"type": "string"},
                        "mimeType": {"type": "string"},
                        "content": {"type": "string"}
                    },
                    "required" : ["name","mimeType","content"]
                }

        },
        "required": ["ubicacion","tipo_de_equipo","fabricante"],
        }

        validate(json,schema=schema)
        return True
    
    except ValidationError as e:
        return str(e)
    
    except SchemaError as e:
        return str(e)
    
def validation_novedad(json):
    try:
        schema = {"type": "object",
        "properties":{
            "nombre_reporta": {"type": "string"},
            "nombre_empresa" : {"type" : "string"},
            "cargo" : {"type" : "string"},
            "descripcion_reporte" : {"type" : "string"},

            "imagenes" : {
                "type" : "object",
                "properties" : {
                    "name": {"type": "string"},
                    "mimeType": {"type": "string"},
                    "content": {"type": "string"}
                },
                "required" : ["name","mimeType","content"]
            }
        },
        "required": ["nombre_reporta","nombre_empresa","cargo","descripcion_reporte"],
        }

        validate(json,schema=schema)
        return True
    
    except ValidationError as e:
        return str(e)
    
    except SchemaError as e:
        return str(e)
    

def validation_servicio(json):
    try:
        schema = {
            "type": "object",
            "properties" : {
                "fecha_ejecucion" : {"type": "string"},
                "id_tipo_servicio" : {"type": "integer", "minimum": 1, "maximum": 3},
                "descripcion" : {"type": "string"},
                "observaciones" : {"type": "string"},

                "informe" : {
                    "type" : "object",
                    "properties" : {
                        "name" : {"type": "string"},
                        "mimeType" : {"type": "string"},
                        "content": {"type": "string"}
                    },
                    "required" : ["name","mimeType","content"]
                }
            },
            "required" : ["fecha_ejecucion","id_tipo_servicio","descripcion"]
        }

        validate(json,schema=schema)
        return True
    
    except ValidationError as e:
        return str(e)
    
    except SchemaError as e:
        return str(e)

def validation_subcliente(json):
    try:
        schema = {
            "type": "object",
            "properties" : {
                "nombre" : {"type": "string"},
                "id_empresa" : {"type": "string"},
                "contacto" : {"type": "string"},
                "direccion" : {"type": "string"},
            },
            "required": ["nombre","id_empresa"]
        }

        validate(json,schema=schema)
        return True
    
    except ValidationError as e:
        return str(e)
    
    except SchemaError as e:
        return str(e)

           