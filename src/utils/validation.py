from jsonschema import validate, ValidationError, SchemaError
import bleach

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
                "id_secundario" : {"type" : ["string","null"]},
                "ubicacion" : {"type" : "string"},
                "tipo_de_equipo" : {"type" : "string"},
                "fabricante" : {"type" : "string"},
                "modelo" : {"type" : ["string","null"]},
                "num_serie" : {"type" : ["string","null"]},
                "datos_relevantes" : {"type" : ["string","null"]},

                "imagen_equipo" : {"type" : ["string","null"]}
                    
                
        },
        "required": ["ubicacion","tipo_de_equipo","fabricante","id_primario"],
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
                    "name": {"type": ["string","null"]},
                    "mimeType": {"type": ["string","null"]},
                    "content": {"type": ["string","null"]}
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
                "id_tipo_servicio" : {"type": "string"},
                "descripcion" : {"type": "string"},
                "observaciones" : {"type" : ["string","null"]},
                "observaciones_usuario" : {"type" : ["string","null"]},

                "orden_de_servicio" : {"type" : ["string","null"]}
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

def validation_costo_servicio(json):
    try:
        schema = {
            "type": "object",
            "properties" : {
                "costo" : {"type" : "number" , "minimum": 0},

                "documento_cotizacion" : {
                    "type" : "object",
                    "properties" : {
                        "name" : {"type": "string"},
                        "mimeType" : {"type": "string"},
                        "content": {"type": "string"}
                    },
                    "required" : ["name","mimeType","content"]
                }   
            },
            "required" : ["costo", "documento_cotizacion"]
        }

        validate(json,schema=schema)
        return True
    
    except ValidationError as e:
        return str(e)
    
    except SchemaError as e:
        return str(e)
    
def validation_permiso(json):
    try:
        schema = {
            "type": "object",
            "properties" : {
                "id_usuario" : {"type": "string"},
                "id_activo" : {"type": "string"},
                "ver_informacion_basica" : {"type": "integer","minimum": 0,"maximum": 1},
                "ver_historial_servicios" : {"type": "integer","minimum": 0,"maximum": 1},
                "ver_novedades" : {"type": "integer","minimum": 0,"maximum": 1},
                "registrar_servicio" : {"type": "integer","minimum": 0,"maximum": 1},
                "registrar_novedad" : {"type": "integer","minimum": 0,"maximum": 1}
            },
            "required": ["id_usuario","id_activo"]
        }

        validate(json,schema=schema)
        return True
    
    except ValidationError as e:
        return str(e)
    
    except SchemaError as e:
        return str(e)
    


           