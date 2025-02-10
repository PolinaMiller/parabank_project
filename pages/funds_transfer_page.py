from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


class FundsTransferPageElementary(BasePage):
    """
    Элементарный объект страницы перевода средств.
    Содержит локаторы и базовые методы для непосредственного взаимодействия с элементами страницы.
    """
    # Локаторы элементов страницы перевода средств
    AMOUNT_INPUT = (By.ID, "amount")
    FROM_ACCOUNT_SELECT = (By.ID, "fromAccountId")
    TO_ACCOUNT_SELECT = (By.ID, "toAccountId")
    TRANSFER_BUTTON = (By.XPATH, "//input[@value='Transfer']")
    SUCCESS_MESSAGE = (
        By.XPATH, "//div[@id='showResult']//h1[contains(text(),'Transfer Complete')]")
    ERROR_MESSAGE = (
        By.XPATH, "//div[@id='showError']//h1[contains(text(), 'Error!')]")

    def clear_and_send_keys(self, locator: tuple, keys: str) -> None:
        """
        Очищает поле, найденное по заданному локатору, и отправляет в него указанные данные.

        :param locator: Кортеж (например, (By.ID, "elementId")).
        :param keys: Строка, которую нужно ввести.
        """
        element = self.find_element(locator)
        element.clear()
        element.send_keys(keys)

    def select_from_dropdown_by_value(self, locator: tuple, value: str) -> None:
        """
        Выбирает значение из выпадающего списка по атрибуту value.

        :param locator: Локатор элемента Select.
        :param value: Значение атрибута value для выбора.
        """
        select = Select(self.find_element(locator))
        select.select_by_value(value)

    def click_transfer_button(self) -> None:
        """
        Нажимает на кнопку, запускающую перевод средств.
        """
        self.click(self.TRANSFER_BUTTON)

    def is_element_visible(self, locator: tuple, timeout: int) -> bool:
        """
        Вспомогательный метод для проверки, что элемент появляется на странице в течение заданного времени.

        :param locator: Локатор элемента.
        :param timeout: Время ожидания в секундах.
        :return: True, если элемент найден, иначе False.
        """
        try:
            self.wait_for_element(locator, timeout=timeout)
            return True
        except Exception:
            return False

    def wait_for_success_message(self, timeout: int = 15) -> bool:
        """
        Ожидает появления сообщения об успешном переводе средств.

        :param timeout: Время ожидания в секундах.
        :return: True, если сообщение появилось, иначе False.
        """
        return self.is_element_visible(self.SUCCESS_MESSAGE, timeout)

    def wait_for_error_message(self, timeout: int = 5) -> bool:
        """
        Ожидает появления сообщения об ошибке при переводе средств.

        :param timeout: Время ожидания в секундах.
        :return: True, если сообщение появилось, иначе False.
        """
        return self.is_element_visible(self.ERROR_MESSAGE, timeout)


class FundsTransferPage(FundsTransferPageElementary):
    """
    Page Object для страницы перевода средств.
    Объединяет элементарные операции в высокоуровневые действия для перевода средств.
    """

    def transfer_funds(self, amount: str, from_account: str, to_account: str) -> None:
        """
        Выполняет перевод средств с одного счета на другой.

        Шаги:
          1. Очищает поле ввода суммы и вводит указанное значение.
          2. Выбирает исходный и целевой счета из выпадающих списков.
          3. Инициирует перевод, нажав на кнопку.

        :param amount: Сумма перевода.
        :param from_account: Значение для выбора исходного счета.
        :param to_account: Значение для выбора счета получателя.
        """
        self.clear_and_send_keys(self.AMOUNT_INPUT, amount)
        self.select_from_dropdown_by_value(
            self.FROM_ACCOUNT_SELECT, from_account)
        self.select_from_dropdown_by_value(self.TO_ACCOUNT_SELECT, to_account)
        self.click_transfer_button()

    def is_transfer_successful(self) -> bool:
        """
        Проверяет, что перевод средств выполнен успешно.

        :return: True, если сообщение об успешном переводе отображается, иначе False.
        """
        return self.wait_for_success_message(timeout=15)

    def is_transfer_error_displayed(self) -> bool:
        """
        Проверяет, отображается ли сообщение об ошибке при выполнении перевода средств.

        :return: True, если сообщение об ошибке найдено, иначе False.
        """
        return self.wait_for_error_message(timeout=5)


class FundsTransferService:
    """
    Сервисный объект для работы с переводом средств.
    Инкапсулирует бизнес-логику, используя Page Object FundsTransferPage.
    """

    def __init__(self, driver):
        self.page = FundsTransferPage(driver)

    def transfer_funds(self, amount: str, from_account: str, to_account: str) -> None:
        """
        Выполняет перевод средств, используя Page Object.

        :param amount: Сумма перевода.
        :param from_account: Значение для выбора исходного счета.
        :param to_account: Значение для выбора счета получателя.
        """
        self.page.transfer_funds(amount, from_account, to_account)

    def is_transfer_successful(self) -> bool:
        """
        Проверяет успешность перевода средств.

        :return: True, если перевод выполнен успешно, иначе False.
        """
        return self.page.is_transfer_successful()

    def is_transfer_error_displayed(self) -> bool:
        """
        Проверяет, отображается ли сообщение об ошибке перевода.

        :return: True, если сообщение об ошибке найдено, иначе False.
        """
        return self.page.is_transfer_error_displayed()
