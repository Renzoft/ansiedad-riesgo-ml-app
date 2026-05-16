import requests

url = "http://127.0.0.1:5000/login"

datos = {
    "correo": "denilson@test.com",
    "contrasena": "123456"
}

respuesta = requests.post(url, json=datos)

print("Status Code:", respuesta.status_code)

print("Respuesta:")

print(respuesta.json())