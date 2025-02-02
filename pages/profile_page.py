from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class ProfilePage(BasePage):
    EDIT_PROFILE_BUTTON = (By.LINK_TEXT, "Update Contact Info")
    PHONE_INPUT = (By.XPATH, "//input[@id='customer.phoneNumber']")
    SAVE_BUTTON = (
        By.XPATH, "//div[@id='updateProfileForm']//input[@value='Update Profile']")
    SUCCESS_MESSAGE = (
        By.XPATH, "//div[@id='updateProfileResult']//h1[contains(text(),'Profile Updated')]")

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
