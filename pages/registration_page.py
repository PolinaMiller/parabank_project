from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class RegistrationPage(BasePage):
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
    SUCCESS_MESSAGE = (By.XPATH, "//h1[contains(text(),'Welcome')]")

    def register(self, first_name, last_name, address, city, state, zip_code, phone, ssn, username, password, confirm_password):
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
        try:
            self.wait_for_element(self.SUCCESS_MESSAGE, timeout=15)
            return True
        except Exception:
            return False

    def is_error_displayed(self):
        try:
            self.wait_for_element(self.ERROR_MESSAGE, timeout=5)
            return True
        except Exception:
            return False
