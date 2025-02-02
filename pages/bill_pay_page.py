from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


class BillPayPage(BasePage):
    PAYEE_NAME_INPUT = (By.XPATH, "//input[@name='payee.name']")
    ADDRESS_INPUT = (By.XPATH, "//input[@name='payee.address.street']")
    CITY_INPUT = (By.XPATH, "//input[@name='payee.address.city']")
    STATE_INPUT = (By.XPATH, "//input[@name='payee.address.state']")
    ZIP_CODE_INPUT = (By.XPATH, "//input[@name='payee.address.zipCode']")
    PHONE_INPUT = (By.XPATH, "//input[@name='payee.phoneNumber']")
    ACCOUNT_INPUT = (By.XPATH, "//input[@name='payee.accountNumber']")
    VERIFY_ACCOUNT_INPUT = (By.XPATH, "//input[@name='verifyAccount']")
    AMOUNT_INPUT = (By.XPATH, "//input[@name='amount']")
    FROM_ACCOUNT_SELECT = (By.XPATH, "//select[@name='fromAccountId']")
    SEND_PAYMENT_BUTTON = (
        By.XPATH, "//div[@id='billpayForm']//input[@value='Send Payment']")
    SUCCESS_MESSAGE = (
        By.XPATH, "//h1[contains(text(),'Bill Payment Complete')]")
    ERROR_MESSAGE = (
        By.XPATH, "//span[@id='validationModel-name' and contains(text(),'Payee name is required')]")
    VERIFY_ACCOUNT_MISMATCH_ERROR = (
        By.XPATH, "//span[@id='validationModel-verifyAccount-mismatch' and contains(text(),'The account numbers do not match')]"
    )
    AMOUNT_INVALID_ERROR = (
        By.XPATH, "//span[@id='validationModel-amount-invalid' and contains(text(),'Please enter a valid amount')]")

    def pay_bill(self, payee_name, address, city, state, zip_code, phone, account, verify_account, amount, from_account):
        self.send_keys(self.PAYEE_NAME_INPUT, payee_name)
        self.send_keys(self.ADDRESS_INPUT, address)
        self.send_keys(self.CITY_INPUT, city)
        self.send_keys(self.STATE_INPUT, state)
        self.send_keys(self.ZIP_CODE_INPUT, zip_code)
        self.send_keys(self.PHONE_INPUT, phone)
        self.send_keys(self.ACCOUNT_INPUT, account)
        self.send_keys(self.VERIFY_ACCOUNT_INPUT, verify_account)
        self.send_keys(self.AMOUNT_INPUT, amount)
        select = Select(self.find_element(self.FROM_ACCOUNT_SELECT))
        select.select_by_value(from_account)
        self.click(self.SEND_PAYMENT_BUTTON)

    def is_payment_successful(self):
        try:
            self.wait_for_element(self.SUCCESS_MESSAGE, timeout=15)
            return True
        except Exception:
            return False

    def is_payment_error_displayed(self):
        try:
            self.wait_for_element(self.ERROR_MESSAGE, timeout=15)
            return True
        except Exception:
            return False

    def is_verify_account_mismatch_error_displayed(self):
        try:
            self.wait_for_element(
                self.VERIFY_ACCOUNT_MISMATCH_ERROR, timeout=15)
            return True
        except Exception:
            return False

    def is_amount_invalid_error_displayed(self):
        try:
            self.wait_for_element(self.AMOUNT_INVALID_ERROR, timeout=15)
            return True
        except Exception:
            return False
