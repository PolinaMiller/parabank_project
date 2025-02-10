from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class AccountOverviewPage(BasePage):
    ACCOUNT_OVERVIEW_HEADER = (
        By.XPATH, "//div[@id='showOverview']//h1[contains(text(), 'Accounts Overview')]")
    ACCOUNT_TABLE = (By.XPATH, "//table[@id='accountTable']")
    TRANSACTION_HISTORY_HEADER = (
        By.XPATH, "//h1[contains(text(),'Account Activity')]")
    ACCOUNT_NUMBER_13344 = (
        By.XPATH, "//table[@id='accountTable']//a[@href='activity.htm?id=13344']")

    def _is_visible(self, locator, timeout=15):
        """
        Вспомогательный метод для проверки видимости элемента на странице.

        :param locator: Локатор элемента в виде кортежа (например, (By.XPATH, "...")).
        :param timeout: Максимальное время ожидания (по умолчанию 15 секунд).
        :return: True, если элемент появляется на странице в течение timeout секунд; иначе, False.
        """
        try:
            self.wait_for_element(locator, timeout=timeout)
            return True
        except Exception as e:
            print(f"Element {locator} not visible: {e}")
            return False

    def wait_for_account_overview_header(self, timeout=15):
        """
        Ожидает появления заголовка раздела "Accounts Overview" на странице.

        :param timeout: Максимальное время ожидания (по умолчанию 15 секунд).
        :return: Найденный элемент заголовка.
        """
        return self.wait_for_element(self.ACCOUNT_OVERVIEW_HEADER, timeout=timeout)

    def is_account_overview_displayed(self):
        """
        Проверяет, отображается ли раздел "Accounts Overview" на странице.

        :return: True, если заголовок найден, иначе False.
        """
        return self._is_visible(self.ACCOUNT_OVERVIEW_HEADER, timeout=15)

    def get_account_balance(self, account_id):
        """
        Находит строку в таблице по номеру аккаунта и возвращает текст первой соседней ячейки (баланс).

        Пример XPath: 
          //table[@id='accountTable']//a[text()='13344']/parent::td/following-sibling::td[1]

        :param account_id: Номер аккаунта, для которого требуется получить баланс.
        :return: Текст, содержащий баланс аккаунта.
        """
        row_locator = (
            By.XPATH,
            f"//table[@id='accountTable']//a[text()='{account_id}']/parent::td/following-sibling::td[1]"
        )
        # Ожидаем, что элемент будет виден, и возвращаем его текст
        return self.wait_for_element(row_locator, timeout=15).text

    def view_transaction_history(self, account_id):
        """
        Переходит по ссылке с номером аккаунта для просмотра истории транзакций,
        после чего ожидает появления заголовка "Account Activity".

        :param account_id: Номер аккаунта, для которого требуется просмотреть историю транзакций.
        """
        link_locator = (
            By.XPATH, f"//table[@id='accountTable']//a[text()='{account_id}']")
        self.click(link_locator)
        self.wait_for_element(self.TRANSACTION_HISTORY_HEADER, timeout=15)

    def is_account_displayed(self, account_id):
        """
        Проверяет, отображается ли указанный номер аккаунта на странице обзора аккаунтов.

        :param account_id: Номер аккаунта для проверки.
        :return: True, если элемент найден в течение 10 секунд; иначе, False.
        """
        locator = (
            By.XPATH, f"//table[@id='accountTable']//a[text()='{account_id}']")
        return self._is_visible(locator, timeout=10)
