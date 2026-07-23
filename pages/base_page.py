import os
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class BasePage:
    """Clase Base que encapsula las operaciones fundamentales de Selenium WebDriver utilizando esperas explícitas."""

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)

    def open_url(self, url):
        """Abre la URL especificada."""
        self.driver.get(url)

    def find_element(self, locator):
        """Espera a que un elemento esté presente en el DOM y lo retorna."""
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_elements(self, locator):
        """Retorna una lista de elementos que coinciden con el localizador."""
        try:
            return self.wait.until(EC.presence_of_all_elements_located(locator))
        except TimeoutException:
            return []

    def wait_for_element_visible(self, locator, custom_timeout=None):
        """Espera a que un elemento sea visible en la interfaz."""
        timeout = custom_timeout if custom_timeout else self.timeout
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator):
        """Espera a que un elemento sea interactuable y hace clic en él."""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
        return element

    def type_text(self, locator, text, clear_first=True):
        """Escribe texto en un campo de entrada después de esperar su visibilidad."""
        element = self.wait_for_element_visible(locator)
        if clear_first:
            element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        """Obtiene el texto visible de un elemento."""
        element = self.wait_for_element_visible(locator)
        return element.text

    def get_attribute(self, locator, attribute):
        """Obtiene el valor de un atributo HTML de un elemento."""
        element = self.find_element(locator)
        return element.get_attribute(attribute)

    def is_element_displayed(self, locator, timeout=3):
        """Verifica si un elemento está desplegado visualmente sin lanzar una excepción."""
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def scroll_to_element(self, locator):
        """Realiza scroll hasta que el elemento sea visible."""
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)

    def take_screenshot(self, filename):
        """Guarda una captura de pantalla en la ruta indicada."""
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        self.driver.save_screenshot(filename)
