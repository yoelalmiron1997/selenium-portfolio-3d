# 🚀 Selenium 4 QA & Scraping Portfolio

Suite de automatización en **Python** con **Selenium 4**, **PyTest** (patrón *Page Object Model*) y un bot de **Web Scraping** para un comparador de precios de impresión 3D. Incluye integración continua y despliegue automático en **GitHub Pages**.

---

## 🌐 Links del Proyecto
- 🔗 **Demo en Vivo**: [https://yoelalmiron1997.github.io/selenium-portfolio-3d/](https://yoelalmiron1997.github.io/selenium-portfolio-3d/)
- 📊 **Reporte de Pruebas HTML**: [https://yoelalmiron1997.github.io/selenium-portfolio-3d/reports/report.html](https://yoelalmiron1997.github.io/selenium-portfolio-3d/reports/report.html)

---

## 🛠️ Tecnologías y Patrones

- **Python 3.10** + **Selenium 4 WebDriver**
- **PyTest** con arquitectura **Page Object Model (POM)** y `WebDriverWait`
- **Web Scraping**: Extracción de datos dinámicos en sitio e-commerce
- **CI/CD & Deploy**: GitHub Actions ejecutando Chrome Headless en la nube

---

## 🚀 Instalación y Uso Local

```bash
# 1. Clonar e instalar dependencias
git clone https://github.com/yoelalmiron1997/selenium-portfolio-3d.git
cd selenium-portfolio-3d
pip install -r requirements.txt

# 2. Ejecutar Pruebas QA (Modo Headless)
pytest tests/ --html=reports/report.html --self-contained-html

# 3. Ejecutar Pruebas QA en navegador visible
pytest tests/ --headed

# 4. Ejecutar el Bot de Scraping
python selenium_scraper.py
```
