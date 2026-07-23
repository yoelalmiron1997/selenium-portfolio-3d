from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import time

class HomePage(BasePage):
    """Page Object para la página principal del Comparador 3D."""

    # Localizadores (By tuples)
    SEARCH_INPUT = (By.ID, "searchInput")
    SEARCH_BUTTON = (By.ID, "searchButton")
    RESULTS_TITLE = (By.ID, "resultsTitle")
    RESULTS_GRID = (By.ID, "resultsGrid")
    PRODUCT_CARDS = (By.CSS_SELECTOR, "#resultsGrid .card")
    SORT_SELECT = (By.ID, "sortSelect")
    LOADER = (By.ID, "loader")
    STORE_FILTERS_CONTAINER = (By.ID, "storeFilters")
    HERO_TITLE = (By.TAG_NAME, "h1")

    # Localizadores dinámicos por valor
    @staticmethod
    def category_radio_locator(category_value):
        return (By.CSS_SELECTOR, f'input[name="category"][value="{category_value}"]')

    @staticmethod
    def store_checkbox_locator(store_name):
        return (By.XPATH, f'//div[@id="storeFilters"]//label[contains(text(), "{store_name}")]/input')

    def __init__(self, driver, timeout=10):
        super().__init__(driver, timeout)

    def search_for(self, query):
        """Realiza una búsqueda ingresando texto y presionando el botón de búsqueda."""
        self.type_text(self.SEARCH_INPUT, query)
        self.click(self.SEARCH_BUTTON)
        time.sleep(0.8) # Esperar a que pase el setTimeout de app.js (600ms)

    def select_category(self, category_value):
        """Selecciona una categoría por su valor ('all', 'impresora', 'filamento')."""
        locator = self.category_radio_locator(category_value)
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].click();", element)
        time.sleep(0.8)

    def sort_by(self, option_value):
        """Ordena los productos seleccionando 'price-asc' o 'price-desc'."""
        select_element = self.find_element(self.SORT_SELECT)
        for option in select_element.find_elements(By.TAG_NAME, "option"):
            if option.get_attribute("value") == option_value:
                option.click()
                break
        time.sleep(0.8)

    def get_displayed_products_count(self):
        """Retorna la cantidad de tarjetas de producto actualmente visibles."""
        time.sleep(0.8)
        cards = self.driver.find_elements(*self.PRODUCT_CARDS)
        return len(cards)

    def get_product_titles(self):
        """Retorna una lista con los títulos de todos los productos visibles."""
        time.sleep(0.8)
        cards = self.driver.find_elements(*self.PRODUCT_CARDS)
        titles = []
        for card in cards:
            title_elem = card.find_element(By.TAG_NAME, "h3")
            titles.append(title_elem.text.strip())
        return titles

    def get_product_prices(self):
        """Retorna una lista con los precios numéricos de todos los productos visibles."""
        time.sleep(0.8)
        cards = self.driver.find_elements(*self.PRODUCT_CARDS)
        prices = []
        for card in cards:
            price_elem = card.find_element(By.CLASS_NAME, "card-price")
            # Extraer solo el número (ejemplo: "$ 150.000" -> 150000.0)
            text = price_elem.text.replace("$", "").replace(".", "").replace(",", ".").replace("\xa0", "").strip()
            try:
                prices.append(float(text))
            except ValueError:
                pass
        return prices

    def get_results_title_text(self):
        """Obtiene el texto del encabezado de resultados."""
        return self.get_text(self.RESULTS_TITLE)
