from app import db

class Rol(db.Model):
    _tablename_ = "rol"

    id_rol = db.Column(db.Integer, primary_key=True)
    nombre_rol = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.String(100))

    def _repr_(self):
        return f"<Rol {self.nombre_rol}>"


#-------------------------------------------------------------------------------------------------


class Empleado(db.Model):
    _tablename_ = "empleado"

    id_empleado = db.Column(db.Integer, primary_key=True)
    cedula = db.Column(db.String(20))
    nombres = db.Column(db.String(100))
    apellidos = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    correo = db.Column(db.String(100))

    def _repr_(self):
        return f"<Empleado {self.nombres}>"


#-------------------------------------------------------------------------------------------------


class Especializacion(db.Model):
    _tablename_ = "especializacion"

    id_especializacion = db.Column(db.Integer, primary_key=True)
    nombre_especializacion = db.Column(db.String(100))

    def _repr_(self):
        return f"<Especializacion {self.nombre_especializacion}>"


#-------------------------------------------------------------------------------------------------


class Usuario(db.Model):
    _tablename_ = "usuario"

    id_usuario = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50))
    clave = db.Column(db.String(255))
    estado = db.Column(db.String(20))

    id_empleado = db.Column(
        db.Integer,
        db.ForeignKey('empleado.id_empleado')
    )

    id_rol = db.Column(
        db.Integer,
        db.ForeignKey('rol.id_rol')
    )
    empleado = db.relationship("Empleado")
    rol = db.relationship("Rol")

    def _repr_(self):
        return f"<Usuario {self.usuario}>"


#-------------------------------------------------------------------------------------------------


class Especialista(db.Model):
    _tablename_ = "especialista"

    id_empleado = db.Column(
        db.Integer,
        db.ForeignKey('empleado.id_empleado'),
        primary_key=True
    )

    id_especializacion = db.Column(
        db.Integer,
        db.ForeignKey('especializacion.id_especializacion')
    )

    hora_inicio = db.Column(db.Time)
    hora_fin = db.Column(db.Time)
    dias_disponibles = db.Column(db.String(100))
    
    empleado = db.relationship(
        "Empleado",
        backref="especialistas"
    )

    especializacion = db.relationship(
        "Especializacion",
        backref="especialistas"
    )

    def _repr_(self):
        return f"<Especialista {self.id_empleado}>"


#-------------------------------------------------------------------------------------------------


class Cita(db.Model):
    _tablename_ = "cita"

    id_cita = db.Column(db.Integer, primary_key=True)

    fecha_cita = db.Column(db.Date)
    hora_cita = db.Column(db.Time)

    id_empleado = db.Column(
        db.Integer,
        db.ForeignKey('empleado.id_empleado')
    )

    id_empleado_especialista = db.Column(
        db.Integer,
        db.ForeignKey('especialista.id_empleado')
    )

    estado_cita = db.Column(db.String(30))
    
    empleado = db.relationship(
    "Empleado",
    foreign_keys=[id_empleado]
)

    especialista = db.relationship(
        "Especialista",
        foreign_keys=[id_empleado_especialista]
    )
    
        

    def _repr_(self):
        return f"<Cita {self.id_cita}>"