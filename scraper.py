import requests
from bs4 import BeautifulSoup
import json
import re

# URLs de prueba para extraer precios reales
TARGETS = [
    {
        "url": "https://3dinsumos.com.ar/Producto/3DPrinter-SistemaSwapA1Mini",
        "type": "accesorio",
        "store": "3D Insumos",
        "image": "https://placehold.co/400x300/1a1a2e/00f0ff?text=Accesorio+3D"
    },
    {
        "url": "https://proyectocolor.com.ar/impresoras-3d/creality/ender-3-v2-neo",
        "type": "impresora",
        "store": "Proyecto Color",
        "image": "https://placehold.co/400x300/1a1a2e/00f0ff?text=Ender+3+V2+Neo"
    },
    {
        "url": "https://proyectocolor.com.ar/filamentos/pla/1kg",
        "type": "filamento",
        "store": "Proyecto Color",
        "image": "https://placehold.co/400x300/1a1a2e/ff003c?text=PLA+1Kg"
    },
    {
        "url": "https://laboratorio3d.com.ar/bambu-lab/",
        "type": "impresora",
        "store": "Laboratorio 3D",
        "image": "https://placehold.co/400x300/1a1a2e/00f0ff?text=Bambu+Lab"
    }
]

def extract_price(text):
    # Buscar patrones como $ 15.000,00 o $15000
    matches = re.findall(r'\$\s*([0-9]{1,3}(?:\.[0-9]{3})*(?:,[0-9]{2})?)', text)
    if not matches:
        return None
    
    prices = []
    for m in matches:
        # Convertir formato arg (15.000,00 -> 15000.00)
        clean = m.replace('.', '').replace(',', '.')
        try:
            prices.append(float(clean))
        except:
            pass
    
    if not prices: return None
    # A menudo hay precios de cuotas (menores) y precio total (mayor). Devolvemos el maximo o el primero lógico
    # Para ser conservador, tomamos el mayor asumiendo que es el precio total, no la cuota
    return max(prices)

def scrape():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    results = []
    _id = 1
    
    for target in TARGETS:
        print(f"Scrapeando: {target['url']}")
        try:
            r = requests.get(target['url'], headers=headers, timeout=10)
            soup = BeautifulSoup(r.text, 'html.parser')
            
            # Nombre del producto (Titulo de la pagina)
            title_tag = soup.find('title')
            name = title_tag.text.split('|')[0].strip() if title_tag else "Producto Desconocido"
            
            # Extraer precio de todo el texto de la pagina
            # (Metodo rustico pero efectivo cuando no sabemos la estructura exacta)
            body_text = soup.get_text()
            price = extract_price(body_text)
            
            if not price:
                # Fallback por si la web carga todo por JS
                price = 150000.0 if target['type'] == 'impresora' else 15000.0
                name += " (Precio Estimado - Web JS)"
                
            results.append({
                "id": _id,
                "name": name,
                "type": target['type'],
                "price": price,
                "store": target['store'],
                "storeUrl": target['url'],
                "image": target['image']
            })
            _id += 1
            print(f" -> Encontrado: {name} | Precio: ${price}")
            
        except Exception as e:
            print(f"Error con {target['url']}: {e}")
            
    # Guardar en JSON
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    print("Scraping completado. Datos guardados en data.json")

if __name__ == "__main__":
    scrape()
