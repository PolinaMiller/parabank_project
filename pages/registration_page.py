from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class RegistrationPageElementary(BasePage):
    """
    Элементарный объект страницы регистрации.
    Содержит локаторы и базовые методы для взаимодействия с элементами страницы.
    """
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

    # Локаторы для сообщений/состояний
    ERROR_MESSAGE = (
        By.XPATH, "//span[contains(@class, 'error') or contains(text(), 'error')]")
    LOGOUT_LINK = (By.XPATH, "//a[contains(text(), 'Log Out')]")

    # Методы для работы с отдельными элементами
    def enter_first_name(self, first_name):
        self.send_keys(self.FIRST_NAME_INPUT, first_name)

    def enter_last_name(self, last_name):
        self.send_keys(self.LAST_NAME_INPUT, last_name)

    def enter_address(self, address):
        self.send_keys(self.ADDRESS_INPUT, address)

    def enter_city(self, city):
        self.send_keys(self.CITY_INPUT, city)

    def enter_state(self, state):
        self.send_keys(self.STATE_INPUT, state)

    def enter_zip_code(self, zip_code):
        self.send_keys(self.ZIP_CODE_INPUT, zip_code)

    def enter_phone(self, phone):
        self.send_keys(self.PHONE_INPUT, phone)

    def enter_ssn(self, ssn):
        self.send_keys(self.SSN_INPUT, ssn)

    def enter_username(self, username):
        self.send_keys(self.USERNAME_INPUT, username)

    def enter_password(self, password):
        self.send_keys(self.PASSWORD_INPUT, password)

    def enter_confirm_password(self, confirm_password):
        self.send_keys(self.CONFIRM_PASSWORD_INPUT, confirm_password)

    def click_register(self):
        self.click(self.REGISTER_BUTTON)

    def get_error_text(self):
        """
        Возвращает текст сообщения об ошибке, если оно отображается.
        """
        try:
            error_element = self.wait_for_element(
                self.ERROR_MESSAGE, timeout=5)
            return error_element.text
        except Exception:
            return None

    def is_logout_link_displayed(self):
        """
        Проверяет наличие ссылки "Log Out", которая появляется после успешной регистрации.
        """
        try:
            self.wait_for_element(self.LOGOUT_LINK, timeout=15)
            return True
        except Exception:
            return False


class RegistrationPage(RegistrationPageElementary):
    """
    Page Object для страницы регистрации.
    Наследует базовые методы взаимодействия с элементами из RegistrationPageElementary
    и предоставляет высокоуровневые операции над страницей.
    """

    def fill_registration_form(self, first_name, last_name, address, city, state, zip_code,
                               phone, ssn, username, password, confirm_password):
        """
        Заполняет все поля формы регистрации.
        """
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_address(address)
        self.enter_city(city)
        self.enter_state(state)
        self.enter_zip_code(zip_code)
        self.enter_phone(phone)
        self.enter_ssn(ssn)
        self.enter_username(username)
        self.enter_password(password)
        self.enter_confirm_password(confirm_password)

    def submit_registration(self):
        """
        Нажимает кнопку регистрации.
        """
        self.click_register()


class RegistrationService:
    """
    Сервисный объект для работы с процессом регистрации.
    Инкапсулирует бизнес-логику, используя Page Object RegistrationPage.
    """

    # Добавляем локаторы для доступа через RegistrationService
    FIRST_NAME_INPUT = RegistrationPageElementary.FIRST_NAME_INPUT
    LAST_NAME_INPUT = RegistrationPageElementary.LAST_NAME_INPUT
    ADDRESS_INPUT = RegistrationPageElementary.ADDRESS_INPUT
    CITY_INPUT = RegistrationPageElementary.CITY_INPUT
    STATE_INPUT = RegistrationPageElementary.STATE_INPUT
    ZIP_CODE_INPUT = RegistrationPageElementary.ZIP_CODE_INPUT
    PHONE_INPUT = RegistrationPageElementary.PHONE_INPUT
    SSN_INPUT = RegistrationPageElementary.SSN_INPUT
    USERNAME_INPUT = RegistrationPageElementary.USERNAME_INPUT
    PASSWORD_INPUT = RegistrationPageElementary.PASSWORD_INPUT
    CONFIRM_PASSWORD_INPUT = RegistrationPageElementary.CONFIRM_PASSWORD_INPUT
    REGISTER_BUTTON = RegistrationPageElementary.REGISTER_BUTTON

    def __init__(self, driver):
        self.page = RegistrationPage(driver)

    def register(self, first_name, last_name, address, city, state, zip_code,
                 phone, ssn, username, password, confirm_password):
        """
        Выполняет полный процесс регистрации:
        заполняет форму и отправляет её.
        """
        self.page.fill_registration_form(first_name, last_name, address, city, state, zip_code,
                                         phone, ssn, username, password, confirm_password)
        self.page.submit_registration()

    def is_registration_successful(self):
        """
        Проверяет, что регистрация прошла успешно (появление ссылки "Log Out").
        """
        return self.page.is_logout_link_displayed()

    def get_error_message(self):
        """
        Возвращает сообщение об ошибке, возникающее при неуспешной регистрации.
        """
        return self.page.get_error_text()
