from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


class FundsTransferPage(BasePage):
    """
    Класс FundsTransferPage предоставляет методы для выполнения перевода средств
    между счетами, а также для проверки успешности или наличия ошибок при выполнении операции.
    """

    # Локатор для поля ввода суммы перевода
    AMOUNT_INPUT = (By.ID, "amount")
    # Локатор для выпадающего списка исходного счета
    FROM_ACCOUNT_SELECT = (By.ID, "fromAccountId")
    # Локатор для выпадающего списка счета получателя
    TO_ACCOUNT_SELECT = (By.ID, "toAccountId")
    # Локатор для кнопки, запускающей перевод средств
    TRANSFER_BUTTON = (By.XPATH, "//input[@value='Transfer']")
    # Локатор для сообщения об успешном завершении перевода
    SUCCESS_MESSAGE = (
        By.XPATH, "//div[@id='showResult']//h1[contains(text(),'Transfer Complete')]")
    # Локатор для сообщения об ошибке, возникающей при переводе средств
    ERROR_MESSAGE = (
        By.XPATH, "//div[@id='showError']//h1[contains(text(), 'Error!')]")

    def transfer_funds(self, amount: str, from_account: str, to_account: str) -> None:
        """
        Выполняет перевод средств с одного счета на другой.

        Шаги:
          1. Очищает поле ввода суммы и вводит переданное значение.
          2. Выбирает исходный счет и счет получателя из соответствующих выпадающих списков.
          3. Инициирует перевод, кликая по кнопке "Transfer".

        :param amount: Сумма перевода в виде строки.
        :param from_account: Значение для выбора исходного счета.
        :param to_account: Значение для выбора счета получателя.
        """
        self.clear_and_send_keys(self.AMOUNT_INPUT, amount)

        # Выбираем исходный счет из выпадающего списка
        from_select = Select(self.find_element(self.FROM_ACCOUNT_SELECT))
        from_select.select_by_value(from_account)

        # Выбираем счет получателя из выпадающего списка
        to_select = Select(self.find_element(self.TO_ACCOUNT_SELECT))
        to_select.select_by_value(to_account)

        # Кликаем по кнопке перевода для отправки формы
        self.click(self.TRANSFER_BUTTON)

    def _is_element_visible(self, locator: tuple, timeout: int) -> bool:
        """
        Вспомогательный метод для проверки, что элемент, заданный локатором, появляется на странице.

        :param locator: Локатор элемента в виде кортежа (например, (By.XPATH, "...")).
        :param timeout: Максимальное время ожидания в секундах.
        :return: True, если элемент появляется в течение указанного времени, иначе False.
        """
        try:
            self.wait_for_element(locator, timeout=timeout)
            return True
        except Exception:
            return False

    def is_transfer_successful(self) -> bool:
        """
        Проверяет, что перевод средств выполнен успешно, ожидая появления сообщения об успехе.

        :return: True, если сообщение об успешном переводе найдено в течение 15 секунд, иначе False.
        """
        return self._is_element_visible(self.SUCCESS_MESSAGE, timeout=15)

    def is_transfer_error_displayed(self) -> bool:
        """
        Проверяет, отображается ли сообщение об ошибке при выполнении перевода средств.

        :return: True, если сообщение об ошибке найдено в течение 5 секунд, иначе False.
        """
        return self._is_element_visible(self.ERROR_MESSAGE, timeout=5)

    def clear_and_send_keys(self, locator: tuple, keys: str) -> None:
        """
        Очищает поле, найденное по заданному локатору, и отправляет в него указанные данные.

        :param locator: Кортеж, содержащий стратегию поиска и значение (например, (By.ID, "elementId")).
        :param keys: Строка, которую нужно ввести в найденное поле.
        """
        element = self.find_element(locator)
        element.clear()
        element.send_keys(keys)
