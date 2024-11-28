from flask import Flask, render_template, request, redirect, flash, jsonify, session, make_response
from flask_jwt import JWT, jwt_required, current_identity
import controladores.controlador_discos as controlador_discos
import controladores.controlador_artistas as controlador_artistas
import controladores.controlador_users as controlador_users
import controladores.controlador_simulacion as controlador_simulacion
import clases.clsDisco as clsDisco
import hashlib
from datetime import datetime

##### SEGURIDAD - INICIO #####
class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

def authenticate(username, password):
    data = controlador_users.obtener_user_por_email(username)
    if data:
        user = User(data[0], data[1], data[2])
        password_hash = encstringsha256(password)
        if user and user.password == password_hash:
            return user
    return None

def identity(payload):
    user_id = payload['identity']
    data = controlador_users.obtener_user_por_id(user_id)
    user = User(data[0], data[1], data[2])
    return user

def encstringsha256(cadena_legible):
    h = hashlib.new('sha256')
    h.update(bytes(cadena_legible, encoding='utf-8'))
    epassword = h.hexdigest()
    return epassword

app = Flask(__name__)

app.debug = True
app.config['SECRET_KEY'] = 'super-secret'

jwt = JWT(app, authenticate, identity)

##### SEGURIDAD - FIN #####

##### INICIO - DISCOS #####
@app.route("/agregar_disco")
def formulario_agregar_disco():
    return render_template("agregar_disco.html")


@app.route("/guardar_disco", methods=["POST"])
def guardar_disco():
    codigo = request.form["codigo"]
    nombre = request.form["nombre"]
    artista = request.form["artista"]
    precio = request.form["precio"]
    genero = request.form["genero"]
    objDisco = clsDisco.Disco(0, codigo, nombre, artista, precio, genero)
    # controlador_discos.insertar_disco(codigo, nombre, artista, precio, genero)
    controlador_discos.insertar_disco(objDisco)
    # De cualquier modo, y si todo fue bien, redireccionar
    return redirect("/discos")


@app.route("/discos")
def discos():
    if 'username' in session:
        discos = controlador_discos.obtener_discos()
        return render_template("discos.html", discos=discos)
    else:
        return render_template("login.html")

@app.route("/eliminar_disco", methods=["POST"])
def eliminar_disco():
    controlador_discos.eliminar_disco(request.form["id"])
    return redirect("/discos")


@app.route("/formulario_editar_disco/<int:id>")
def editar_disco(id):
    # Obtener el disco por ID
    disco = controlador_discos.obtener_disco_por_id(id)
    return render_template("editar_disco.html", disco=disco)


@app.route("/actualizar_disco", methods=["POST"])
def actualizar_disco():
    id = request.form["id"]
    codigo = request.form["codigo"]
    nombre = request.form["nombre"]
    artista = request.form["artista"]
    precio = request.form["precio"]
    genero = request.form["genero"]
    controlador_discos.actualizar_disco(codigo, nombre, artista, precio, genero, id)
    return redirect("/discos")
##### FIN - DISCOS #####

##### INICIO - ARTISTAS #####
@app.route("/artistas")
def artistas():
    artistas = controlador_artistas.obtener_artistas()
    return render_template("artistas.html", artistas=artistas)

@app.route("/agregar_artista")
def formulario_agregar_artista():
    return render_template("agregar_artista.html")

@app.route("/guardar_artista", methods=["POST"])
def guardar_artista():
    nombre = request.form["nombre"]
    nacionalidad = request.form["nacionalidad"]
    aniolanzamiento = request.form["aniolanzamiento"]
    cantidaddiscos = request.form["cantidaddiscos"]
    web = request.form["web"]
    redsocialprincipal = request.form["redsocialprincipal"]
    promediostream = request.form["promediostream"]
    controlador_artistas.insertar_artista(nombre, nacionalidad, aniolanzamiento, cantidaddiscos, web, redsocialprincipal, promediostream)
    # De cualquier modo, y si todo fue bien, redireccionar
    return redirect("/artistas")

@app.route("/formulario_editar_artista/<int:id>")
def editar_artista(id):
    # Obtener el artista por ID
    artista = controlador_artistas.obtener_artista_por_id(id)
    return render_template("editar_artista.html", artista=artista)

