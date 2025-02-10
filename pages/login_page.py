from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class LoginPageElementary(BasePage):
    """
    Элементарный объект страницы входа.
    Содержит локаторы и базовые методы для непосредственного взаимодействия с элементами страницы.
    """
    # Локаторы для элементов страницы входа
    USERNAME_INPUT = (
        By.XPATH, "//div[@id='loginPanel']//input[@name='username']")
    PASSWORD_INPUT = (
        By.XPATH, "//div[@id='loginPanel']//input[@name='password']")
    LOGIN_BUTTON = (By.XPATH, "//input[@value='Log In']")
    ERROR_MESSAGE = (
        By.XPATH, "//div[@id='updateProfileError']//h1[@class='Error!']")

    def enter_username(self, username: str) -> None:
        """Вводит имя пользователя в поле ввода."""
        self.send_keys(self.USERNAME_INPUT, username)

    def enter_password(self, password: str) -> None:
        """Вводит пароль в поле ввода."""
        self.send_keys(self.PASSWORD_INPUT, password)

    def click_login_button(self) -> None:
        """Нажимает на кнопку входа."""
        self.click(self.LOGIN_BUTTON)

    def wait_for_error_message(self, timeout: int = 15):
        """
        Ожидает появления сообщения об ошибке.

        :param timeout: Время ожидания в секундах.
        :return: Элемент сообщения об ошибке или исключение при таймауте.
        """
        return self.wait_for_element(self.ERROR_MESSAGE, timeout=timeout)

    def is_error_message_displayed(self, timeout: int = 15) -> bool:
        """
        Проверяет, отображается ли сообщение об ошибке.

        :param timeout: Время ожидания в секундах.
        :return: True, если сообщение об ошибке найдено, иначе False.
        """
        try:
            self.wait_for_error_message(timeout=timeout)
            return True
        except Exception:
            return False


class LoginPage(LoginPageElementary):
    """
    Page Object для страницы входа.
    Объединяет элементарные методы в высокоуровневые операции, такие как вход в систему и проверка ошибок.
    """

    def login(self, username: str, password: str) -> None:
        """
        Выполняет вход в систему: вводит имя пользователя, пароль и нажимает кнопку "Log In".

        :param username: Имя пользователя.
        :param password: Пароль.
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()

    def is_error_displayed(self) -> bool:
        """
        Проверяет, отображается ли сообщение об ошибке при неудачной попытке входа.

        :return: True, если сообщение об ошибке найдено, иначе False.
        """
        return self.is_error_message_displayed(timeout=15)


class LoginService:
    """
    Сервисный объект для работы со страницей входа.
    Инкапсулирует бизнес-логику (например, процедуру авторизации), используя Page Object LoginPage.
    """

    def __init__(self, driver):
        self.page = LoginPage(driver)

    def login(self, username: str, password: str) -> None:
        """
        Выполняет вход в систему через Page Object.

        :param username: Имя пользователя.
        :param password: Пароль.
        """
        self.page.login(username, password)

    def is_error_displayed(self) -> bool:
        """
        Проверяет, отображается ли сообщение об ошибке при попытке входа.

        :return: True, если сообщение об ошибке найдено, иначе False.
        """
        return self.page.is_error_displayed()
