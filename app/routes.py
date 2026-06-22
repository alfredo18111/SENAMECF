from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.models import Empleado, Especializacion

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

@main.route("/especializaciones/")
def especializaciones():

    especializaciones = Especializacion.query.all()

    return render_template(
        "especializaciones.html",
        especializaciones=especializaciones
    )

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