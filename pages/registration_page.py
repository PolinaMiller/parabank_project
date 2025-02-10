from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class RegistrationPage(BasePage):
    # Локаторы полей формы регистрации
    FIRST_NAME_INPUT = (
        By.XPATH, "//form[@id='customerForm']//input[@id='customer.firstName']")
    LAST_NAME_INPUT = (
        By.XPATH, "//form[@id='customerForm']//input[@id='customer.lastName']")
    ADDRESS_INPUT = (
        By.XPATH, "//form[@id='customerForm']//input[@id='customer.address.street']")
    CITY_INPUT = (
        By.XPATH, "//form[@id='customerForm']//input[@id='customer.address.city']")
    STATE_INPUT = (
        By.XPATH, "//form[@id='customerForm']//input[@id='customer.address.state']")
    ZIP_CODE_INPUT = (
        By.XPATH, "//form[@id='customerForm']//input[@id='customer.address.zipCode']")
    PHONE_INPUT = (
        By.XPATH, "//form[@id='customerForm']//input[@id='customer.phoneNumber']")
    SSN_INPUT = (
        By.XPATH, "//form[@id='customerForm']//input[@id='customer.ssn']")
    USERNAME_INPUT = (
        By.XPATH, "//form[@id='customerForm']//input[@id='customer.username']")
    PASSWORD_INPUT = (
        By.XPATH, "//form[@id='customerForm']//input[@id='customer.password']")
    CONFIRM_PASSWORD_INPUT = (
        By.XPATH, "//form[@id='customerForm']//input[@id='repeatedPassword']")
    REGISTER_BUTTON = (
        By.XPATH, "//form[@id='customerForm']//input[@value='Register']")

    # Локатор для сообщения об ошибке регистрации (отображается, если регистрация не удалась)
    ERROR_MESSAGE = (
        By.XPATH, "//span[contains(@class, 'error') or contains(text(), 'error')]")

    # Локатор для ссылки "Log Out", которая должна появляться после успешной регистрации
    LOGOUT_LINK = (By.XPATH, "//a[contains(text(), 'Log Out')]")

    def register(self, first_name, last_name, address, city, state, zip_code,
                 phone, ssn, username, password, confirm_password):
        """
        Заполняет форму регистрации и отправляет ее.

        :param first_name: Имя пользователя.
        :param last_name: Фамилия пользователя.
        :param address: Адрес (улица, дом).
        :param city: Город.
        :param state: Штат/Область.
        :param zip_code: Почтовый индекс.
        :param phone: Номер телефона.
        :param ssn: Социальное страхование (SSN).
        :param username: Имя пользователя для входа.
        :param password: Пароль.
        :param confirm_password: Подтверждение пароля.
        """
        self.send_keys(self.FIRST_NAME_INPUT, first_name)
        self.send_keys(self.LAST_NAME_INPUT, last_name)
        self.send_keys(self.ADDRESS_INPUT, address)
        self.send_keys(self.CITY_INPUT, city)
        self.send_keys(self.STATE_INPUT, state)
        self.send_keys(self.ZIP_CODE_INPUT, zip_code)
        self.send_keys(self.PHONE_INPUT, phone)
        self.send_keys(self.SSN_INPUT, ssn)
        self.send_keys(self.USERNAME_INPUT, username)
        self.send_keys(self.PASSWORD_INPUT, password)
        self.send_keys(self.CONFIRM_PASSWORD_INPUT, confirm_password)
        self.click(self.REGISTER_BUTTON)

    def is_registration_successful(self):
        """
        Проверяет, что регистрация прошла успешно, ожидая появления ссылки "Log Out".

        :return: True, если ссылка "Log Out" обнаружена на странице, иначе False.
        """
        try:
            self.wait_for_element(self.LOGOUT_LINK, timeout=15)
            return True
        except Exception:
            return False

    def get_error_message(self):
        """
        Возвращает текст сообщения об ошибке, возникающем при неуспешной регистрации.

        :return: Строка с текстом ошибки, если сообщение найдено; иначе, None.
        """
        try:
            error_element = self.wait_for_element(
                self.ERROR_MESSAGE, timeout=5)
            return error_element.text
        except Exception:
            return None
