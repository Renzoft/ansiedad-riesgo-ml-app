"""
Prueba de registro
"""
import requests

url = "http://127.0.0.1:5000/registro"

datos = {
    "nombre": "Denilson",
    "correo": "denilson@test.com",
    "contrasena": "123456",
    "facultad": "Ingeniería",
    "ciclo": 7,
}

respuesta = requests.post(url, json=datos)

print("Status Code:", respuesta.status_code)

print("Respuesta:", respuesta.json())
