# Sentiment Analysis and Web Scraping API

This project is a FastAPI-based application that performs web scraping on various news websites and conducts sentiment analysis on the extracted headlines using the Hugging Face Transformers library. [2024-11-29]

---

## Setup Guide

### Requirements
- **Python Version:** 3.12 is recommended for compatibility with the Transformers library.
- **Tools:**
  - Rust (for compiling some dependencies in Transformers)
  - Visual Studio Installer with the `Desktop development with C++` workload
  - Hugging Face token (for accessing certain models)

---

### Video Tutorial to create the API
[Crea una API con Python en menos de 5 minutos (Fast API)](https://www.youtube.com/watch?v=J0y2tjBz2Ao)

---

### Steps to Set Up the Environment

#### 1. Create a Virtual Environment
Ahora vamos a crear el archivo necesario para hacer la api, abrimos una nueva terminal y creamos una nueva carpeta.

Una vez dentro de esta, creamos un entorno virtual (lo llamaré `fastapi-env` para evitar conflictos con otros proyectos:
- On Windows:
  ```bash
  python -m venv fastapi-env
  ```
- On Ubuntu/Linux:
  ```bash
  python3 -m venv fastapi-env
  ```

#### 2. Activate the Virtual Environment
- On Windows:
  ```bash
  fastapi-env\Scripts\activate
  ```
- On Ubuntu/Linux:
  ```bash
  source fastapi-env/bin/activate
  ```

#### 3. Install Dependencies
If a `requirements.txt` file exists:
```bash
pip install -r requirements.txt
```

If no `requirements.txt` is available, install the required packages manually:
```bash
pip install fastapi uvicorn requests beautifulsoup4 transformers torch
```
> [!NOTE]
> If you are using **Python 3.13**, it is recommended to use Anaconda, as its Python version is compatible with this project.

#### 4. Install Rust (Required for Transformers)
Visit the [Rust installation](https://rustup.rs/) page and follow the instructions for your platform.

---

### Optional Setup (GeoIP-Based Access)
- Install GeoIP2 for demographic-based access restriction:
  ```bash
  pip install geoip2
  ```
- Download the GeoIP database from [MaxMind's website](https://dev.maxmind.com/geoip/geolocate-an-ip/databases/).

- Ejemplo del código:
  ```python
  from fastapi import FastAPI, HTTPException, Request
  import geoip2.database
  
  app = FastAPI()
  
  # Load the pre-trained GeoIP database for location-based access
  # The GeoLite2-City.mmdb file must be downloaded from MaxMind's website
  geoip_reader = geoip2.database.Reader('GeoLite2-City.mmdb')  # Ensure this file is in your project directory
  
  # Function to check if the user is allowed based on their IP location
  def is_user_allowed(ip: str) -> bool:
      try:
          # Query the IP address using the GeoIP2 database
          response = geoip_reader.city(ip)
  
          # Check if the country is Spain (ISO code "ES")
          if response.country.iso_code != "ES":
              return False
          
          # Check if the region is Andalusia
          if response.subdivisions.most_specific.name != "Andalucía":
              return False
          
          # Check if the city is Málaga
          if response.city.name != "Málaga":
              return False
          
          return True  # If all conditions are met, allow access
      except Exception as e:
          # Handle any exception (e.g., invalid IP address or GeoIP query failure)
          return False
  
  # Endpoint to access the content and check the user's location
  @app.get("/scrapping_CNN")
  def obtener_titulares_CNN(request: Request):
      user_ip = request.client.host  # Get the IP address of the user
  
      # Check if the user is allowed based on their geographical location
      if not is_user_allowed(user_ip):
          raise HTTPException(status_code=403, detail="Access Denied: You must be from Málaga, Andalucía, Spain.")
  
      # Continue with the scraping and sentiment analysis (from your existing code)
      try:
          # Call the scraping function
          news_items = content_web_CNN()
  
          # Perform sentiment analysis on the extracted titles
          sentiment_results = analyze_sentiments_CNN(news_items)
  
          # Return the sentiment results and the titles
          return {"result": sentiment_results, "amount": len(sentiment_results)}
  
      except Exception as e:
          return {"error": str(e)}
  ```
  
---

### Hugging Face Token Setup
1. Visit [Hugging Face](https://huggingface.co/) and create an account.
2. Navigate to your [account settings](https://huggingface.co/settings/tokens) and generate a personal access token.
3. Use the token in the project by logging in (only required once):
```python
from huggingface_hub import login
login("your_huggingface_token_here")
```

---

### Running the API
1. Create a file named `main.py` containing the application code.
2. Start the FastAPI server using uvicorn:
   ```bash
   uvicorn main:app --reload
   ```
  For remote hosting:
  ```bash
  uvicorn main:app --host 0.0.0.0 --port 8000 --reload
  ```
3. Deactivate the virtual enviroment when done:
   ```bash
   deactivate
   ```
   Or `CTLR + C`

If deactivation doesn't work, identify and terminate the `uvicorn` process:
```bash
tasklist | findstr uvicorn
taskkill /PID <PID>
```

---

### Generating a Requirements File
To create a `requirements.txt` file for deployment:
```bash
pip freeze > requirements.txt
```

---

### Project Features
#### API Endpoints
- GET `/scrapping_bbc`: Scrapes and analyzes headlines from BBC.
- GET `/scrapping_cnn`: Scrapes and analyzes headlines from CNN.
- GET `/scrapping_nytimes`: Scrapes and analyzes headlines from The New York Times.
- GET `/`: Displays project credits.
- GET `/docs`: Documento de la api creada automáticamente por FastAPI.

#### Sentiment Analysis
The project uses Hugging Face's `yiyanghkust/finbert-tone` model for analyzing sentiment (Positive, Neutral, Negative).

#### URL for Local Access
- [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

### Additional Notes
