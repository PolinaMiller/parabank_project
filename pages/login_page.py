from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class LoginPage(BasePage):
    """
    Страница входа в систему, обеспечивающая ввод учетных данных и проверку ошибок авторизации.
    """

    # Локатор для поля ввода имени пользователя
    USERNAME_INPUT = (
        By.XPATH, "//div[@id='loginPanel']//input[@name='username']")
    # Локатор для поля ввода пароля
    PASSWORD_INPUT = (
        By.XPATH, "//div[@id='loginPanel']//input[@name='password']")
    # Локатор для кнопки входа
    LOGIN_BUTTON = (By.XPATH, "//input[@value='Log In']")
    # Локатор для сообщения об ошибке при неудачной попытке входа
    ERROR_MESSAGE = (
        By.XPATH, "//div[@id='updateProfileError']//h1[@class='Error!']")

    def login(self, username: str, password: str) -> None:
        """
        Выполняет вход в систему, заполняя поля имени пользователя и пароля, затем нажимая кнопку "Log In".

        :param username: Имя пользователя.
        :param password: Пароль.
        """
        self.send_keys(self.USERNAME_INPUT, username)
        self.send_keys(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def is_error_displayed(self) -> bool:
        """
        Проверяет, отображается ли сообщение об ошибке на странице входа.

        :return: True, если сообщение об ошибке найдено в течение 15 секунд, иначе False.
        """
        try:
            self.wait_for_element(self.ERROR_MESSAGE, timeout=15)
            return True
        except Exception:
            return False
