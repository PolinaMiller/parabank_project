from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """
    Базовый класс для всех страниц, предоставляющий общие методы для взаимодействия с веб-элементами.
    Этот класс следует использовать как родительский для всех страниц в тестовом фреймворке,
    что обеспечивает единообразное и переиспользуемое взаимодействие с элементами страницы.
    """

    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализирует базовую страницу с использованием предоставленного экземпляра WebDriver.

        :param driver: Экземпляр WebDriver, используемый для взаимодействия с браузером.
        """
        self.driver = driver

    def find_element(self, locator: tuple) -> WebElement:
        """
        Находит и возвращает веб-элемент, соответствующий указанному локатору.

        :param locator: Кортеж (By, значение), например, (By.ID, "element_id").
        :return: Найденный веб-элемент.
        """
        return self.driver.find_element(*locator)

    def click(self, locator: tuple) -> None:
        """
        Находит элемент по локатору и выполняет по нему клик.

        :param locator: Локатор элемента, например, (By.XPATH, "//button[@id='submit']").
        """
        element = self.find_element(locator)
        element.click()

    def send_keys(self, locator: tuple, keys: str) -> None:
        """
        Очищает поле, найденное по указанному локатору, и вводит заданный текст.

        :param locator: Локатор элемента, например, (By.ID, "username").
        :param keys: Текст, который необходимо ввести в элемент.
        """
        element = self.find_element(locator)
        element.clear()
        element.send_keys(keys)

    def wait_for_element(self, locator: tuple, timeout: int = 15) -> WebElement:
        """
        Ожидает появления видимого элемента на странице в течение заданного времени.

        :param locator: Локатор элемента, например, (By.CSS_SELECTOR, ".success").
        :param timeout: Максимальное время ожидания в секундах (по умолчанию 15 секунд).
        :return: Найденный веб-элемент, если он появляется в течение заданного времени.
        :raises: TimeoutException, если элемент не найден за указанный период.
        """
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
