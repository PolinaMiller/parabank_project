from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class AccountOverviewPageElementary(BasePage):
    """
    Элементарный объект страницы обзора счетов.

    Содержит локаторы и базовые методы для непосредственного взаимодействия с элементами страницы.
    """
    ACCOUNT_OVERVIEW_HEADER = (
        By.XPATH, "//div[@id='showOverview']//h1[contains(text(), 'Accounts Overview')]"
    )
    ACCOUNT_TABLE = (By.XPATH, "//table[@id='accountTable']")
    TRANSACTION_HISTORY_HEADER = (
        By.XPATH, "//h1[contains(text(),'Account Activity')]"
    )

    def is_element_visible(self, locator: tuple, timeout: int = 15) -> bool:
        """
        Проверяет, появляется ли элемент на странице в течение заданного времени.

        :param locator: Локатор элемента, например, (By.XPATH, "...")
        :param timeout: Максимальное время ожидания в секундах.
        :return: True, если элемент найден, иначе False.
        """
        try:
            self.wait_for_element(locator, timeout=timeout)
            return True
        except Exception as e:
            print(f"Element {locator} not visible: {e}")
            return False

    def wait_for_account_overview_header(self, timeout: int = 15):
        """
        Ожидает появления заголовка "Accounts Overview".

        :param timeout: Максимальное время ожидания.
        :return: Найденный элемент заголовка.
        """
        return self.wait_for_element(self.ACCOUNT_OVERVIEW_HEADER, timeout=timeout)

    def get_row_balance_element(self, account_id: str, timeout: int = 15):
        """
        Находит ячейку с балансом по заданному номеру аккаунта.

        Пример XPath:
          //table[@id='accountTable']//a[text()='13344']/parent::td/following-sibling::td[1]

        :param account_id: Номер аккаунта.
        :param timeout: Время ожидания появления элемента.
        :return: Веб-элемент с балансом.
        """
        row_locator = (
            By.XPATH,
            f"//table[@id='accountTable']//a[text()='{account_id}']/parent::td/following-sibling::td[1]"
        )
        return self.wait_for_element(row_locator, timeout=timeout)

    def click_account_link(self, account_id: str) -> None:
        """
        Кликает по ссылке с номером аккаунта.

        :param account_id: Номер аккаунта.
        """
        link_locator = (
            By.XPATH,
            f"//table[@id='accountTable']//a[text()='{account_id}']"
        )
        self.click(link_locator)

    def wait_for_transaction_history_header(self, timeout: int = 15):
        """
        Ожидает появления заголовка "Account Activity" (история транзакций).

        :param timeout: Максимальное время ожидания.
        :return: Найденный элемент заголовка.
        """
        return self.wait_for_element(self.TRANSACTION_HISTORY_HEADER, timeout=timeout)

    def is_account_link_visible(self, account_id: str, timeout: int = 10) -> bool:
        """
        Проверяет, отображается ли ссылка с номером аккаунта.

        :param account_id: Номер аккаунта.
        :param timeout: Максимальное время ожидания.
        :return: True, если элемент найден, иначе False.
        """
        locator = (
            By.XPATH,
            f"//table[@id='accountTable']//a[text()='{account_id}']"
        )
        return self.is_element_visible(locator, timeout=timeout)


class AccountOverviewPage(AccountOverviewPageElementary):
    """
    Page Object для страницы обзора счетов.

    Наследует элементарные методы из AccountOverviewPageElementary и предоставляет
    высокоуровневые операции для работы со страницей.
    """

    def is_account_overview_displayed(self) -> bool:
        """
        Проверяет, отображается ли раздел "Accounts Overview".

        :return: True, если заголовок найден, иначе False.
        """
        return self.is_element_visible(self.ACCOUNT_OVERVIEW_HEADER, timeout=15)

    def get_account_balance(self, account_id: str) -> str:
        """
        Возвращает баланс по заданному номеру аккаунта.

        :param account_id: Номер аккаунта.
        :return: Текст ячейки, содержащий баланс.
        """
        balance_element = self.get_row_balance_element(account_id, timeout=15)
        return balance_element.text

    def view_transaction_history(self, account_id: str) -> None:
        """
        Переходит по ссылке с номером аккаунта для просмотра истории транзакций и
        ожидает появления заголовка "Account Activity".

        :param account_id: Номер аккаунта.
        """
        self.click_account_link(account_id)
        self.wait_for_transaction_history_header(timeout=15)

    def is_account_displayed(self, account_id: str) -> bool:
        """
        Проверяет, отображается ли ссылка с заданным номером аккаунта.

        :param account_id: Номер аккаунта.
        :return: True, если элемент найден, иначе False.
        """
        return self.is_account_link_visible(account_id, timeout=10)


class AccountOverviewService:
    """
    Сервисный объект для работы со страницей обзора счетов.

    Инкапсулирует бизнес-логику, используя Page Object AccountOverviewPage.
    """

    def __init__(self, driver):
        self.page = AccountOverviewPage(driver)

    def check_account_overview_display(self) -> bool:
        """
        Проверяет, что раздел "Accounts Overview" отображается на странице.

        :return: True, если раздел отображается, иначе False.
        """
        return self.page.is_account_overview_displayed()

    def fetch_account_balance(self, account_id: str) -> str:
        """
        Получает баланс по заданному номеру аккаунта.

        :param account_id: Номер аккаунта.
        :return: Баланс аккаунта в виде строки.
        """
        return self.page.get_account_balance(account_id)

    def open_account_transaction_history(self, account_id: str) -> None:
        """
        Переходит к просмотру истории транзакций по заданному аккаунту.

        :param account_id: Номер аккаунта.
        """
        self.page.view_transaction_history(account_id)

    def verify_account_presence(self, account_id: str) -> bool:
        """
        Проверяет, отображается ли указанный аккаунт на странице.

        :param account_id: Номер аккаунта.
        :return: True, если аккаунт найден, иначе False.
        """
        return self.page.is_account_displayed(account_id)
