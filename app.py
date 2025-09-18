from flask import Flask, render_template, request, redirect, url_for, flash
from conexion.conexion import get_connection

app = Flask(__name__)
app.secret_key = "clave_secreta_flask"  # Necesaria para mensajes flash

# -----------------------------
# Ruta de Inicio
# -----------------------------
@app.route("/")
def inicio():
    return render_template("inicio.html")

# -----------------------------
# Ruta de Acerca de Nosotros
# -----------------------------
@app.route("/nosotros")
def nosotros():
    return render_template("nosotros.html")

# -----------------------------
# Ruta de Contacto
# -----------------------------
@app.route("/contacto")
def contacto():
    return render_template("contacto.html")

# -----------------------------
# Ruta para Crear Usuario
# -----------------------------
@app.route("/crear_usuario", methods=["GET", "POST"])
def crear_usuario():
    nombre = ""
    email = ""
    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]

        try:
            conn = get_connection()
            cursor = conn.cursor()
            # Insertamos un valor fijo para password
            cursor.execute(
                "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
                (nombre, email, "sin_password")
            )
            conn.commit()
            cursor.close()
            conn.close()
            flash("Usuario creado correctamente", "success")
            # Limpiar variables para que el formulario quede vacío
            nombre = ""
            email = ""
        except Exception as e:
            flash(f"Error al crear usuario: {str(e)}", "danger")

    return render_template("crear_usuario.html", nombre=nombre, email=email)


# -----------------------------
# Ruta para Consultar Usuarios
# -----------------------------
@app.route("/consultar_usuarios")
def consultar_usuarios():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id_usuario, nombre, email FROM usuarios")
        usuarios = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template("consultar_usuarios.html", usuarios=usuarios)
    except Exception as e:
        flash(f"Error al consultar usuarios: {str(e)}", "danger")
        return redirect(url_for("inicio"))

# -----------------------------
# Ruta para probar la conexión con la base de datos
# -----------------------------
@app.route("/test_db")
def test_db():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DATABASE();")
        db_name = cursor.fetchone()
        cursor.close()
        conn.close()
        return f"✅ Conectado a la base de datos: {db_name[0]}"
    except Exception as e:
        return f"❌ Error de conexión: {str(e)}"

# -----------------------------
# Ejecutar la aplicación
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
