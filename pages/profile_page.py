from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class ProfilePageElementary(BasePage):
    """
    Элементарный объект страницы профиля.
    Содержит локаторы и базовые методы для непосредственного взаимодействия с элементами страницы.
    """
    # Локаторы элементов страницы профиля
    EDIT_PROFILE_BUTTON = (By.LINK_TEXT, "Update Contact Info")
    PHONE_INPUT = (By.XPATH, "//input[@id='customer.phoneNumber']")
    SAVE_BUTTON = (
        By.XPATH, "//div[@id='updateProfileForm']//input[@value='Update Profile']")
    SUCCESS_MESSAGE = (
        By.XPATH, "//div[@id='updateProfileResult']//h1[contains(text(),'Profile Updated')]")
    ERROR_MESSAGE = (
        By.XPATH,
        "//div[@id='updateProfileForm']//span[contains(@class, 'error') and not(contains(@style, 'display:none'))]"
    )

    def click_edit_profile(self) -> None:
        """
        Нажимает на кнопку редактирования профиля ("Update Contact Info").
        """
        self.click(self.EDIT_PROFILE_BUTTON)

    def wait_for_update_form(self, timeout: int = 10) -> None:
        """
        Ожидает появления формы обновления профиля по ID.
        """
        self.wait_for_element((By.ID, "updateProfileForm"), timeout=timeout)

    def clear_and_enter_phone(self, new_phone: str) -> None:
        """
        Очищает поле ввода номера телефона и вводит новое значение.
        """
        # Предполагается, что метод clear() реализован в BasePage.
        self.clear(self.PHONE_INPUT)
        self.send_keys(self.PHONE_INPUT, new_phone)

    def click_save(self) -> None:
        """
        Нажимает на кнопку сохранения изменений в профиле.
        """
        self.click(self.SAVE_BUTTON)

    def wait_for_success_message(self, timeout: int = 30):
        """
        Ожидает появления сообщения об успешном обновлении профиля.
        Возвращает элемент, если он найден, или генерирует исключение.
        """
        return self.wait_for_element(self.SUCCESS_MESSAGE, timeout=timeout)

    def wait_for_error_message(self, timeout: int = 30):
        """
        Ожидает появления сообщения об ошибке при обновлении профиля.
        Возвращает элемент, если он найден, или генерирует исключение.
        """
        return self.wait_for_element(self.ERROR_MESSAGE, timeout=timeout)

    def is_element_visible(self, locator: tuple, timeout: int = 15) -> bool:
        """
        Проверяет, появляется ли указанный элемент на странице в течение заданного времени.

        :param locator: Локатор элемента (например, (By.XPATH, "...")).
        :param timeout: Максимальное время ожидания в секундах.
        :return: True, если элемент найден; иначе, False.
        """
        try:
            self.wait_for_element(locator, timeout=timeout)
            return True
        except Exception:
            return False


class ProfilePage(ProfilePageElementary):
    """
    Page Object для страницы профиля пользователя.
    Наследует базовые методы из ProfilePageElementary и объединяет их в высокоуровневые операции.
    """

    def update_phone_number(self, new_phone: str) -> None:
        """
        Выполняет обновление номера телефона пользователя.

        Шаги:
          1. Нажимает кнопку редактирования профиля.
          2. Ожидает появления формы обновления профиля.
          3. Очищает поле ввода номера телефона и вводит новое значение.
          4. Нажимает кнопку сохранения изменений.

        :param new_phone: Новый номер телефона для установки.
        """
        self.click_edit_profile()
        self.wait_for_update_form()
        self.clear_and_enter_phone(new_phone)
        self.click_save()

    def is_update_successful(self) -> bool:
        """
        Проверяет, что сообщение об успешном обновлении профиля отображается на странице.

        :return: True, если сообщение об успехе найдено; иначе, False.
        """
        return self.is_element_visible(self.SUCCESS_MESSAGE, timeout=30)

    def is_error_displayed(self) -> bool:
        """
        Проверяет, что сообщение об ошибке при обновлении профиля отображается на странице.

        :return: True, если сообщение об ошибке найдено; иначе, False.
        """
        return self.is_element_visible(self.ERROR_MESSAGE, timeout=30)


class ProfileService:
    """
    Сервисный объект для работы с обновлением профиля пользователя.
    Инкапсулирует бизнес-логику, используя Page Object ProfilePage.
    """

    def __init__(self, driver):
        self.page = ProfilePage(driver)

    def update_phone_number(self, new_phone: str) -> None:
        """
        Выполняет обновление номера телефона через Page Object.

        :param new_phone: Новый номер телефона для обновления.
        """
        self.page.update_phone_number(new_phone)

    def is_update_successful(self) -> bool:
        """
        Проверяет, что обновление профиля прошло успешно.

        :return: True, если обновление успешно; иначе, False.
        """
        return self.page.is_update_successful()

    def is_error_displayed(self) -> bool:
        """
        Проверяет, что при обновлении профиля появилось сообщение об ошибке.

        :return: True, если сообщение об ошибке отображается; иначе, False.
        """
        return self.page.is_error_displayed()
