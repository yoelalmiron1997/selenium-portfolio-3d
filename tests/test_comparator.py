import os
import pytest
from pages.home_page import HomePage

# Obtener ruta absoluta al index.html local para las pruebas
abs_path = os.path.abspath('index.html').replace('\\', '/')
LOCAL_INDEX_PATH = f"file:///{abs_path}"

class TestComparador3D:
    """Suite de pruebas E2E automatizadas para la aplicación web Comparador 3D usando Selenium WebDriver."""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Precondición: Navegar a la página principal antes de cada prueba."""
        self.home_page = HomePage(driver)
        self.home_page.open_url(LOCAL_INDEX_PATH)

    def test_load_homepage(self):
        """Verifica la carga correcta de la página principal y sus componentes esenciales."""
        header_text = self.home_page.get_text(self.home_page.HERO_TITLE)
        assert "Impresión 3D" in header_text, "El título principal no coincide."
        
        initial_count = self.home_page.get_displayed_products_count()
        assert initial_count > 0, "No se cargaron tarjetas de productos en la grilla inicial."

    def test_search_functionality(self):
        """Verifica el filtrado de productos por término de búsqueda en tiempo real."""
        search_query = "Ender"
        self.home_page.search_for(search_query)

        titles = self.home_page.get_product_titles()
        assert len(titles) > 0, f"No se encontraron productos para la búsqueda: '{search_query}'."
        for title in titles:
            assert search_query.lower() in title.lower(), f"El producto '{title}' no coincide con la búsqueda '{search_query}'."

    def test_category_filter_printers(self):
        """Verifica el filtro de categorías por 'Impresoras 3D'."""
        self.home_page.select_category("impresora")
        
        count = self.home_page.get_displayed_products_count()
        assert count > 0, "El filtro de impresoras 3D no devolvió ningún resultado."

    def test_sorting_by_price_asc_and_desc(self):
        """Valida que los productos se ordenen correctamente por precio ascendente y descendente."""
        # 1. Probar orden ascendente
        self.home_page.sort_by("price-asc")
        prices_asc = self.home_page.get_product_prices()
        assert len(prices_asc) > 1, "Se requieren al menos 2 productos para validar el ordenamiento."
        assert prices_asc == sorted(prices_asc), f"Los precios no están en orden ascendente: {prices_asc}"

        # 2. Probar orden descendente
        self.home_page.sort_by("price-desc")
        prices_desc = self.home_page.get_product_prices()
        assert prices_desc == sorted(prices_desc, reverse=True), f"Los precios no están en orden descendente: {prices_desc}"

    def test_search_no_results(self):
        """Verifica que una búsqueda sin coincidencias muestre 0 resultados."""
        self.home_page.search_for("ProductoInexistente12345")
        count = self.home_page.get_displayed_products_count()
        assert count == 0, "Se esperaba 0 resultados para un término de búsqueda inexistente."
