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


################################################################################################################################
# Function to perform web scraping
def generic_web_content(url, tag, class1=None, class2=None, subtitle_tag=None):
    # Verify that the request was successful (status code 200)
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Error accessing the website: {response.status_code}")

    # Step 2: Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Step 3: Extract the main elements (tags with optional class)
    if class1:
        elements = soup.find_all(tag, class_=class1)
    else:
        elements = soup.find_all(tag)

    # List to store the results
    results = []
    
    # Extract title and link
    for element in elements:
        # Extract the link (the 'href' attribute value of the tag)
        relative_link = element.get("href")
        if relative_link:
            # Convert to full URL if necessary
            full_link = urljoin(url, relative_link) if relative_link.startswith('/') else relative_link

            # Extract the text from the secondary tag if specified
            if subtitle_tag:
                if class2:
                    # If class2 is a list or tuple, check if any match
                    if isinstance(class2, (list, tuple)):
                        for cls in class2:
                            subtitle = element.find(subtitle_tag, class_=cls)
                            # Break the loop if a subtitle is found
                            if subtitle:
                                break
                    # If class2 is a single class
                    else:  
                        subtitle = element.find(subtitle_tag, class_=class2)
                else:
                    subtitle = element.find(subtitle_tag)
                if subtitle:
                    text = subtitle.get_text(strip=True)
                else:
                    text = None
            else:
                text = element.get_text(strip=True)

            # Add to results if both are present
            if text and full_link:
                results.append({"title": text, "link": full_link})

    return results

# Function to removes duplicates from a list.
def remove_duplicates(lst):
    unique_list = []
    for item in lst:
        if item not in unique_list:
            unique_list.append(item)
    return unique_list

# Function to analyze the sentiments of the news_items
def analyze_sentiments(news_items):
    # Analyzes the sentiments of the titles and associates them with their links
    results = []

    for i, r in enumerate(news_items):
        try:
            # Analyze the sentiment of the title
            sentiment = sentiment_pipeline(r['title'])

            # Add the result
            results.append({
                "title": r['title'],
                "link": r['link'],
                "sentiment": sentiment[0]['label'],
                "precision": sentiment[0]['score'] * 100
            })
        except Exception as e:
            # Handle cases where sentiment analysis or data is invalid
            print(f"Error analyzing sentiment for: {r.get('title', 'Unknown')} - {e}")
            results.append({
                "title": r.get('title', 'Unknown'),
                "link": r.get('link', 'Unknown'),
                "sentiment": "UNKNOWN",
                "confidence": 0.0
            })

    # Sort the results by precision in descending order
    if results:
        results = sorted(results, key=lambda x: x['precision'], reverse=True)
    
    return results

################################################################################################################################

# Endpoint to get the news items and their sentiments
# Scrapes headlines from BBC and performs sentiment analysis.
@app.get("/scrapping_bbc")
def scrape_bbc_headlines():
    try:
        # URL and parameters for BBC scraping
        url = "https://bbc.com"
        tag = "a"
        class1 = "sc-2e6baa30-0 gILusN"
        class2 = ["sc-8ea7699c-3 dhclWg", "sc-8ea7699c-3 hlhXXQ"]
        subtitle_tag = "h2"

        # Scraping content from BBC
        news_items = generic_web_content(url, tag, class1, class2, subtitle_tag)

        # Remove duplicates
        unique_news_items = remove_duplicates(news_items)

        # Perform sentiment analysis
        sentiment_results = analyze_sentiments(unique_news_items)

        # Return the results
        return {
            "result": sentiment_results,
            "amount": len(sentiment_results)
        }

    except Exception as e:
        return {"error": str(e)}


# CNN Endpoint
@app.get("/scrapping_cnn")
def scrape_cnn_headlines():
    try:
        # URL and parameters for CNN scraping
        url = "https://cnn.com"
        tag = "a"
        class1 = "container__link"
        class2 = "container__headline-text"
        subtitle_tag = "span"

        # Scraping content from CNN
        news_items = generic_web_content(url, tag, class1, class2, subtitle_tag)

        # Remove duplicates
        unique_news_items = remove_duplicates(news_items)

        # Perform sentiment analysis
        sentiment_results = analyze_sentiments(unique_news_items)

        # Return the results
        return {
            "result": sentiment_results,
            "amount": len(sentiment_results)
        }

    except Exception as e:
        return {"error": str(e)}

# NYTimes Endpoint
@app.get("/scrapping_nytimes")
def scrape_nytimes_headlines():
    try:
        # URL and parameters for NYTimes scraping
        url_nytimes = "https://www.nytimes.com/international/section/world?page=10"
        
        # Scraping content from NYTimes
        news_items_1 = generic_web_content(url_nytimes, tag="a", class1="css-1u3p7j1")
        news_items_2 = generic_web_content(url_nytimes, tag="a", class1="css-8hzhxf", class2="css-1j88qqx e15t083i0", subtitle_tag="h3")
        
        # Combine results
        news_items = news_items_1 + news_items_2

        # Remove duplicates
        unique_news_items = remove_duplicates(news_items)

        # Perform sentiment analysis
        sentiment_results = analyze_sentiments(unique_news_items)

        # Return the results
        return {
            "result": sentiment_results,
            "amount": len(sentiment_results)
        }

    except Exception as e:
        return {"error": str(e)}


# Endpoint for getting the credits from an API
@app.get("/")
def index():
    return {"Credits" : "Created by 'David Moreno Cerezo' and 'Jairo Andrades Bueno'"}

################################################################################################################################
