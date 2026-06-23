from flask import Blueprint, render_template, request, redirect, url_for, session
from app import db
from app.models import Empleado, Especializacion, Especialista, Rol, Usuario, Cita

main = Blueprint("main", __name__)

@main.route("/")
def inicio():

    if "usuario" not in session:
        return redirect(url_for("main.login"))
    
    total_empleados = Empleado.query.count()
    total_especialistas = Especialista.query.count()
    total_especializaciones = Especializacion.query.count()
    total_usuarios = Usuario.query.count()
    total_citas = Cita.query.count()

    return render_template(
    "index.html",
    total_empleados=total_empleados,
    total_especialistas=total_especialistas,
    total_especializaciones=total_especializaciones,
    total_usuarios=total_usuarios,
    total_citas=total_citas
)

@main.route("/empleados")
def empleados():
    
    if "usuario" not in session:
        return redirect(url_for("main.login"))

    empleados = Empleado.query.all()

    return render_template(
        "empleados.html",
        empleados=empleados
    )


#-------------------------------------------------------------------------------------------------


@main.route("/especializaciones/")
def especializaciones():
    
    if "usuario" not in session:
        return redirect(url_for("main.login"))

    especializaciones = Especializacion.query.all()

    return render_template(
        "especializaciones.html",
        especializaciones=especializaciones
    )

@main.route("/especializaciones/nuevo", methods=["POST"])
def nueva_especializacion():

    especializacion = Especializacion(
        nombre_especializacion=request.form["nombre"]
    )

    db.session.add(especializacion)
    db.session.commit()

    return redirect(
        url_for("main.especializaciones")
    )
    
@main.route("/especializaciones/eliminar/<int:id>")
def eliminar_especializacion(id):

    especializacion = Especializacion.query.get_or_404(id)

    db.session.delete(especializacion)
    db.session.commit()

    return redirect(
        url_for("main.especializaciones")
    )
    
@main.route("/especializaciones/editar/<int:id>", methods=["GET", "POST"])
def editar_especializacion(id):

    especializacion = Especializacion.query.get_or_404(id)

    if request.method == "POST":

        especializacion.nombre_especializacion = request.form["nombre"]

        db.session.commit()

        return redirect(
            url_for("main.especializaciones")
        )

    return render_template(
        "editar_especializacion.html",
        especializacion=especializacion
    )


#-------------------------------------------------------------------------------------------------


@main.route("/especialistas")
def especialistas():
    
    if "usuario" not in session:
        return redirect(url_for("main.login"))
    

    especialistas = Especialista.query.all()

    empleados = Empleado.query.all()

    especializaciones = Especializacion.query.all()

    return render_template(
        "especialistas.html",
        especialistas=especialistas,
        empleados=empleados,
        especializaciones=especializaciones
    )

@main.route("/especialistas/nuevo", methods=["POST"])
def nuevo_especialista():

    especialista = Especialista(
        id_empleado=request.form["empleado"],
        id_especializacion=request.form["especializacion"],
        hora_inicio=request.form["hora_inicio"],
        hora_fin=request.form["hora_fin"],
        dias_disponibles=request.form["dias_disponibles"]
    )

    db.session.add(especialista)
    db.session.commit()

    return redirect(
        url_for("main.especialistas")
    )

@main.route("/especialistas/eliminar/<int:id>")
def eliminar_especialista(id):

    especialista = Especialista.query.get_or_404(id)

    db.session.delete(especialista)
    db.session.commit()

    return redirect(
        url_for("main.especialistas")
    )

@main.route(
    "/especialistas/editar/<int:id>",
    methods=["GET", "POST"]
)
def editar_especialista(id):

    especialista = Especialista.query.get_or_404(id)

    if request.method == "POST":

        especialista.hora_inicio = request.form["hora_inicio"]
        especialista.hora_fin = request.form["hora_fin"]
        especialista.dias_disponibles = request.form["dias_disponibles"]

        db.session.commit()

        return redirect(
            url_for("main.especialistas")
        )

    return render_template(
        "editar_especialista.html",
        especialista=especialista
    )

#-------------------------------------------------------------------------------------------------


@main.route("/roles/")
def roles():
    
    if "usuario" not in session:
        return redirect(url_for("main.login"))

    roles = Rol.query.all()

    return render_template(
        "roles.html",
        roles=roles
    )

@main.route("/roles/nuevo", methods=["POST"])
def nuevo_rol():

    rol = Rol(
        nombre_rol=request.form["nombre_rol"],
        descripcion=request.form["descripcion"]
    )

    db.session.add(rol)
    db.session.commit()

    return redirect(
        url_for("main.roles")
    )

@main.route("/roles/eliminar/<int:id>")
def eliminar_rol(id):

    rol = Rol.query.get_or_404(id)

    db.session.delete(rol)
    db.session.commit()

    return redirect(
        url_for("main.roles")
    )

@main.route("/roles/editar/<int:id>", methods=["GET", "POST"])
def editar_rol(id):

    rol = Rol.query.get_or_404(id)

    if request.method == "POST":

        rol.nombre_rol = request.form["nombre_rol"]
        rol.descripcion = request.form["descripcion"]

        db.session.commit()

        return redirect(
            url_for("main.roles")
        )

    return render_template(
        "editar_rol.html",
        rol=rol
    )


