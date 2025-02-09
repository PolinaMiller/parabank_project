from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class ProfilePage(BasePage):
    EDIT_PROFILE_BUTTON = (By.LINK_TEXT, "Update Contact Info")

    PHONE_INPUT = (By.XPATH, "//input[@id='customer.phoneNumber']")

    SAVE_BUTTON = (
        By.XPATH, "//div[@id='updateProfileForm']//input[@value='Update Profile']")

    SUCCESS_MESSAGE = (
        By.XPATH, "//div[@id='updateProfileResult']//h1[contains(text(),'Profile Updated')]")

    ERROR_MESSAGE = (
        By.XPATH, "//div[@id='updateProfileForm']//span[contains(@class, 'error') and not(contains(@style, 'display:none'))]")

    def update_phone_number(self, new_phone):
        """
        Нажимает на ссылку "Update Contact Info", ожидает появления формы обновления профиля,
        очищает поле номера телефона, вводит новое значение и нажимает кнопку "Update Profile".
        """
        self.click(self.EDIT_PROFILE_BUTTON)
        self.wait_for_element((By.ID, "updateProfileForm"), timeout=10)
        phone_field = self.find_element(self.PHONE_INPUT)
        phone_field.clear()
        phone_field.send_keys(new_phone)
        self.click(self.SAVE_BUTTON)

    def is_update_successful(self):
        try:
            self.wait_for_element(self.SUCCESS_MESSAGE, timeout=30)
            return True
        except Exception:
            return False

    def is_error_displayed(self):
        try:
            self.wait_for_element(self.ERROR_MESSAGE, timeout=30)
            return True
        except Exception:
            return False
