import flask
import sirope
import flask_login
import os

from flask_login import login_manager
from model.juegodto import JuegoDto
from model.resenhacritica import Resenhacritica
from model.resenhausuario import Resenhausuario
from model.userdto import UserDto
from werkzeug.utils import secure_filename
from datetime import datetime
from static.users.usuariosciritcos import usuarioscriticos

UPLOAD_FOLDER = '/imagenes'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

##Cargar y guardar los usuarios criticos del fichero usuarioscriticos.py
def userscriticos():
    users = usuarioscriticos()
    for x in users:
        sirope.Sirope().save(x)

def create_app():
    lmanager = login_manager.LoginManager()
    fapp = flask.Flask(__name__)
    sirp = sirope.Sirope()

    userscriticos()

    fapp.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    fapp.config["SECRET_KEY"] = "message-board"
    lmanager.init_app(fapp)
    return fapp, lmanager, sirp

app, lm, srp = create_app()

@lm.user_loader
def user_loader(usuario):
    return UserDto.find(srp, usuario)

@lm.unauthorized_handler
def unauthorized_handler():
    flask.flash("Unauthorized")
    return flask.redirect("/")

@app.route('/')
def get_index():
    usr = UserDto.current_user()
    juegos_list = list(sirope.Sirope().load_all(JuegoDto))
    juegos_oids = {j.__oid__: sirope.Sirope().safe_from_oid(j.__oid__) for j in juegos_list}
    sust = {
        "usr": usr,
        "juegos_list": juegos_list,
        "juegos_oids": juegos_oids,
    }

    return flask.render_template("index.html", **sust)

@app.route("/login_pag")
def login_pag():
    return flask.render_template("login.html")

@app.route("/inicio_sesion", methods=["POST"])
def inicio_sesion():
    usuario = flask.request.form.get("edEUsr")
    password = flask.request.form.get("edPassword")

    if not usuario:
        usr = UserDto.current_user()
        if not usr:
            flask.flash("¡Es necesario el login previo!")
            return flask.redirect("/login_pag")
    else:
        if not password:
            flask.flash("¿Y la contraseña?")
            return flask.redirect("/login_pag")

        usr = UserDto.find(srp, usuario)
        if not usr:
            usr = UserDto(usuario, password, "user")
            srp.save(usr)

        elif not usr.chk_password(password):
            flask.flash("Contraseña incorrecta")
            return flask.redirect("/login_pag")

        flask_login.login_user(usr)

    return flask.redirect("/")

@app.route("/Anhadirjuego")
def anhadirjuego():
    usr = UserDto.current_user()
    sust = {
        "usr": usr
    }
    return flask.render_template("anhadirjuego.html", **sust)

@app.route("/save_juego", methods=["GET","POST"])
def save_juego():
    titulo = flask.request.form.get("edTitulo")
    resumen = flask.request.form.get("edResumen")
    nota = flask.request.form.get("edNota")
    imagen = flask.request.files['edImagen']
    autor = UserDto.current_user().usuario

    if not titulo:
        flask.flash("Indique el título del videojuego")
        return flask.redirect("/Anhadirjuego")
    if not resumen:
        flask.flash("Falta la reseña del videojuego")
        return flask.redirect("/Anhadirjuego")
    if not nota:
        flask.flash("Califique el juego, entre un 0 y 100")
        return flask.redirect("/Anhadirjuego")
    elif nota:
        try:
            nota = int(nota)
        except ValueError:
            flask.flash("La nota debe ser un entero entre 0 y 100")
            return flask.redirect("/Anhadirjuego")
    if int(nota) < 0 or int(nota) > 100:
        flask.flash("La nota debe estar comprendida entre 0 y 100")
        return flask.redirect("/Anhadirjuego")
    if not imagen:
        flask.flash("Es necesario subir la imagen del juego")
        return flask.redirect("/Anhadirjuego")
    else:
        filename = secure_filename(imagen.filename)
        imagen.save(os.path.join('static/imagenes', filename)) ##guardar img en carpeta

    imagen_url = ('imagenes/' + filename)
    juego = JuegoDto(titulo,resumen,autor,imagen_url,nota)
    juego.medianotacrit = juego.agregaycalculanotacrit(nota)
    srp.save(juego)

    return flask.redirect("/")

@app.route("/editarjuego")
def editarjuego():
    usr = UserDto.current_user()
    safe_oid = flask.request.args.get('oid')
    game = srp.load(sirope.Sirope().oid_from_safe(safe_oid))
    sust = {
        "usr": usr,
        "safe_oid":safe_oid,
        "game": game
    }
    return flask.render_template("editarjuego.html", **sust)

@app.route("/editar_juego", methods=["GET","POST"])
def editar_juego():
    titulo = flask.request.form.get("edTitulo")
    resumen = flask.request.form.get("edResumen")
    nota = flask.request.form.get("edNota")
    autor = UserDto.current_user().usuario
    juego_oid = flask.request.args.get('oid')
    notaprevia = int(flask.request.args.get('nota'))

    if not titulo:
        flask.flash("Indique el título del videojuego")
        return flask.redirect(flask.request.referrer)
    if not resumen:
        flask.flash("Falta la reseña del videojuego")
        return flask.redirect(flask.request.referrer)
    if not nota:
        flask.flash("Califique el juego, entre un 0 y 100")
        return flask.redirect(flask.request.referrer)
    elif nota:
        try:
            nota = int(nota)
        except ValueError:
            flask.flash("La nota debe ser un entero entre 0 y 100")
            return flask.redirect(flask.request.referrer)
    if int(nota) < 0 or int(nota) > 100:
        flask.flash("La nota debe estar comprendida entre 0 y 100")
        return flask.redirect(flask.request.referrer)

    juego = srp.load(sirope.Sirope().oid_from_safe(juego_oid))
    if not juego:
        return flask.flask("edita juego: juego no encontrado")

    if flask.request.method == 'POST':
        f = flask.request.files['edImagen']
        #Como no permite cargar en el form la img anterior, si no se selecciona una, se mantiene la anterior imagen
        if f:
            filename = secure_filename(f.filename)
            f.save(os.path.join('static/imagenes', filename))
            juego._imagen = ('imagenes/'+filename)

    """Necesario eliminar la nota anterior antes de añadir la nueva,
     pues si no habrá una nota de más y la media será incorrecta"""
    juego.medianotacrit = juego.eliminaycalculanotacrit(notaprevia)
    juego.medianotacrit = juego.agregaycalculanotacrit(nota)
    juego._titulo = titulo
    juego._resumen = resumen
    juego._nota = nota

    srp.save(juego)
    return flask.redirect("/juego?oid="+juego_oid)

