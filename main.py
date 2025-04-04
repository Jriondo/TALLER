from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import json
import os

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# Ruta para mostrar la página de inicio con HTML y todas las frutas
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, mensaje: str = None):
    try:
        # Verifica si el archivo frutas.json existe
        if not os.path.exists("frutas.json"):
            # Si no existe, crea un archivo vacío o con datos predeterminados
            with open("frutas.json", "w") as file:
                json.dump([], file, ensure_ascii=False, indent=4)

        # Lee el archivo JSON
        with open("frutas.json", "r") as file:
            frutas_json = json.load(file)
        
        # Pasa las frutas y el mensaje al template
        return templates.TemplateResponse("index.html", {"request": request, "frutas": frutas_json, "mensaje": mensaje})
    
    except Exception as e:
        return {"error": f"Error al leer el archivo: {str(e)}"}

# Ruta para agregar, actualizar y eliminar frutas desde el mismo formulario
@app.post("/")
async def modificar_fruta(request: Request, nueva_fruta: str = Form(None), color: str = Form(None), precio: str = Form(None), fruta_id: int = Form(None), eliminar_id: int = Form(None)):
    try:
        # Cargar el archivo JSON
        with open("frutas.json", "r") as file:
            frutas_json = json.load(file)
        
        if nueva_fruta and color and precio:  # Si se proporcionan datos para agregar o actualizar
            if fruta_id is not None:  # Si se está actualizando una fruta existente
                if fruta_id < len(frutas_json):
                    frutas_json[fruta_id] = {
                        "nombre": nueva_fruta,
                        "color": color,
                        "precio": precio
                    }
                else:
                    return {"error": "Fruta no encontrada para actualizar."}
            else:  # Si se está agregando una nueva fruta
                frutas_json.append({
                    "nombre": nueva_fruta,
                    "color": color,
                    "precio": precio
                })

        if eliminar_id is not None:  # Si se solicita eliminar una fruta
            if eliminar_id < len(frutas_json):
                del frutas_json[eliminar_id]
            else:
                return {"error": "Fruta no encontrada para eliminar."}
        
        # Guardar los cambios en el archivo JSON
        with open("frutas.json", "w") as file:
            json.dump(frutas_json, file, ensure_ascii=False, indent=4)

        # Redirigir con mensaje de éxito
        return templates.TemplateResponse("index.html", {"request": request, "frutas": frutas_json, "mensaje": "Operación realizada correctamente."})
    
    except Exception as e:
        return {"error": f"Error al modificar la fruta: {str(e)}"}
