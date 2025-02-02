from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class NavigationPage(BasePage):
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
        link_locator = (
            By.XPATH, f"//div[@id='leftPanel']//a[text()='{link_text}']")
        self.click(link_locator)
