################################################################################################################################
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

################################################################################################################################
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

################################################################################################################################
# Opcional
# Instalar geoip2 para limitar el acceso a una zona demografica
# pip install geoip2

# Instalar su base de datos
# https://dev.maxmind.com/geoip/geolocate-an-ip/databases/

# from fastapi import FastAPI, HTTPException, Request
# import geoip2.database

# app = FastAPI()

# # Load the pre-trained GeoIP database for location-based access
# # The GeoLite2-City.mmdb file must be downloaded from MaxMind's website
# geoip_reader = geoip2.database.Reader('GeoLite2-City.mmdb')  # Ensure this file is in your project directory

# # Function to check if the user is allowed based on their IP location
# def is_user_allowed(ip: str) -> bool:
#     try:
#         # Query the IP address using the GeoIP2 database
#         response = geoip_reader.city(ip)

#         # Check if the country is Spain (ISO code "ES")
#         if response.country.iso_code != "ES":
#             return False
        
#         # Check if the region is Andalusia
#         if response.subdivisions.most_specific.name != "Andalucía":
#             return False
        
#         # Check if the city is Málaga
#         if response.city.name != "Málaga":
#             return False
        
#         return True  # If all conditions are met, allow access
#     except Exception as e:
#         # Handle any exception (e.g., invalid IP address or GeoIP query failure)
#         return False

# # Endpoint to access the content and check the user's location
# @app.get("/scrapping_CNN")
# def obtener_titulares_CNN(request: Request):
#     user_ip = request.client.host  # Get the IP address of the user

#     # Check if the user is allowed based on their geographical location
#     if not is_user_allowed(user_ip):
#         raise HTTPException(status_code=403, detail="Access Denied: You must be from Málaga, Andalucía, Spain.")

#     # Continue with the scraping and sentiment analysis (from your existing code)
#     try:
#         # Call the scraping function
#         news_items = content_web_CNN()

#         # Perform sentiment analysis on the extracted titles
#         sentiment_results = analyze_sentiments_CNN(news_items)

#         # Return the sentiment results and the titles
#         return {"result": sentiment_results, "amount": len(sentiment_results)}

#     except Exception as e:
#         return {"error": str(e)}


################################################################################################################################

# Si queremos asegurarnos de tener el uvicorn podemos ejecutar:
# pip install fastapi uvicorn

# Crear archivo main.py
# Ejecutar archivo main.py
# uvicorn main:app --reload (si esta solo en local)

# Tambien podemos ejecutar:
# uvicorn main:app --host 0.0.0.0 --port 8000 (recomendable)
# uvicorn main:app --host 0.0.0.0 --port 8000 --reload (otra opcion)

# desactivar archivo, escribimos en el cmd
# deactivate

# Si no funciona el deactivate ponemos lo siguiente en el cmd
# tasklist | findstr uvicorn
# taskkill /PID <PID>

# Crear archivo requeriment
# pip freeze > requirements.txt

#Ruta donde se ejecuta
# http://127.0.0.1:8000

################################################################################################################################



# Libraries for web scraping
# Library to create the API and manage routes
from fastapi import FastAPI

# Library to make HTTP requests to websites
import requests

# Library for parsing and extracting data from HTML
from bs4 import BeautifulSoup

# Library for type hints, useful for defining lists and their contents
from typing import List

# Library to perform natural language processing (NLP) tasks, like sentiment analysis
from transformers import pipeline

# Library to handle relative and absolute URLs
from urllib.parse import urljoin

# Initialize the FastAPI application to define and manage API routes
app = FastAPI()


# Load the pre-trained Hugging Face pipeline for sentiment analysis
# The model distilbert-base-uncased-finetuned-sst-2-english is designed for sentiment analysis in English
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")


# Function to perform web scraping
def content_from_web(url: str) -> List[str]:
    # Step 1: Download the HTML content of the page
    response = requests.get(url)

    # Verify that the request was successful (status code 200)
    if response.status_code != 200:
        raise Exception(f"Error accessing the website: {response.status_code}")

    # Step 2: Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Step 3: Extract the relevant data (in this case, headlines from <h2>)
    titles = [title.get_text().strip() for title in soup.find_all("h2")]

    return titles

# Function to analyze the sentiments of the titles using the BERT model
def analyze_sentiments(titulos: List[str]) -> List[dict]:
    results = []

    # Analyze each title with the Hugging Face pipeline
    for title in titulos:
        sentiment = sentiment_pipeline(title)

        # Store the result
        results.append({
            "title": title,
            "sentiment": sentiment[0]['label'],
            "precision": sentiment[0]['score']
        })

    return results


