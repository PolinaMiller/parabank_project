from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class NavigationPage(BasePage):
    """
    Класс NavigationPage предназначен для работы с навигационным меню приложения.
    Он предоставляет методы для перехода по ссылкам меню с использованием динамических локаторов,
    что упрощает поддержку и тестирование навигации.
    """

    # Дополнительные локаторы для прямого обращения к отдельным ссылкам,
    # если потребуется проверка наличия конкретных элементов.
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

    def navigate_to(self, link_text):
        """
        Переходит по ссылке навигационного меню с заданным текстом.

        Используется динамический локатор, который находит ссылку внутри левой панели
        по точному совпадению текста.

        :param link_text: Текст ссылки, по которой необходимо выполнить переход
                          (например, "Accounts Overview", "Transfer Funds" и т.д.).
        :raises: Исключение, если элемент не найден в течение заданного времени ожидания.
        """
        # Формируем динамический локатор на основе переданного текста ссылки.
        link_locator = (
            By.XPATH, f"//div[@id='leftPanel']//a[text()='{link_text}']")
        self.click(link_locator)