#-------------------------------------------------------------------------------------------------


@main.route("/usuarios/")
def usuarios():
    
    if "usuario" not in session:
        return redirect(url_for("main.login"))

    usuarios = Usuario.query.all()
    empleados = Empleado.query.all()
    roles = Rol.query.all()

    return render_template(
        "usuarios.html",
        usuarios=usuarios,
        empleados=empleados,
        roles=roles
    )
    
@main.route("/usuarios/nuevo", methods=["POST"])
def nuevo_usuario():

    usuario = Usuario(
        usuario=request.form["usuario"],
        clave=request.form["clave"],
        estado=request.form["estado"],
        id_empleado=request.form["id_empleado"],
        id_rol=request.form["id_rol"]
    )

    db.session.add(usuario)
    db.session.commit()

    return redirect(
        url_for("main.usuarios")
    )
    
@main.route("/usuarios/eliminar/<int:id>")
def eliminar_usuario(id):

    usuario = Usuario.query.get_or_404(id)

    db.session.delete(usuario)
    db.session.commit()

    return redirect(
        url_for("main.usuarios")
    )
    
@main.route("/usuarios/editar/<int:id>", methods=["GET", "POST"])
def editar_usuario(id):

    usuario = Usuario.query.get_or_404(id)

    if request.method == "POST":

        usuario.usuario = request.form["usuario"]
        usuario.clave = request.form["clave"]
        usuario.estado = request.form["estado"]

        db.session.commit()

        return redirect(
            url_for("main.usuarios")
        )

    return render_template(
        "editar_usuario.html",
        usuario=usuario
    )

#-------------------------------------------------------------------------------------------------


@main.route("/empleados/nuevo", methods=["POST"])
def nuevo_empleado():
    
    if "usuario" not in session:
        return redirect(url_for("main.login"))

    empleado = Empleado(
        cedula=request.form["cedula"],
        nombres=request.form["nombres"],
        apellidos=request.form["apellidos"],
        telefono=request.form["telefono"],
        correo=request.form["correo"]
    )

    db.session.add(empleado)
    db.session.commit()

    return redirect(url_for("main.empleados"))

@main.route("/empleados/eliminar/<int:id>")
def eliminar_empleado(id):

    empleado = Empleado.query.get_or_404(id)

    db.session.delete(empleado)
    db.session.commit()

    return redirect(url_for("main.empleados"))

@main.route("/empleados/editar/<int:id>", methods=["GET", "POST"])
def editar_empleado(id):

    empleado = Empleado.query.get_or_404(id)

    if request.method == "POST":

        empleado.cedula = request.form["cedula"]
        empleado.nombres = request.form["nombres"]
        empleado.apellidos = request.form["apellidos"]
        empleado.telefono = request.form["telefono"]
        empleado.correo = request.form["correo"]

        db.session.commit()

        return redirect(url_for("main.empleados"))

    return render_template(
        "editar_empleado.html",
        empleado=empleado
    )


#-------------------------------------------------------------------------------------------------


@main.route("/citas/")
def citas():
    
    if "usuario" not in session:
        return redirect(url_for("main.login"))

    citas = Cita.query.all()
    empleados = Empleado.query.all()
    especialistas = Especialista.query.all()

    return render_template(
        "citas.html",
        citas=citas,
        empleados=empleados,
        especialistas=especialistas
    )

@main.route("/citas/nuevo", methods=["POST"])
def nueva_cita():

    cita = Cita(
        fecha_cita=request.form["fecha_cita"],
        hora_cita=request.form["hora_cita"],
        id_empleado=request.form["id_empleado"],
        id_empleado_especialista=request.form["id_empleado_especialista"],
        estado_cita=request.form["estado_cita"]
    )

    db.session.add(cita)
    db.session.commit()

    return redirect(
        url_for("main.citas")
    )

@main.route("/citas/eliminar/<int:id>")
def eliminar_cita(id):

    cita = Cita.query.get_or_404(id)

    db.session.delete(cita)
    db.session.commit()

    return redirect(
        url_for("main.citas")
    )


@main.route("/citas/editar/<int:id>", methods=["GET", "POST"])
def editar_cita(id):

    cita = Cita.query.get_or_404(id)

    if request.method == "POST":

        cita.fecha_cita = request.form["fecha_cita"]
        cita.hora_cita = request.form["hora_cita"]
        cita.estado_cita = request.form["estado_cita"]

        db.session.commit()

        return redirect(
            url_for("main.citas")
        )

    return render_template(
        "editar_cita.html",
        cita=cita
    )
    
#-------------------------------------------------------------------------------------------------

@main.route("/login", methods=["GET", "POST"])
def login():
    

    if request.method == "POST":

        usuario_ingresado = request.form["usuario"]
        clave_ingresada = request.form["clave"]

        usuario = Usuario.query.filter_by(
            usuario=usuario_ingresado
        ).first()

        if usuario:

            if usuario.clave == clave_ingresada:

                if usuario.estado == "Activo":
                    session["usuario"] = usuario.usuario

                    return redirect(
                        url_for("main.inicio")
                    )

        return "Usuario o clave incorrectos"

    return render_template("login.html")


#-------------------------------------------------------------------------------------------------


@main.route("/logout")
def logout():

    session.pop("usuario", None)

    return redirect(
        url_for("main.login")
    )