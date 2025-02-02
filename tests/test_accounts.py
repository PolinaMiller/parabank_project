from pages.account_overview_page import AccountOverviewPage
from pages.login_page import LoginPage


def test_account_overview(driver, base_url):
    driver.get(base_url)
    login_page = LoginPage(driver)
    login_page.login("john", "demo")
    account_overview = AccountOverviewPage(driver)
    assert account_overview.is_account_overview_displayed(
    ), "Account Overview is not displayed."


def test_view_transaction_history(driver, base_url):
    driver.get(base_url)
    login_page = LoginPage(driver)
    login_page.login("john", "demo")
    account_overview = AccountOverviewPage(driver)
    account_overview.view_transaction_history("13344")
    assert "Account Activity" in driver.page_source, "Transaction history is not displayed."
