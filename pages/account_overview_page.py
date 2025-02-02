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

    def is_account_overview_displayed(self):
        """
        Ожидает появления заголовка раздела "Accounts Overview" и возвращает True, если он найден.
        """
        try:
            self.wait_for_element(self.ACCOUNT_OVERVIEW_HEADER, timeout=15)
            return True
        except Exception as e:
            print("Account overview header not found:", e)
            return False

    def get_account_balance(self, account_id):
        """
        Находит строку в таблице по номеру аккаунта и возвращает текст первой соседней ячейки (баланс).
        Пример XPath: //table[@id='accountTable']//a[text()='13344']/parent::td/following-sibling::td[1]
        """
        row_locator = (
            By.XPATH,
            f"//table[@id='accountTable']//a[text()='{account_id}']/parent::td/following-sibling::td[1]"
        )
        return self.find_element(row_locator).text

    def view_transaction_history(self, account_id):
        """
        Кликает по ссылке с номером аккаунта для перехода на страницу истории транзакций.
        После клика ожидает появления заголовка "Account Activity".
        """
        link_locator = (
            By.XPATH, f"//table[@id='accountTable']//a[text()='{account_id}']")
        self.click(link_locator)
        self.wait_for_element(self.TRANSACTION_HISTORY_HEADER, timeout=15)

    def is_account_displayed(self, account_id):
        """
        Проверяет, отображается ли номер аккаунта на странице обзора аккаунтов.
        Возвращает True, если элемент с указанным номером найден, иначе False.
        """
        locator = (
            By.XPATH, f"//table[@id='accountTable']//a[text()='{account_id}']")
        try:
            self.wait_for_element(locator, timeout=10)
            return True
        except Exception:
            return False
