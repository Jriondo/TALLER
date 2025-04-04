from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
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

# Ruta para agregar una nueva fruta desde un formulario
@app.post("/agregar")
async def agregar_fruta(nueva_fruta: str = Form(...), color: str = Form(...), precio: str = Form(...)):
    try:
        with open("frutas.json", "r") as file:
            frutas_json = json.load(file)

        # Agregar la nueva fruta
        frutas_json.append({
            "nombre": nueva_fruta,
            "color": color,
            "precio": precio
        })

        # Guardar los cambios en el archivo JSON
        with open("frutas.json", "w") as file:
            json.dump(frutas_json, file, ensure_ascii=False, indent=4)

        # Redirigir con mensaje de éxito
        return RedirectResponse(url="/?mensaje=Fruta%20agregada%20correctamente")
    
    except Exception as e:
        return {"error": f"Error al agregar la fruta: {str(e)}"}

# Ruta para actualizar una fruta
@app.post("/frutas/{fruta_id}")
async def actualizar_fruta(fruta_id: int, nueva_fruta: str = Form(...), color: str = Form(...), precio: str = Form(...)):
    try:
        with open("frutas.json", "r") as file:
            frutas_json = json.load(file)

        # Verifica que la fruta exista
        if fruta_id < len(frutas_json):
            frutas_json[fruta_id] = {
                "nombre": nueva_fruta,
                "color": color,
                "precio": precio
            }

            # Guardar los cambios en el archivo JSON
            with open("frutas.json", "w") as file:
                json.dump(frutas_json, file, ensure_ascii=False, indent=4)

            # Redirigir con mensaje de éxito
            return RedirectResponse(url="/?mensaje=Fruta%20actualizada%20correctamente")
        else:
            return {"error": "Fruta no encontrada"}
    
    except Exception as e:
        return {"error": f"Error al actualizar la fruta: {str(e)}"}

# Ruta para eliminar una fruta
@app.post("/eliminar/{fruta_id}")
async def eliminar_fruta(fruta_id: int):
    try:
        with open("frutas.json", "r") as file:
            frutas_json = json.load(file)

        # Verifica que la fruta exista
        if fruta_id < len(frutas_json):
            del frutas_json[fruta_id]

            # Guardar los cambios en el archivo JSON
            with open("frutas.json", "w") as file:
                json.dump(frutas_json, file, ensure_ascii=False, indent=4)

            # Redirigir con mensaje de éxito
            return RedirectResponse(url="/?mensaje=Fruta%20eliminada%20correctamente")
        else:
            return {"error": "Fruta no encontrada"}
    
    except Exception as e:
        return {"error": f"Error al eliminar la fruta: {str(e)}"}
