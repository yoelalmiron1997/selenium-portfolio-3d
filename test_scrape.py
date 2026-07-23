import requests
from bs4 import BeautifulSoup
import json

def test_scrape(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Try to find common product containers
        print(f"--- {url} ---")
        items = soup.find_all(['div', 'li', 'article'], class_=lambda x: x and ('product' in x.lower() or 'item' in x.lower()))
        print(f"Found {len(items)} possible product items.")
        
        if items:
            for i, item in enumerate(items[:3]): # Check first 3
                title = item.find(['h2', 'h3', 'a'], class_=lambda x: x and ('title' in x.lower() or 'name' in x.lower()))
                price = item.find(['span', 'div', 'p'], class_=lambda x: x and 'price' in x.lower())
                link = item.find('a')
                img = item.find('img')
                
                print(f"Item {i}:")
                if title: print(f"  Title: {title.text.strip()}")
                if price: print(f"  Price: {price.text.strip()}")
                if link and link.has_attr('href'): print(f"  Link: {link['href']}")
                if img and img.has_attr('src'): print(f"  Img: {img['src']}")
        else:
            print("Could not find product items with generic classes.")
            
    except Exception as e:
        print(f"Error: {e}")

test_scrape("https://3dinsumos.com.ar/Productos?search=ender+3")
test_scrape("https://proyectocolor.com.ar/search/?q=ender+3")
