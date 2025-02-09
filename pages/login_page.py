from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class LoginPage(BasePage):
    USERNAME_INPUT = (
        By.XPATH, "//div[@id='loginPanel']//input[@name='username']")
    PASSWORD_INPUT = (
        By.XPATH, "//div[@id='loginPanel']//input[@name='password']")
    LOGIN_BUTTON = (By.XPATH, "//input[@value='Log In']")
    ERROR_MESSAGE = (
        By.XPATH, "//div[@id='updateProfileError']//h1[@class='Error!']")

    def login(self, username, password):
        self.send_keys(self.USERNAME_INPUT, username)
        self.send_keys(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def is_error_displayed(self):
        try:
            self.wait_for_element(self.ERROR_MESSAGE, timeout=15)
            return True
        except Exception:
            return False
