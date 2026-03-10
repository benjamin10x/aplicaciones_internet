from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

FASTAPI_BASE = "http://localhost:5000"


@app.get("/")
def index():
    try:
        response = requests.get(f"{FASTAPI_BASE}/v1/usuarios/", timeout=5)
        response.raise_for_status()

        payload = response.json()
        usuarios = payload.get("data", [])
        total = payload.get("total", len(usuarios))
        error = None

    except Exception as e:
        usuarios = []
        total = 0
        error = f"No pude conectar con FastAPI en {FASTAPI_BASE}. Error: {e}"
        print(error)

    return render_template(
        "index.html",
        usuarios=usuarios,
        total=total,
        error=error
    )


@app.post("/agregar")
def agregar():
    try:
        user_id = int(request.form.get("id", "").strip())
    except ValueError:
        print("El ID debe ser un número entero.")
        return redirect(url_for("index"))

    nombre = (request.form.get("nombre") or "").strip()
    email = (request.form.get("email") or "").strip()

    if not nombre or not email:
        print("Nombre y email son obligatorios.")
        return redirect(url_for("index"))

    data = {
        "id": user_id,
        "nombre": nombre,
        "email": email
    }

    try:
        response = requests.post(
            f"{FASTAPI_BASE}/v1/usuarios/",
            json=data,
            timeout=5
        )

        if response.status_code >= 400:
            try:
                detail = response.json().get("detail", response.text)
            except Exception:
                detail = response.text
            print(detail)
        else:
            print("Usuario agregado")

    except Exception as e:
        print("Error al conectarse con FastAPI:", e)

    return redirect(url_for("index"))


@app.post("/eliminar/<int:user_id>")
def eliminar(user_id: int):
    try:
        response = requests.delete(
            f"{FASTAPI_BASE}/v1/usuario/{user_id}"
        )

        if response.status_code >= 400:
            try:
                detail = response.json().get("detail", response.text)
            except Exception:
                detail = response.text
            print("No se pudo eliminar:", detail)
        else:
            print("Usuario eliminado")

    except Exception as e:
        print("Error al conectarse con FastAPI:", e)

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5010, debug=True)