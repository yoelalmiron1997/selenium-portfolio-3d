# 🚀 Selenium 4 QA Automation & Web Scraping Suite (Portafolio)

![Python Version](https://img.shields.io/badge/python-3.7%20%7C%203.10-blue.svg)
![Selenium](https://img.shields.io/badge/selenium-v4.11-green.svg)
![PyTest](https://img.shields.io/badge/pytest-v7.4-orange.svg)
![CI/CD](https://img.shields.io/badge/GitHub%20Actions-Automated-purple.svg)
![Deploy](https://img.shields.io/badge/GitHub%20Pages-Live%20Demo-brightgreen.svg)

Proyecto profesional de automatización utilizando **Selenium 4 WebDriver** en **Python**, implementando el patrón de diseño **Page Object Model (POM)** para pruebas E2E y un **Bot de Web Scraping dinámico**. Incluye integración continua (CI/CD) con **GitHub Actions** y despliegue automático en **GitHub Pages**.

---

## 🌐 Demo en Vivo & Reportes
- 🔗 **Aplicación Web Desplegada**: `https://<tu-usuario>.github.io/<tu-repositorio>/`
- 📊 **Reporte Interactivo de Pruebas HTML**: `https://<tu-usuario>.github.io/<tu-repositorio>/reports/report.html`

---

## 🛠️ Arquitectura del Proyecto

```text
├── .github/workflows/
│   └── deploy.yml          # Workflow de CI/CD para GitHub Actions
├── pages/
│   ├── __init__.py
│   ├── base_page.py        # Clase base POM con wrappers de WebDriverWait y capturas
│   └── home_page.py        # Page Object con localizadores y acciones del Comparador 3D
├── tests/
│   ├── __init__.py
│   └── test_comparator.py  # Suite de pruebas E2E con PyTest (Búsqueda, Filtros, Precios)
├── reports/
│   └── report.html         # Reporte interactivo generado automáticamente por pytest-html
├── conftest.py             # Fixtures de PyTest, configuración de Chrome Headless y Hooks
├── selenium_scraper.py     # Bot de scraping dinámico para extracción de precios reales
├── data.json               # Base de datos JSON parseada y consumida por el frontend
├── index.html              # Dashboard frontend interactivo
├── styles.css              # Estilos UI modernos con CSS nativo y Glassmorphism
├── app.js                  # Lógica del frontend y renderizado dinámico
├── requirements.txt        # Dependencias del proyecto
└── README.md               # Documentación principal del portafolio
```

---

## 💻 Características Principales

### 1. **Framework de QA Automation (E2E)**
- **Page Object Model (POM)**: Separación clara entre localizadores, acciones de página y aserciones de pruebas.
- **Esperas Explícitas (`WebDriverWait`)**: Eliminación de esperas estáticas (`sleep`) garantizando pruebas rápidas y estables ante latencia de red.
- **Visual & Headless Execution**: Soporte para ejecutar en modo silencioso (`--headless`) o visual en navegador real (`--headed`).
- **Capturas Automáticas en Fallo**: Captura de pantalla automática en `reports/screenshots/` si cualquier prueba falla.
- **Reporte HTML Interactivo**: Generación de reportes detallados con tiempos de ejecución, logs y capturas de pantalla.

### 2. **Selenium Dynamic Web Scraper Bot**
- Automatización de navegadores en segundo plano para extraer precios de productos en tiempo real desde e-commerce reales.
- Manejo de renderizado dinámico en JavaScript, scroll automático y parseo confiable en `data.json`.

### 3. **Pipeline de CI/CD en la Nube (GitHub Actions)**
- Ejecución automática de pruebas e2e y scraper en cada `push` o mediante un cron job diario.
- Publicación automática de la aplicación web y reportes en **GitHub Pages**.

---

## ⚙️ Instalación y Ejecución Local

### 1. Clonar el repositorio e instalar dependencias
```bash
git clone https://github.com/<tu-usuario>/<tu-repositorio>.git
cd <tu-repositorio>
pip install -r requirements.txt
```

### 2. Ejecutar la Suite de Pruebas Automatizadas (PyTest)
```bash
# Modo Headless (Por defecto) con reporte HTML
pytest tests/ --html=reports/report.html --self-contained-html

# Modo Visual (Abre el navegador Chrome en pantalla)
pytest tests/ --headed
```

### 3. Ejecutar el Scraper de Selenium
```bash
python selenium_scraper.py
```

---

## 🚀 Pasos para Activar tu Deploy en GitHub Pages

1. Subir este proyecto a un nuevo repositorio de GitHub:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Selenium QA & Scraper Portfolio"
   git branch -M main
   git remote add origin https://github.com/<tu-usuario>/<nombre-repo>.git
   git push -u origin main
   ```
2. Ir a **Settings > Pages** en tu repositorio de GitHub.
3. En **Source**, seleccionar la rama **`gh-pages`** y guardar.
4. ¡Listo! Tu aplicación estará desplegada en `https://<tu-usuario>.github.io/<nombre-repo>/`.