@app.route("/actualizar_artista", methods=["POST"])
def actualizar_artista():
    id = request.form["id"]
    nombre = request.form["nombre"]
    nacionalidad = request.form["nacionalidad"]
    aniolanzamiento = request.form["aniolanzamiento"]
    cantidaddiscos = request.form["cantidaddiscos"]
    web = request.form["web"]
    redsocialprincipal = request.form["redsocialprincipal"]
    promediostream = request.form["promediostream"]
    controlador_artistas.actualizar_artista(nombre, nacionalidad, aniolanzamiento, cantidaddiscos, web, redsocialprincipal, promediostream, id)
    return redirect("/artistas")

@app.route("/eliminar_artista", methods=["POST"])
def eliminar_artista():
    controlador_artistas.eliminar_artista(request.form["id"])
    return redirect("/artistas")

##### FIN - ARTISTAS #####
@app.route("/")
@app.route("/login")
def login():
    if 'username' in session:
        return redirect("/discos")
    else:
        return render_template("login.html")

@app.route("/signup")
def signup():
    if 'username' in session:
        return redirect("/discos")
    else:
        return render_template("signup.html")

@app.route("/iniciar_sesion", methods=["POST"])
def iniciar_sesion():
    email = request.form['username']
    password = request.form['password']
    user = controlador_users.obtener_user_por_email(email)
    epassword = encstringsha256(password)
    if user and user[2] == epassword:
        session['username'] = email
        resp = make_response(redirect("/discos"))
        resp.set_cookie('username', email, 3600)
        return resp
    else:
        return redirect("/login")

@app.route("/registrar_usuario", methods=["POST"])
def registrar_usuario():
    email = request.form['username']
    password = request.form['password']
    confpassword = request.form['confpassword']
    if password == confpassword:
        epassword = encstringsha256(password)
        controlador_users.registrar_usuario(email, epassword)
        return redirect("/login")
    else:
        return redirect("/signup")

@app.route('/logout')
def logout():
    session.pop('username', None)
    resp = make_response(redirect("/login"))
    resp.set_cookie('username', '', 0)
    return resp

@app.route("/api_obtenerdiscos")
def api_obtenerdiscos():
    rpta = dict()
    try:
        discos = controlador_discos.obtener_discos()
        rpta["data"] = discos
        rpta["message"] = "El listado de discos se realizó correctamente"
        rpta["status"] = 1
        return jsonify(rpta)
    except Exception as e:
        rpta["data"] = {}
        rpta["message"] = "Ocurrió un error: " + repr(e)
        rpta["status"] = -1
        return jsonify(rpta)

@app.route("/api_zavaletaroger_simularprestamo", methods=["POST"])
@jwt_required()
def api_zavaletaroger_simularprestamo():
    try:
        capital = request.json["capital"]
        tasaimensual = request.json["tasaimensual"]
        cantidadmeses = request.json["cantidadmeses"]

        data = {
            "fecha_simulacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "capital": capital,
            "tasa_mensual": tasaimensual,
            "cantidad_meses": cantidadmeses,
            "cuotas": []
        }

        capitalmes = capital / cantidadmeses
        total = 0.0
        rpta = dict()

        for i in range(cantidadmeses):
            interes = round((capital - (capitalmes * i)) * (tasaimensual / 100), 2)
            total_cuota = round(capitalmes + interes, 2)
            data["cuotas"].append({
                "mes": f"Mes {i + 1}",
                "capital": round(capitalmes, 2),
                "interes": interes,
                "total": total_cuota
            })
            total += total_cuota

        data["total"] = round(total, 2)
        data["itotal"] = round(total - capital, 2)

        id_simulacion = controlador_simulacion.insertar_simulacion(data)
        data["idsimulacion"] = id_simulacion

        rpta["data"] = data
        rpta["message"] = "Simulación generada correctamente"
        rpta["status"] = 1

        # Return response
        return jsonify(rpta), 200

    except Exception as e:
        return jsonify({"message": str(e), "status": 0}), 500

##### APIs - INICIO #####

##### APIs - FIN #####

# Iniciar el servidor
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)