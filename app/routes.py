from flask import Blueprint, render_template
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

@main.route("/prueba")
def prueba():
    return "FUNCIONA"