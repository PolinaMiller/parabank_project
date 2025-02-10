from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePageElementary:
    """
    Элементарный базовый класс для всех страниц.

    Реализует низкоуровневые операции с веб-элементами, такие как поиск,
    клики, ввод текста и ожидание появления элементов.

    Используется как фундамент для построения Page Object, наследуемых от него,
    а также применяется в Service Object для непосредственного взаимодействия с элементами.
    """

    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализирует объект страницы с использованием экземпляра WebDriver.

        :param driver: Экземпляр WebDriver для взаимодействия с браузером.
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


class BasePageObject(BasePageElementary):
    """
    Базовый класс для Page Object.

    Наследует все элементарные операции из BasePageElementary и служит основой для
    построения высокоуровневых моделей страниц, инкапсулирующих взаимодействие с элементами.
    """
    # Здесь можно определить общие для всех Page Object методы, если потребуется.
    pass


class BaseServiceObject:
    """
    Базовый класс для Service Object.

    Сервисный объект инкапсулирует бизнес-логику, используя Page Object классы,
    и предоставляет единый доступ к драйверу для реализации бизнес-процессов.
    """

    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализирует сервисный объект с использованием экземпляра WebDriver.

        :param driver: Экземпляр WebDriver для взаимодействия с браузером.
        """
        self.driver = driver