################################################################################################################################
# Function to scrape the CNN website
def content_web_CNN():
    # Step 1: Download the HTML content of the page
    url = "https://www.cnn.com"

     # List to store the results
    results = []

    # Verify that the request was successful (status code 200)
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Error accessing the website: {response.status_code}")

    # Step 2: Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Step 3: Extract the <a> tags containing the class 'container__link' (to get both title and link)
    news_items = soup.find_all("a", class_="container__link")

    # Extract title and link
    for news in news_items:
        # Extract the link (the value of the 'href' attribute in the <a> tag)
        relative_link = news.get("href")

        # If the link is relative (starts with '/'), combine it with the base URL
        if relative_link and relative_link.startswith('/'):
            full_link = urljoin(url, relative_link)  # Concatenate the base URL with the relative path
        else:
            full_link = relative_link  # If it's already a full URL, leave it as is

        # Find the <span> with the class 'container__headline-text' inside each <a>
        span = news.find("span", class_="container__headline-text")

        # If the <span> and the link are found, extract the title and add it to the results
        if span and full_link:
            title = span.get_text(strip=True)
            results.append({"title": title, "link": full_link})

    return results

# Function to analyze the sentiments of the news_items
def analyze_sentiments_CNN(news_items):
    # Analyzes the sentiments of the titles and associates them with their links
    results = []

    for news in news_items:
        title = news["title"]
        link = news["link"]

        # Analyze the sentiment of the title
        sentiment = sentiment_pipeline(title)

        # Add the result
        results.append({
            "title": title,
            "link": link,
            "sentiment": sentiment[0]['label'],
            "precision": sentiment[0]['score']
        })

    return results

# Endpoint to get the news items and their sentiments
@app.get("/scrapping_CNN")
def get_CNN_headlines():
    try:
        # Call the scraping function
        news_items = content_web_CNN()

        # Perform sentiment analysis on the extracted titles
        sentiment_results = analyze_sentiments_CNN(news_items)

        # Return the sentiment results and the titles
        return {"result": sentiment_results, "amount": len(sentiment_results)}

    except Exception as e:
        return {"error": str(e)}



################################################################################################################################
# Test endpoints

# Option 1: The URL is included directly in the route, which may require encoding special characters.
# Example: http://127.0.0.1:8000/scraping/bbc
# Route to get headlines from a website
@app.get("/scrapping/{url}")
def get_headlines(url: str):
    try:
        # If the URL does not start with "http", it will be completed with https://
        if not url.startswith("http"):
            url = f"https://www.{url}.com"

        # Call the scraping function
        titles = content_from_web(url)

        # Remove the last title
        titles = titles[:-1]

        # Perform sentiment analysis on the extracted titles
        sentiment_results = analyze_sentiments(titles)

        # Return the sentiment results and the titles
        return {"result": sentiment_results, "amount": len(sentiment_results)}

    except Exception as e:
        return {"error": str(e)}


# Option 2: Use a query parameter ?url=, which simplifies passing complete URLs and avoids issues with special characters in the paths.
# Example: http://127.0.0.1:8000/scraping/?url=https://www.bbc.com
# Route to get the headlines from a website
@app.get("/scrapping/")
def obtener_titulares(url: str):
    try:
         # If the URL does not start with "http", it will be completed with https://
        if not url.startswith("http"):
            url = f"https://www.{url}.com"

        # Call the scraping function
        titles = content_from_web(url)

        # Remove the last title
        titles = titles[:-1]

        # Perform sentiment analysis on the extracted titles
        sentiment_results = analyze_sentiments(titles)

        # Return the sentiment results and the titles
        return {"result": sentiment_results, "amount": len(sentiment_results)}

    except Exception as e:
        return {"error": str(e)}



# Endpoint for getting the credits from an API
@app.get("/")
def index():
    return {"Credits" : "Created by 'David Moreno Cerezo' and 'Jairo Andrades Bueno'"}



###############################################################
# Ejemplos de prueba
# from fastapi import FastAPI
from pydantic import BaseModel # Validacion de datos
from typing import Optional # Datos opcionales

#app = FastAPI()

# Validar los datos
class Libro(BaseModel):
    titulo: str
    autor: str
    paginas: int
    editorial: Optional[str]


# @app.get("/")
# def index():
#     return {"message" : "Created by [Person 1] and [Person 2]"}


@app.get("/libros/{id}")
def mostrar_libro(id: int):
    return {"id": id, "nombre": "El Señor de los Anillos"}


@app.post("/libros")
def insertar_libro(libro: Libro):
    return {"menssage": f"Libro '{libro.titulo}' insertado"}
