from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.models import Empleado, Especializacion, Especialista

main = Blueprint("main", __name__)

@main.route("/")
def inicio():
    return render_template("index.html")

@main.route("/empleados")
def empleados():

    empleados = Empleado.query.all()

    return render_template(
        "empleados.html",
        empleados=empleados
    )


#-------------------------------------------------------------------------------------------------


@main.route("/especializaciones/")
def especializaciones():

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


@main.route("/empleados/nuevo", methods=["POST"])
def nuevo_empleado():

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


