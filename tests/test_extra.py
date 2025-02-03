from selenium.webdriver.common.by import By
import pytest
import time
from pages.login_page import LoginPage
from pages.registration_page import RegistrationPage
from pages.account_overview_page import AccountOverviewPage
from pages.funds_transfer_page import FundsTransferPage
from pages.bill_pay_page import BillPayPage
from pages.contact_page import ContactPage
from pages.search_page import SearchPage


def test_home_page_title_after_login(driver, base_url):
    """Проверка, что после входа в систему заголовок страницы корректный."""
    driver.get(base_url)
    login_page = LoginPage(driver)
    login_page.login("john", "demo")
    assert "Parabank" in driver.title or "Accounts Overview" in driver.page_source, \
        "Заголовок главной страницы некорректен после входа в систему."


def test_account_number_displayed_in_account_overview(driver, base_url):
    """Проверка отображения номера аккаунта '13344' в обзоре аккаунтов."""
    driver.get(base_url)
    login_page = LoginPage(driver)
    login_page.login("john", "demo")
    account_overview = AccountOverviewPage(driver)
    assert account_overview.is_account_displayed("13344"), \
        "Номер аккаунта '13344' не отображается на странице обзора аккаунтов."


def test_account_balance_is_numeric(driver, base_url):
    driver.get(base_url)
    login_page = LoginPage(driver)
    login_page.login("john", "demo")
    account_overview = AccountOverviewPage(driver)

    account_element = driver.find_element(
        By.XPATH, "//table[@id='accountTable']//a")
    account_id = account_element.text.strip()

    balance_text = account_overview.get_account_balance(account_id)
    try:
        balance = float(balance_text.replace("$", "").replace(",", "").strip())
    except ValueError:
        pytest.fail(f"Баланс '{balance_text}' не является числовым значением.")

    assert isinstance(
        balance, float), "Баланс аккаунта не является числовым значением."


def test_contact_page_fields_displayed(driver, base_url):
    """Проверка, что на странице контактов отображаются все обязательные поля."""
    driver.get(f"{base_url}/contact.htm")
    contact_page = ContactPage(driver)
    assert driver.find_element(*contact_page.NAME_INPUT).is_displayed(), \
        "Поле 'Name' не отображается на странице контактов."
    assert driver.find_element(*contact_page.EMAIL_INPUT).is_displayed(), \
        "Поле 'Email' не отображается на странице контактов."
    assert driver.find_element(*contact_page.PHONE_INPUT).is_displayed(), \
        "Поле 'Phone' не отображается на странице контактов."
    assert driver.find_element(*contact_page.MESSAGE_INPUT).is_displayed(), \
        "Поле 'Message' не отображается на странице контактов."


def test_funds_transfer_balance_update(driver, base_url):
    driver.get(base_url)
    login_page = LoginPage(driver)
    login_page.login("john", "demo")
    account_overview = AccountOverviewPage(driver)
    account_elements = driver.find_elements(
        By.XPATH, "//table[@id='accountTable']//a")
    if len(account_elements) < 2:
        pytest.skip("Недостаточно аккаунтов для выполнения теста.")
    from_account = account_elements[0].text.strip()
    to_account = account_elements[1].text.strip()
    initial_balance_text = account_overview.get_account_balance(from_account)

    try:
        initial_balance = float(initial_balance_text.replace(
            "$", "").replace(",", "").strip())
    except ValueError:
        pytest.skip(
            "Начальный баланс не является числовым значением. Пропускаем тест обновления баланса.")

    transfer_amount = 50.0
    driver.get(f"{base_url}/transfer.htm")
    transfer_page = FundsTransferPage(driver)
    transfer_page.transfer_funds(
        str(transfer_amount), from_account, to_account)

    time.sleep(2)

    driver.get(f"{base_url}/overview.htm")
    updated_balance_text = account_overview.get_account_balance(from_account)
    try:
        updated_balance = float(updated_balance_text.replace(
            "$", "").replace(",", "").strip())
    except ValueError:
        pytest.fail("Обновленный баланс не является числовым значением.")

    expected_balance = initial_balance - transfer_amount
    assert abs(updated_balance - expected_balance) < 0.01, \
        f"Баланс не обновлен корректно: ожидалось {expected_balance}, получено {updated_balance}."


def test_bill_pay_confirmation_details(driver, base_url):
    driver.get(base_url)
    login_page = LoginPage(driver)
    login_page.login("john", "demo")
    driver.get(f"{base_url}/billpay.htm")
    bill_pay = BillPayPage(driver)
    payee_name = "Electric Company"
    bill_pay.pay_bill(
        payee_name=payee_name,
        address="456 Electric Ave",
        city="City",
        state="State",
        zip_code="67890",
        phone="555-6789",
        account="987654",
        verify_account="987654",
        amount="200",
        from_account="13344"
    )
    assert bill_pay.is_payment_successful(), "Bill payment was not successful."


def test_registration_page_fields_visibility(driver, base_url):
    """Проверка видимости всех обязательных полей на странице регистрации."""
    driver.get(f"{base_url}/register.htm")
    registration_page = RegistrationPage(driver)
    fields = [
        registration_page.FIRST_NAME_INPUT,
        registration_page.LAST_NAME_INPUT,
        registration_page.ADDRESS_INPUT,
        registration_page.CITY_INPUT,
        registration_page.STATE_INPUT,
        registration_page.ZIP_CODE_INPUT,
        registration_page.PHONE_INPUT,
        registration_page.SSN_INPUT,
        registration_page.USERNAME_INPUT,
        registration_page.PASSWORD_INPUT,
        registration_page.CONFIRM_PASSWORD_INPUT,
    ]
    for locator in fields:
        element = driver.find_element(*locator)
        assert element.is_displayed(
        ), f"Поле с локатором {locator} не отображается на странице регистрации."


def test_search_results_content(driver, base_url):
    """Проверяет, что контейнер с результатами поиска отсутствует."""
    driver.get(base_url)
    search_page = SearchPage(driver)
    results = driver.find_elements(*search_page.RESULTS)
    assert len(
        results) == 0, "Контейнер результатов поиска обнаружен, хотя его быть не должно."


def test_logout_invalidates_session(driver, base_url):
    """
    Проверяет, что после выхода из системы пользователь не может получить доступ к защищённой странице,
    даже если сессионная кука (JSESSIONID) остается.
    """
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
        "После выхода из системы доступ к защищённой странице разрешён, "
        "что свидетельствует о том, что сессия не аннулирована."
    )
