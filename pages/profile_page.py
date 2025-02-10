from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class ProfilePage(BasePage):
    """
    Класс ProfilePage реализует взаимодействие со страницей профиля пользователя.
    Он предоставляет методы для обновления номера телефона и проверки результатов операции.
    """

    # Локатор для кнопки редактирования профиля (ссылка "Update Contact Info")
    EDIT_PROFILE_BUTTON = (By.LINK_TEXT, "Update Contact Info")
    # Локатор для поля ввода номера телефона
    PHONE_INPUT = (By.XPATH, "//input[@id='customer.phoneNumber']")
    # Локатор для кнопки сохранения изменений в форме обновления профиля
    SAVE_BUTTON = (
        By.XPATH, "//div[@id='updateProfileForm']//input[@value='Update Profile']")
    # Локатор для сообщения об успешном обновлении профиля (ожидается текст 'Profile Updated')
    SUCCESS_MESSAGE = (
        By.XPATH, "//div[@id='updateProfileResult']//h1[contains(text(),'Profile Updated')]")
    # Локатор для сообщения об ошибке в форме обновления профиля (отображается только если элемент видим)
    ERROR_MESSAGE = (
        By.XPATH, "//div[@id='updateProfileForm']//span[contains(@class, 'error') and not(contains(@style, 'display:none'))]")

    def update_phone_number(self, new_phone: str) -> None:
        """
        Обновляет номер телефона пользователя.

        Шаги:
          1. Нажимает на ссылку "Update Contact Info" для перехода к форме редактирования.
          2. Ожидает появления формы обновления профиля (идентифицируется по ID формы).
          3. Очищает поле ввода номера телефона и вводит новое значение.
          4. Нажимает кнопку "Update Profile" для сохранения изменений.

        :param new_phone: Новый номер телефона, который требуется установить.
        """
        self.click(self.EDIT_PROFILE_BUTTON)
        self.wait_for_element((By.ID, "updateProfileForm"), timeout=10)
        self.send_keys(self.PHONE_INPUT, new_phone)
        self.click(self.SAVE_BUTTON)

    def _is_element_visible(self, locator: tuple, timeout: int = 15) -> bool:
        """
        Вспомогательный метод для проверки, что элемент, заданный локатором, появляется на странице.

        :param locator: Локатор элемента (например, (By.XPATH, "...")).
        :param timeout: Максимальное время ожидания в секундах (по умолчанию 15 секунд).
        :return: True, если элемент появляется в течение указанного времени; иначе, False.
        """
        try:
            self.wait_for_element(locator, timeout=timeout)
            return True
        except Exception:
            return False

    def is_update_successful(self) -> bool:
        """
        Проверяет, что сообщение об успешном обновлении профиля отображается на странице.

        :return: True, если сообщение об успехе найдено в течение 30 секунд; иначе, False.
        """
        return self._is_element_visible(self.SUCCESS_MESSAGE, timeout=30)

    def is_error_displayed(self) -> bool:
        """
        Проверяет, что сообщение об ошибке при обновлении профиля отображается на странице.

        :return: True, если сообщение об ошибке найдено в течение 30 секунд; иначе, False.
        """
        return self._is_element_visible(self.ERROR_MESSAGE, timeout=30)
