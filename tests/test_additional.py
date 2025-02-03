import time
from selenium.webdriver.common.by import By
import pytest
from pages.login_page import LoginPage
from pages.registration_page import RegistrationPage
from pages.funds_transfer_page import FundsTransferPage
from pages.bill_pay_page import BillPayPage
from pages.profile_page import ProfilePage
from pages.navigation_page import NavigationPage
from pages.search_page import SearchPage


def test_multiple_failed_login_attempts(driver, base_url):
    driver.get(base_url)
    login_page = LoginPage(driver)
    for attempt in range(3):
        login_page.login("invalidUser", "invalidPass")
        assert login_page.is_error_displayed(
        ), f"Ошибка не отображается при попытке {attempt + 1}"
        driver.get(base_url)


def test_registration_mismatched_password(driver, base_url):
    driver.get(f"{base_url}/register.htm")
    registration_page = RegistrationPage(driver)
    registration_page.register(
        first_name="Mismatch",
        last_name="User",
        address="123 Any St",
        city="City",
        state="State",
        zip_code="11111",
        phone="555-1212",
        ssn="000-00-0000",
        username="mismatchuser",
        password="password123",
        confirm_password="different123"
    )
    assert not registration_page.is_registration_successful(), \
        "Регистрация прошла успешно, несмотря на несовпадающие пароли."


def test_funds_transfer_negative_amount(driver, base_url):
    driver.get(base_url)
    login_page = LoginPage(driver)
    login_page.login("john", "demo")
    driver.get(f"{base_url}/transfer.htm")
    transfer_page = FundsTransferPage(driver)
    transfer_page.transfer_funds("-50", "13344", "13344")
    assert transfer_page.is_transfer_successful(
    ), "Перевод отрицательной суммы не был выполнен успешно."


def test_funds_transfer_same_account(driver, base_url):
    driver.get(base_url)
    login_page = LoginPage(driver)
    login_page.login("john", "demo")
    driver.get(f"{base_url}/transfer.htm")
    transfer_page = FundsTransferPage(driver)
    transfer_page.transfer_funds("100", "13344", "13344")
    assert transfer_page.is_transfer_successful(
    ), "Перевод между одинаковыми счетами не был выполнен успешно."


def test_funds_transfer_non_numeric_amount(driver, base_url):
    driver.get(base_url)
    login_page = LoginPage(driver)
    login_page.login("john", "demo")
    driver.get(f"{base_url}/transfer.htm")
    transfer_page = FundsTransferPage(driver)
    transfer_page.transfer_funds("abc", "13344", "13344")
    assert transfer_page.is_transfer_error_displayed(), \
        "Ошибка не отображается при передаче нечислового значения суммы перевода."


def test_update_profile_empty_phone(driver, base_url):
    driver.get(base_url)
    login_page = LoginPage(driver)
    login_page.login("john", "demo")
    driver.get(f"{base_url}/updateprofile.htm")
    profile_page = ProfilePage(driver)
    profile_page.update_phone_number("")
    assert profile_page.is_update_successful(
    ), "Обновление профиля не прошло успешно при пустом номере телефона."


def test_access_restricted_after_logout(driver, base_url):
    driver.get(base_url)
    login_page = LoginPage(driver)
    login_page.login("john", "demo")

    logout_link = driver.find_element(By.LINK_TEXT, "Log Out")
    logout_link.click()
    time.sleep(1)

    driver.get(f"{base_url}/overview.htm")

    page_source = driver.page_source
    expected_indicator = "Customer Login"

    assert expected_indicator in page_source, (
        f"После выхода доступ к защищённой странице разрешён. Ожидается наличие '{expected_indicator}' в странице."
    )


@pytest.mark.parametrize("link_text, expected_text", [
    ("Open New Account", "Open New Account"),
    ("Accounts Overview", "Accounts Overview"),
    ("Transfer Funds", "Transfer Funds"),
    ("Bill Pay", "Bill Pay"),
    ("Find Transactions", "Find Transactions"),
    ("Update Contact Info", "Update Contact Info"),
    ("Request Loan", "Request Loan"),
    ("Log Out", "Customer Login")
])
def test_navigation_parameterized(driver, base_url, link_text, expected_text):
    driver.get(base_url)
    login_page = LoginPage(driver)
    login_page.login("john", "demo")
    navigation = NavigationPage(driver)
    navigation.navigate_to(link_text)
    assert expected_text in driver.page_source, \
        f"На странице '{link_text}' не найден ожидаемый текст: '{expected_text}'."


def test_search_empty_query(driver, base_url):
    """Проверяет, что для пустого запроса отсутствует поле поиска (функционал не реализован)."""
    driver.get(base_url)
    search_page = SearchPage(driver)
    assert not search_page.is_search_field_present(
    ), "Поле поиска обнаружено при пустом запросе."


def test_search_nonexistent_query(driver, base_url):
    """Проверяет, что для несуществующего запроса отсутствует поле поиска (функционал не реализован)."""
    driver.get(base_url)
    search_page = SearchPage(driver)
    assert not search_page.is_search_field_present(
    ), "Поле поиска обнаружено при запросе несуществующего элемента."


def test_login_session_persistence(driver, base_url):
    driver.get(base_url)
    login_page = LoginPage(driver)
    login_page.login("john", "demo")
    driver.refresh()
    assert "Accounts Overview" in driver.page_source, \
        "Сессия не сохраняется после обновления страницы."


def test_logout_link_visibility(driver, base_url):
    driver.get(base_url)
    login_page = LoginPage(driver)
    login_page.login("john", "demo")
    try:
        logout_link = driver.find_element("link text", "Log Out")
        assert logout_link.is_displayed(
        ), "Ссылка 'Log Out' не отображается после успешного входа."
    except Exception:
        pytest.fail("Ссылка 'Log Out' не найдена после успешного входа.")
