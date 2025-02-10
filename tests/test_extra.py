import pytest
import time
from selenium.webdriver.common.by import By
from pages.login_page import LoginPage
from pages.registration_page import RegistrationPage
from pages.account_overview_page import AccountOverviewPage
from pages.funds_transfer_page import FundsTransferPage
from pages.bill_pay_page import BillPayPage
from pages.contact_page import ContactPage
from pages.search_page import SearchPage

# --------------------------
# Фикстуры для тестов
# --------------------------


@pytest.fixture
def login_user(driver, base_url):
    """
    Фикстура для выполнения входа в систему с учетными данными "john"/"demo".
    Возвращает экземпляр LoginPage для дальнейшего взаимодействия.
    """
    driver.get(base_url)
    login_page = LoginPage(driver)
    login_page.login("john", "demo")
    return login_page


@pytest.fixture
def account_overview_page(driver, base_url, login_user):
    """
    Фикстура для получения объекта AccountOverviewPage после входа в систему.
    """
    # После входа переходим на страницу обзора аккаунтов
    return AccountOverviewPage(driver)


@pytest.fixture
def funds_transfer_page(driver, base_url, login_user):
    """
    Фикстура для получения объекта FundsTransferPage после входа в систему и перехода на страницу перевода средств.
    """
    driver.get(f"{base_url}/transfer.htm")
    return FundsTransferPage(driver)


@pytest.fixture
def registration_page(driver, base_url):
    """
    Фикстура для получения объекта RegistrationPage.
    """
    driver.get(f"{base_url}/register.htm")
    return RegistrationPage(driver)


@pytest.fixture
def contact_page(driver, base_url):
    """
    Фикстура для получения объекта ContactPage.
    """
    driver.get(f"{base_url}/contact.htm")
    return ContactPage(driver)


@pytest.fixture
def search_page(driver, base_url):
    """
    Фикстура для получения объекта SearchPage.
    """
    driver.get(base_url)
    return SearchPage(driver)

# --------------------------
# Тесты
# --------------------------


def test_home_page_title_after_login(driver, base_url):
    """Проверка, что после входа в систему заголовок страницы корректный."""
    driver.get(base_url)
    login_page = LoginPage(driver)
    login_page.login("john", "demo")
    # Проверяем, что заголовок содержит "Parabank" или страница содержит "Accounts Overview"
    assert "Parabank" in driver.title or "Accounts Overview" in driver.page_source, (
        "Заголовок главной страницы некорректен после входа в систему."
    )


def test_account_number_displayed_in_account_overview(account_overview_page):
    """Проверка отображения номера аккаунта '13344' в обзоре аккаунтов."""
    # Проверяем, что номер аккаунта "13344" отображается на странице
    assert account_overview_page.is_account_displayed("13344"), (
        "Номер аккаунта '13344' не отображается на странице обзора аккаунтов."
    )


def test_account_balance_is_numeric(account_overview_page, driver):
    """
    Проверка, что баланс аккаунта, полученный из таблицы обзора, является числовым значением.
    """
    # Находим первый элемент аккаунта в таблице
    account_element = driver.find_element(
        By.XPATH, "//table[@id='accountTable']//a")
    account_id = account_element.text.strip()
    # Получаем текст баланса для найденного аккаунта
    balance_text = account_overview_page.get_account_balance(account_id)
    try:
        balance = float(balance_text.replace("$", "").replace(",", "").strip())
    except ValueError:
        pytest.fail(f"Баланс '{balance_text}' не является числовым значением.")
    # Проверяем, что баланс является числом типа float
    assert isinstance(
        balance, float), "Баланс аккаунта не является числовым значением."


def test_contact_page_fields_displayed(contact_page, driver):
    """Проверка, что на странице контактов отображаются все обязательные поля."""
    # Проверяем видимость каждого обязательного поля на странице контактов
    assert driver.find_element(*contact_page.NAME_INPUT).is_displayed(), (
        "Поле 'Name' не отображается на странице контактов."
    )
    assert driver.find_element(*contact_page.EMAIL_INPUT).is_displayed(), (
        "Поле 'Email' не отображается на странице контактов."
    )
    assert driver.find_element(*contact_page.PHONE_INPUT).is_displayed(), (
        "Поле 'Phone' не отображается на странице контактов."
    )
    assert driver.find_element(*contact_page.MESSAGE_INPUT).is_displayed(), (
        "Поле 'Message' не отображается на странице контактов."
    )


def test_funds_transfer_balance_update(funds_transfer_page, account_overview_page, driver, base_url):
    """
    Проверка корректного обновления баланса аккаунта после перевода средств.
    Тест предполагает, что у пользователя есть минимум два аккаунта.
    """
    # Получаем все элементы аккаунтов из таблицы
    account_elements = driver.find_elements(
        By.XPATH, "//table[@id='accountTable']//a")
    if len(account_elements) < 2:
        pytest.skip("Недостаточно аккаунтов для выполнения теста.")
    # Выбираем первый аккаунт для списания и второй для зачисления
    from_account = account_elements[0].text.strip()
    to_account = account_elements[1].text.strip()
    # Получаем начальный баланс исходного аккаунта
    initial_balance_text = account_overview_page.get_account_balance(
        from_account)
    try:
        initial_balance = float(initial_balance_text.replace(
            "$", "").replace(",", "").strip())
    except ValueError:
        pytest.skip(
            "Начальный баланс не является числовым значением. Пропускаем тест обновления баланса.")
    transfer_amount = 50.0
    # Переходим на страницу перевода средств
    driver.get(f"{base_url}/transfer.htm")
    funds_transfer_page.transfer_funds(
        str(transfer_amount), from_account, to_account)
    # Ждем некоторое время для обновления баланса (рекомендуется заменить явное ожидание на динамическое ожидание)
    time.sleep(2)
    # Переходим обратно на страницу обзора аккаунтов
    driver.get(f"{base_url}/overview.htm")
    updated_balance_text = account_overview_page.get_account_balance(
        from_account)
    try:
        updated_balance = float(updated_balance_text.replace(
            "$", "").replace(",", "").strip())
    except ValueError:
        pytest.fail("Обновленный баланс не является числовым значением.")
    expected_balance = initial_balance - transfer_amount
    assert abs(updated_balance - expected_balance) < 0.01, (
        f"Баланс не обновлен корректно: ожидалось {expected_balance}, получено {updated_balance}."
    )


def test_bill_pay_confirmation_details(driver, base_url):
    """
    Проверка, что после оплаты счета отображается сообщение об успешном выполнении операции.
    """
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


def test_registration_page_fields_visibility(registration_page, driver):
    """Проверка видимости всех обязательных полей на странице регистрации."""
    # Список локаторов обязательных полей регистрации
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
    # Проверяем, что каждый элемент присутствует и видим
    for locator in fields:
        element = driver.find_element(*locator)
        assert element.is_displayed(
        ), f"Поле с локатором {locator} не отображается на странице регистрации."


def test_search_results_content(search_page, driver):
    """Проверяет, что контейнер с результатами поиска отсутствует."""
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
