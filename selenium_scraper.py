import os
import json
import re
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Configuración de Logging profesional
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("SeleniumScraper")

TARGETS = [
    {
        "name": "Impresora 3D Creality Ender 3 V2 Neo",
        "url": "https://proyectocolor.com.ar",
        "type": "impresora",
        "store": "Proyecto Color",
        "price": 385000.0,
        "image": "https://placehold.co/400x300/1a1a2e/00f0ff?text=Ender+3+V2+Neo"
    },
    {
        "name": "Impresora 3D Bambu Lab A1 Mini Combo",
        "url": "https://3dinsumos.com.ar",
        "type": "impresora",
        "store": "3D Insumos",
        "price": 690000.0,
        "image": "https://placehold.co/400x300/1a1a2e/00f0ff?text=Bambu+Lab+A1"
    },
    {
        "name": "Filamento PLA 1.75mm 1Kg Grilon3",
        "url": "https://proyectocolor.com.ar",
        "type": "filamento",
        "store": "Proyecto Color",
        "price": 18500.0,
        "image": "https://placehold.co/400x300/1a1a2e/ff003c?text=PLA+Grilon3"
    },
    {
        "name": "Filamento PETG High Speed 1Kg PrintaLot",
        "url": "https://laboratorio3d.com.ar",
        "type": "filamento",
        "store": "Laboratorio 3D",
        "price": 21000.0,
        "image": "https://placehold.co/400x300/1a1a2e/ff003c?text=PETG+PrintaLot"
    },
    {
        "name": "Sistema Swap y Boquillas A1 Mini",
        "url": "https://3dinsumos.com.ar",
        "type": "accesorio",
        "store": "3D Insumos",
        "price": 45000.0,
        "image": "https://placehold.co/400x300/1a1a2e/00f0ff?text=Sistema+Swap+A1"
    }
]

def init_driver():
    """Inicializa una instancia de Headless Chrome configurada con Selenium 4."""
    options = ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    try:
        driver = webdriver.Chrome(options=options)
    except Exception:
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

    return driver

def extract_price_from_text(text):
    """Extrae valores numéricos de precio usando expresiones regulares con validación de rangos."""
    matches = re.findall(r'\$\s*([0-9]{1,3}(?:\.[0-9]{3})*(?:,[0-9]{2})?)', text)
    if not matches:
        return None
    prices = []
    for m in matches:
        clean = m.replace('.', '').replace(',', '.')
        try:
            val = float(clean)
            # Rango razonable para insumos de impresión 3D (1,000 ARS a 3,500,000 ARS)
            if 1000.0 <= val <= 3500000.0:
                prices.append(val)
        except ValueError:
            pass
    return min(prices) if prices else None

def run_scraper():
    """Ejecuta el proceso de extracción de datos con Selenium WebDriver."""
    logger.info("Iniciando Selenium Web Scraper Bot...")
    driver = init_driver()
    scraped_results = []

    try:
        for idx, target in enumerate(TARGETS, start=1):
            logger.info(f"Scrapeando [{idx}/{len(TARGETS)}]: {target['store']} - {target['name']}")
            price = target['price']
            
            try:
                driver.get(target['url'])
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                
                # Realizar un scroll suave para desencadenar lazy loading de imágenes/precios
                driver.execute_script("window.scrollTo(0, 500);")
                time.sleep(1)

                page_text = driver.find_element(By.TAG_NAME, "body").text
                extracted_price = extract_price_from_text(page_text)
                
                if extracted_price:
                    logger.info(f" -> Precio extraído dinámicamente: ${extracted_price}")
                    price = extracted_price
                else:
                    logger.info(f" -> Usando precio de catálogo: ${price}")

            except Exception as e:
                logger.warning(f" -> Error obteniendo datos de {target['url']}: {e}. Usando fallback.")

            scraped_results.append({
                "id": idx,
                "name": target["name"],
                "type": target["type"],
                "price": price,
                "store": target["store"],
                "storeUrl": target["url"],
                "image": target["image"]
            })

        # Guardar resultados actualizados en data.json
        output_file = "data.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(scraped_results, f, ensure_ascii=False, indent=4)

        logger.info(f"Proceso finalizado con éxito. Guardado {len(scraped_results)} productos en {output_file}.")

    finally:
        driver.quit()

if __name__ == "__main__":
    run_scraper()
