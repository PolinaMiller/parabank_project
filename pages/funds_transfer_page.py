from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


class FundsTransferPage(BasePage):
    AMOUNT_INPUT = (By.ID, "amount")
    FROM_ACCOUNT_SELECT = (By.ID, "fromAccountId")
    TO_ACCOUNT_SELECT = (By.ID, "toAccountId")
    TRANSFER_BUTTON = (By.XPATH, "//input[@value='Transfer']")
    SUCCESS_MESSAGE = (
        By.XPATH, "//div[@id='showResult']//h1[contains(text(),'Transfer Complete')]")
    ERROR_MESSAGE = (
        By.XPATH, "//div[@id='showError']//h1[contains(text(), 'Error!')]")

    def transfer_funds(self, amount, from_account, to_account):
        self.clear_and_send_keys(self.AMOUNT_INPUT, amount)

        from_select = Select(self.find_element(self.FROM_ACCOUNT_SELECT))
        from_select.select_by_value(from_account)
        to_select = Select(self.find_element(self.TO_ACCOUNT_SELECT))
        to_select.select_by_value(to_account)

        self.click(self.TRANSFER_BUTTON)

    def is_transfer_successful(self):
        try:
            self.wait_for_element(self.SUCCESS_MESSAGE, timeout=15)
            return True
        except Exception:
            return False

    def is_transfer_error_displayed(self):
        try:
            self.wait_for_element(self.ERROR_MESSAGE, timeout=5)
            return True
        except Exception:
            return False

    def clear_and_send_keys(self, locator, keys):
        """
        Очищает поле, найденное по локатору, и отправляет в него указанные ключи.
        """
        element = self.find_element(locator)
        element.clear()
        element.send_keys(keys)