@app.route("/borrarjuego")
def borrarjuego():
    usr = UserDto.current_user()
    safe_oid = flask.request.args.get('oid')
    game = srp.load(sirope.Sirope().oid_from_safe(safe_oid))
    sust = {
        "usr": usr,
        "safe_oid":safe_oid,
        "game": game
    }
    return flask.render_template("borrarjuego.html", **sust)

@app.route("/borrar_juego", methods=["POST"])
def borrar_juego():
    juego_oid = flask.request.args.get('oid')
    juego_safe_oid = sirope.Sirope().oid_from_safe(juego_oid)
    srp.delete(juego_safe_oid)

    return flask.redirect("/")

@app.route("/juego", methods=["GET", "POST"])
def pag_juego():
    usr = UserDto.current_user()
    safe_oid = flask.request.args.get('oid')
    game = srp.load(sirope.Sirope().oid_from_safe(safe_oid))

    sust = {
        "usr": usr,
        "safe_oid": safe_oid,
        "game" : game,
        "resenhasCriticas": srp.multi_load(game.resenhacriticas),
        "resenhasUsers": srp.multi_load(game.resenhausuarios),
        "numCriticas": len(game.resenhacriticas),
        "numNotasUsers": len(game.resenhausuarios),
        "comentarios_oids": {c.__oid__: sirope.Sirope().safe_from_oid(c.__oid__) for c in srp.multi_load(game.resenhacriticas) },
        "comentarios_oids_usrs": {c.__oid__: sirope.Sirope().safe_from_oid(c.__oid__) for c in srp.multi_load(game.resenhausuarios)}
    }

    return flask.render_template("juego.html", **sust)


@app.route("/addcomentario/", methods=["POST"])
def addcomentario():
    comentario = flask.request.form.get("edComentario")
    nota = flask.request.form.get("edNota")
    autor = UserDto.current_user().usuario
    fecha = f"{datetime.now().day:02d}/{datetime.now().month:02d}/{datetime.now().year:02d}"

    safe_oid = flask.request.args.get('oid')
    juego = srp.load(sirope.Sirope().oid_from_safe(safe_oid))

    if not juego:
        return flask.flash("modifica(): juego no encontrado")
    if not comentario:
        flask.flash("Escriba un comentario")
        return flask.redirect(flask.request.referrer)
    if not nota:
        flask.flash("Califique el juego, entre un 0 y 100")
        return flask.redirect(flask.request.referrer)
    elif nota:
        try:
            nota = int(nota)
        except ValueError:
            flask.flash("La nota debe ser un entero entre 0 y 100")
            return flask.redirect(flask.request.referrer)
    if int(nota) < 0 or int(nota) > 100:
        flask.flash("La nota debe estar comprendida entre 0 y 100")
        return flask.redirect(flask.request.referrer)

    """Si es un usuario critico, 'admin'"""
    if UserDto.current_user().access == 'admin':
        rese = srp.save(Resenhacritica(nota,comentario,autor,fecha))
        juego.add_resenhacriticas(rese)
        juego.medianotacrit = juego.agregaycalculanotacrit(nota)
    else:
        rese = srp.save(Resenhausuario(nota, comentario, autor, fecha))
        juego.add_resenhausuarios(rese)
        juego.medianotausr = juego.agregaycalculanotausr(nota)

    srp.save(juego)
    return flask.redirect(flask.request.referrer)

@app.route("/borrarComentario/", methods=["GET", "POST"])
def borrar_comentario():
    comentario_oid = flask.request.args.get('oid') #obtener str del oid
    comentario_safe_oid = sirope.Sirope().oid_from_safe(comentario_oid) #obtener oid de la resenha
    juego_oid = flask.request.args.get('juego') #obtenemos str del oid del juego
    juego = srp.load(sirope.Sirope().oid_from_safe(juego_oid)) #cargamos juego
    nota = int(flask.request.args.get('nota'))
    if not comentario_oid:
        return flask.flash("elimina():OID nod encontrado")

    """Si es un usuario critico"""
    if UserDto.current_user().access == 'admin':
        juego.del_resenhacriticas(comentario_safe_oid)  # eliminamos el comentario(oid) de resenhacriticas[]
        juego.medianotacrit = juego.eliminaycalculanotacrit(nota)
    else:
        juego.del_resenhausuarios(comentario_safe_oid)  # eliminamos el comentario(oid) de resenhausuarios[]
        juego.medianotausr = juego.eliminaycalculanotausr(nota)

    srp.save(juego) #guardar los cambios
    srp.delete(comentario_safe_oid)  # borrar la reseña

    return flask.redirect(flask.request.referrer)

@app.route("/logout")
def logout():
    flask_login.logout_user()
    return flask.redirect("/")


if __name__ == '__main__':
    app.run()


