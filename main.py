#################################
# IMPORTANTE
# tendremos que utilizar la version de python 3.12 para poder utilizar transformers

# video tutorial
# https://www.youtube.com/watch?v=J0y2tjBz2Ao

# Crear directorio virtual dentro de la carpeta del proyecto
# python -m venv fastapi-env (windows)
# python3 -m venv fastapi-env (ubuntu)

# activar entorno virtual
# fastapi-env\Scripts\activate (windows)
# source fastapi-env/bin/activate (ubuntu)

# Si tenemos un archivo requeriment.txt podemos instalar las dependencias necesarias con:
# pip install -r requeriments.txt

###############################################################
# si no tenemos requeriments.txt ejecutamos lo siguiente:
# instalar fastapi y uvicorn
# pip install fastapi uvicorn

# instalar request y beautifulsoup4 y transformers
# para instalar transformer es necesario instalar rust para algunas de sus librerias
# Tambien instalar Visual Studio Installer con el complemento Desktop development with C++

# https://rustup.rs/
# pip install requests beautifulsoup4 transformers

# Instalamos torch o tensorflow, si tenemos python 3.13 tendremos que instalar anaconda ya que su version de python es 3.12 y yo tengo la 3.13
# https://pytorch.org/get-started/locally/
# pip install torch

################################################################

# Si queremos asegurarnos de tener el uvicorn podemos ejecutar:
# pip install fastapi uvicorn

# Crear archivo main.py
# Ejecutar archivo main.py
# uvicorn main:app --reload (si esta solo en local)

# Tambien podemos ejecutar:
# uvicorn main:app --host 0.0.0.0 --port 800 (recomendable)

# desactivar archivo, escribimos en el cmd
# deactivate

# Si no funciona el deactivate ponemos lo siguiente en el cmd
# tasklist | findstr uvicorn
# taskkill /PID <PID>

#Ruta donde se ejecuta
# http://127.0.0.1:8000

################################################
from fastapi import FastAPI
from pydantic import BaseModel # Validacion de datos
from typing import Optional # Datos opcionales

app = FastAPI()



from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
from typing import List
from transformers import pipeline

app = FastAPI()


# Cargar el pipeline preentrenado de Hugging Face para análisis de sentimientos
# El modelo distilbert-base-uncased-finetuned-sst-2-english está diseñado para análisis de sentimientos en inglés
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")


# Función para hacer el scraping de la web
def contenido_web(url: str) -> List[str]:
    # Paso 1: Descargar el contenido HTML de la página
    response = requests.get(url)

    # Verificar que la solicitud fue exitosa (código 200)
    if response.status_code != 200:
        raise Exception(f"Error al acceder al sitio web: {response.status_code}")

    # Paso 2: Analizar el contenido HTML con BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Paso 3: Extraer los datos de interés (en este caso, titulares de <h2>)
    titles = [title.get_text().strip() for title in soup.find_all("h2")]

    return titles


# Función para analizar los sentimientos de los títulos utilizando el modelo BERT
def analizar_sentimientos(titulos: List[str]) -> List[dict]:
    resultados = []

    # Analizar cada título con el pipeline de Hugging Face
    for title in titulos:
        sentiment = sentiment_pipeline(title)

        # Guardar el resultado
        resultados.append({
            "titulo": title,
            "sentimiento": sentiment[0]['label'],
            "confianza": sentiment[0]['score']
        })

    return resultados

# Opcion 1: La URL está incluida directamente en la ruta, lo cual puede requerir codificación de caracteres especiales.
# Ejemplo: http://127.0.0.1:8000/scraping/bbc
# Ruta para obtener los titulares de un sitio web
@app.get("/scraping/{url}")
def obtener_titulares(url: str):
    try:

        # Si la URL no contiene "http" al principio, se completa con https://
        if not url.startswith("http"):
            url = f"https://www.{url}.com"

        # Llamamos a la función de scraping
        titulos = contenido_web(url)

        # Eliminamos el último título (como en tu código original)
        titulos = titulos[:-1]

        # Realizamos el análisis de sentimientos sobre los títulos extraídos
        resultados_sentimiento = analizar_sentimientos(titulos)

        # Devolvemos los resultados de los sentimientos y los títulos
        return {"resultados": resultados_sentimiento, "cantidad": len(resultados_sentimiento)}

    except Exception as e:
        return {"error": str(e)}


# Opcion 2: Usa un parámetro de consulta ?url=, lo que simplifica el paso de URL completas y evita problemas con caracteres especiales en las rutas.
# Ejemplo: http://127.0.0.1:8000/scraping/?url=https://www.bbc.com
# Ruta para obtener los titulares de un sitio web
@app.get("/scraping/")
def obtener_titulares(url: str):
    try:
        # Si la URL no contiene "http" al principio, se completa con https://
        if not url.startswith("http"):
            url = f"https://www.{url}.com"

        # Llamamos a la función de scraping
        titulos = contenido_web(url)

        # Eliminamos el último título (como en tu código original)
        titulos = titulos[:-1]

        # Realizamos el análisis de sentimientos sobre los títulos extraídos
        resultados_sentimiento = analizar_sentimientos(titulos)

        # Devolvemos los resultados de los sentimientos y los títulos
        return {"resultados": resultados_sentimiento, "cantidad": len(resultados_sentimiento)}

    except Exception as e:
        return {"error": str(e)}



# Validar los datos
class Libro(BaseModel):
    titulo: str
    autor: str
    paginas: int
    editorial: Optional[str]


@app.get("/")
def index():
    return {"message" : "Hello, World!"}


@app.get("/libros/{id}")
def mostrar_libro(id: int):
    return {"id": id, "nombre": "El Señor de los Anillos"}


@app.post("/libros")
def insertar_libro(libro: Libro):
    return {"menssage": f"Libro '{libro.titulo}' insertado"}
