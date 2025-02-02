from pages.navigation_page import NavigationPage
from pages.login_page import LoginPage

def test_navigation_links(driver, base_url):
    driver.get(base_url)
    login_page = LoginPage(driver)
    login_page.login("john", "demo")
    navigation = NavigationPage(driver)
    
    assert "Welcome" in driver.page_source, "Приветственное сообщение не отображается."

    navigation.navigate_to("Open New Account")
    assert "Open New Account" in driver.page_source, "Страница 'Open New Account' не отображается."

    navigation.navigate_to("Accounts Overview")
    assert "Accounts Overview" in driver.page_source, "Страница 'Accounts Overview' не отображается."

    navigation.navigate_to("Transfer Funds")
    assert "Transfer Funds" in driver.page_source, "Страница 'Transfer Funds' не отображается."

    navigation.navigate_to("Bill Pay")
    assert "Bill Pay" in driver.page_source, "Страница 'Bill Pay' не отображается."

    navigation.navigate_to("Find Transactions")
    assert "Find Transactions" in driver.page_source, "Страница 'Find Transactions' не отображается."

    navigation.navigate_to("Update Contact Info")
    assert "Update Contact Info" in driver.page_source, "Страница 'Update Contact Info' не отображается."

    navigation.navigate_to("Request Loan")
    assert "Request Loan" in driver.page_source, "Страница 'Request Loan' не отображается."

    navigation.navigate_to("Log Out")
    assert "Customer Login" in driver.page_source, "После выхода не отображается страница 'Customer Login'."
