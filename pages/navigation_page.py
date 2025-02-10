from pages.navigation_page import NavigationPage
from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class NavigationPageElementary(BasePage):
    """
    Элементарный объект для работы с навигационным меню.
    Содержит локаторы и базовые методы для взаимодействия с элементами меню.
    """
    # Статичные локаторы для конкретных ссылок навигации
    OPEN_NEW_ACCOUNT_LINK = (
        By.XPATH, "//div[@id='leftPanel']//a[text()='Open New Account']")
    ACCOUNTS_OVERVIEW_LINK = (
        By.XPATH, "//div[@id='leftPanel']//a[text()='Accounts Overview']")
    TRANSFER_FUNDS_LINK = (
        By.XPATH, "//div[@id='leftPanel']//a[text()='Transfer Funds']")
    BILL_PAY_LINK = (By.XPATH, "//div[@id='leftPanel']//a[text()='Bill Pay']")
    FIND_TRANSACTIONS_LINK = (
        By.XPATH, "//div[@id='leftPanel']//a[text()='Find Transactions']")
    UPDATE_CONTACT_INFO_LINK = (
        By.XPATH, "//div[@id='leftPanel']//a[text()='Update Contact Info']")
    REQUEST_LOAN_LINK = (
        By.XPATH, "//div[@id='leftPanel']//a[text()='Request Loan']")
    LOG_OUT_LINK = (By.XPATH, "//div[@id='leftPanel']//a[@href='logout.htm']")

    def click_link(self, locator: tuple) -> None:
        """
        Нажимает на элемент, определяемый заданным локатором.
        """
        self.click(locator)

    def click_dynamic_link(self, link_text: str) -> None:
        """
        Нажимает на ссылку навигационного меню, определяемую динамическим локатором по тексту ссылки.
        """
        dynamic_locator = (
            By.XPATH, f"//div[@id='leftPanel']//a[text()='{link_text}']")
        self.click(dynamic_locator)


class NavigationPage(NavigationPageElementary):
    """
    Page Object для навигационного меню.
    Наследует элементарные операции и объединяет их в высокоуровневые действия.
    """

    def navigate_to(self, link_text: str) -> None:
        """
        Переходит по ссылке навигационного меню с заданным текстом.

        :param link_text: Текст ссылки (например, "Accounts Overview", "Transfer Funds" и т.д.)
        """
        self.click_dynamic_link(link_text)

    def open_new_account(self) -> None:
        """Переходит на страницу открытия нового счета."""
        self.click_link(self.OPEN_NEW_ACCOUNT_LINK)

    def accounts_overview(self) -> None:
        """Переходит на страницу обзора счетов."""
        self.click_link(self.ACCOUNTS_OVERVIEW_LINK)

    def transfer_funds(self) -> None:
        """Переходит на страницу перевода средств."""
        self.click_link(self.TRANSFER_FUNDS_LINK)

    def bill_pay(self) -> None:
        """Переходит на страницу оплаты счетов."""
        self.click_link(self.BILL_PAY_LINK)

    def find_transactions(self) -> None:
        """Переходит на страницу поиска транзакций."""
        self.click_link(self.FIND_TRANSACTIONS_LINK)

    def update_contact_info(self) -> None:
        """Переходит на страницу обновления контактной информации."""
        self.click_link(self.UPDATE_CONTACT_INFO_LINK)

    def request_loan(self) -> None:
        """Переходит на страницу запроса кредита."""
        self.click_link(self.REQUEST_LOAN_LINK)

    def log_out(self) -> None:
        """Выполняет выход из учетной записи."""
        self.click_link(self.LOG_OUT_LINK)


class NavigationService:
    """
    Сервисный объект для работы с навигационным меню.
    Инкапсулирует бизнес-логику перехода между страницами, используя Page Object NavigationPage.
    """

    def __init__(self, driver):
        self.navigation_page = NavigationPage(driver)

    def navigate_to(self, link_text: str) -> None:
        """
        Переходит на страницу, используя динамический локатор с заданным текстом ссылки.

        :param link_text: Текст ссылки навигационного меню.
        """
        self.navigation_page.navigate_to(link_text)

    def open_new_account(self) -> None:
        self.navigation_page.open_new_account()

    def go_to_accounts_overview(self) -> None:
        self.navigation_page.accounts_overview()

    def transfer_funds(self) -> None:
        self.navigation_page.transfer_funds()

    def bill_pay(self) -> None:
        self.navigation_page.bill_pay()

    def find_transactions(self) -> None:
        self.navigation_page.find_transactions()

    def update_contact_info(self) -> None:
        self.navigation_page.update_contact_info()

    def request_loan(self) -> None:
        self.navigation_page.request_loan()

    def log_out(self) -> None:
        self.navigation_page.log_out()
