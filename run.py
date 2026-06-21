print("INICIO")

from app import create_app

print("IMPORTO APP")

app = create_app()

print("APP CREADA")
print(app.url_map)

if __name__ == "__main__":
    app.run(debug=True)