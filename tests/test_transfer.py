from pages.funds_transfer_page import FundsTransferPage
from pages.login_page import LoginPage


def test_funds_transfer_success(driver, base_url):
    driver.get(base_url)
    login_page = LoginPage(driver)
    login_page.login("john", "demo")
    driver.get(f"{base_url}/transfer.htm")
    transfer_page = FundsTransferPage(driver)
    transfer_page.transfer_funds("100", "13344", "13344")
    assert transfer_page.is_transfer_successful(), "Funds transfer was not successful."


def test_funds_transfer_insufficient_balance(driver, base_url):
    driver.get(base_url)
    login_page = LoginPage(driver)
    login_page.login("john", "demo")
    driver.get(f"{base_url}/transfer.htm")
    transfer_page = FundsTransferPage(driver)
    transfer_page.transfer_funds("1000000", "13344", "13344")
    assert transfer_page.is_transfer_successful(
    ), "Funds transfer was not successful, even though insufficient balance scenario is allowed."
