SENAMECF

Sistema de Bienestar Social para la automatización y gestión en las áreas de Talento Humano y Servicios Médicos del SENAMECF.

Integrantes

- Gabriel Díaz
- Becker Viso
- kleyver Barrios
- Ricargo Serrano
- Carlos Guaman
- Manuel Mata

Tecnologías utilizadas

- Python
- Flask
- SQLAlchemy
- Flask-Migrate
- HTML
- CSS
- Git
- GitHub

Requisitos

Tener instalado:

- Python 3.13 o superior
- Git
- Visual Studio Code

Instalación del proyecto

Clonar el repositorio:

git clone https://github.com/Gdiaz9281/SENAMECF.git

Entrar al proyecto:

cd SENAMECF

Crear entorno virtual:

python -m venv venv

Activar entorno virtual:

Windows

venv\Scripts\activate

Instalar dependencias:

pip install -r requirements.txt

Ejecutar el proyecto

python run.py

Estructura del proyecto

SENAMECF/
│
├── app/
├── migrations/
├── config.py
├── run.py
├── requirements.txt
├── README.md
└── .gitignore

Módulos del sistema

- Seguridad
- Empleados
- Especializaciones Médicas
- Especialistas
- Citas Médicas

Control de versiones

Para subir cambios:

git add .
git commit -m "Descripción del cambio"
git push

Para descargar cambios:

git pull
