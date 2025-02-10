import pytest
import time
from selenium.webdriver.common.by import By

# Импортируем сервисные объекты страниц
from pages.login_page import LoginService
from pages.registration_page import RegistrationService
from pages.account_overview_page import AccountOverviewService
from pages.funds_transfer_page import FundsTransferService
from pages.bill_pay_page import BillPayService
from pages.contact_page import ContactService
from pages.search_page import SearchService
from pages.navigation_page import NavigationService

# --------------------------
# Фикстуры для тестов
# --------------------------


@pytest.fixture
def login_service(driver, base_url):
    """
    Фикстура для выполнения входа в систему с учетными данными "john"/"demo".
    Возвращает сервисный объект LoginService.
    """
    driver.get(base_url)
    ls = LoginService(driver)
    ls.login("john", "demo")
    return ls


@pytest.fixture
def account_overview_service(driver, base_url, login_service):
    """
    Фикстура для получения сервисного объекта AccountOverviewService после входа в систему.
    Предполагается, что после логина отображается страница обзора аккаунтов.
    """
    return AccountOverviewService(driver)


@pytest.fixture
def funds_transfer_service(driver, base_url, login_service):
    """
    Фикстура для получения сервисного объекта FundsTransferService после входа в систему
    и перехода на страницу перевода средств.
    """
    driver.get(f"{base_url}/transfer.htm")
    return FundsTransferService(driver)


@pytest.fixture
def registration_service(driver, base_url):
    """
    Фикстура для получения сервисного объекта RegistrationService.
    """
    driver.get(f"{base_url}/register.htm")
    return RegistrationService(driver)


@pytest.fixture
def contact_service(driver, base_url):
    """
    Фикстура для получения сервисного объекта ContactService.
    """
    driver.get(f"{base_url}/contact.htm")
    return ContactService(driver)


@pytest.fixture
def search_service(driver, base_url):
    """
    Фикстура для получения сервисного объекта SearchService.
    """
    driver.get(base_url)
    return SearchService(driver)


# --------------------------
# Тесты
# --------------------------

def test_home_page_title_after_login(login_service, driver, base_url):
    """
    Проверка, что после входа в систему заголовок страницы корректный.
    Ожидается, что заголовок содержит "Parabank" или в исходном коде есть "Accounts Overview".
    """
    # Фикстура login_service уже выполнила вход
    assert "Parabank" in driver.title or "Accounts Overview" in driver.page_source, (
        "Заголовок главной страницы некорректен после входа в систему."
    )


def test_account_number_displayed_in_account_overview(account_overview_service):
    """
    Проверка отображения номера аккаунта '13344' в обзоре аккаунтов.
    """
    assert account_overview_service.is_account_displayed("13344"), (
        "Номер аккаунта '13344' не отображается на странице обзора аккаунтов."
    )


def test_account_balance_is_numeric(account_overview_service, driver):
    """
    Проверка, что баланс аккаунта, полученный из таблицы обзора, является числовым значением.
    """
    # Находим первый аккаунт в таблице обзора
    account_element = driver.find_element(
        By.XPATH, "//table[@id='accountTable']//a")
    account_id = account_element.text.strip()
    balance_text = account_overview_service.get_account_balance(account_id)
    try:
        balance = float(balance_text.replace("$", "").replace(",", "").strip())
    except ValueError:
        pytest.fail(f"Баланс '{balance_text}' не является числовым значением.")
    assert isinstance(
        balance, float), "Баланс аккаунта не является числовым значением."


def test_contact_page_fields_displayed(contact_service, driver):
    """
    Проверка, что на странице контактов отображаются все обязательные поля.
    """
    # Используем локаторы, определённые в сервисном объекте (наследуемых от Page Object/Elementary)
    assert driver.find_element(*contact_service.NAME_INPUT).is_displayed(), (
        "Поле 'Name' не отображается на странице контактов."
    )
    assert driver.find_element(*contact_service.EMAIL_INPUT).is_displayed(), (
        "Поле 'Email' не отображается на странице контактов."
    )
    assert driver.find_element(*contact_service.PHONE_INPUT).is_displayed(), (
        "Поле 'Phone' не отображается на странице контактов."
    )
    assert driver.find_element(*contact_service.MESSAGE_INPUT).is_displayed(), (
        "Поле 'Message' не отображается на странице контактов."
    )


def test_funds_transfer_balance_update(funds_transfer_service, account_overview_service, driver, base_url):
    """
    Проверка корректного обновления баланса аккаунта после перевода средств.
    Тест предполагает, что у пользователя есть минимум два аккаунта.
    """
    # Находим все аккаунты на странице обзора
    account_elements = driver.find_elements(
        By.XPATH, "//table[@id='accountTable']//a")
    if len(account_elements) < 2:
        pytest.skip("Недостаточно аккаунтов для выполнения теста.")
    from_account = account_elements[0].text.strip()
    to_account = account_elements[1].text.strip()

    # Получаем начальный баланс исходного аккаунта
    initial_balance_text = account_overview_service.get_account_balance(
        from_account)
    try:
        initial_balance = float(initial_balance_text.replace(
            "$", "").replace(",", "").strip())
    except ValueError:
        pytest.skip(
            "Начальный баланс не является числовым значением. Пропускаем тест обновления баланса.")

    transfer_amount = 50.0
    # Переходим на страницу перевода средств (фикстура funds_transfer_service уже это делает)
    funds_transfer_service.transfer_funds(
        str(transfer_amount), from_account, to_account)
    # Явное ожидание можно заменить динамическим ожиданием
    time.sleep(2)
    driver.get(f"{base_url}/overview.htm")
    updated_balance_text = account_overview_service.get_account_balance(
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
    # Выполняем вход через LoginService
    ls = LoginService(driver)
    ls.login("john", "demo")
    driver.get(f"{base_url}/billpay.htm")
    bill_pay_service = BillPayService(driver)
    bill_pay_service.pay_bill(
        payee_name="Electric Company",
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
    assert bill_pay_service.is_payment_successful(), "Bill payment was not successful."


def test_registration_page_fields_visibility(registration_service, driver):
    """
    Проверка видимости всех обязательных полей на странице регистрации.
    """
    # Список локаторов обязательных полей регистрации
    fields = [
        registration_service.FIRST_NAME_INPUT,
        registration_service.LAST_NAME_INPUT,
        registration_service.ADDRESS_INPUT,
        registration_service.CITY_INPUT,
        registration_service.STATE_INPUT,
        registration_service.ZIP_CODE_INPUT,
        registration_service.PHONE_INPUT,
        registration_service.SSN_INPUT,
        registration_service.USERNAME_INPUT,
        registration_service.PASSWORD_INPUT,
        registration_service.CONFIRM_PASSWORD_INPUT,
    ]
    for locator in fields:
        element = driver.find_element(*locator)
        assert element.is_displayed(
        ), f"Поле с локатором {locator} не отображается на странице регистрации."


def test_search_results_content(search_service, driver):
    """
    Проверяет, что контейнер с результатами поиска отсутствует.
    """
    results = driver.find_elements(*search_service.RESULTS)
    assert len(
        results) == 0, "Контейнер результатов поиска обнаружен, хотя его быть не должно."


def test_logout_invalidates_session(driver, base_url):
    """
    Проверяет, что после выхода из системы пользователь не может получить доступ к защищённой странице,
    даже если сессионная кука (JSESSIONID) остается.
    """
    driver.get(base_url)
    ls = LoginService(driver)
    ls.login("john", "demo")
    # Используем NavigationService для выхода
    nav_service = NavigationService(driver)
    nav_service.log_out()
    time.sleep(1)
    driver.get(f"{base_url}/overview.htm")
    page_source = driver.page_source
    expected_indicator = "Customer Login"
    assert expected_indicator in page_source, (
        "После выхода из системы доступ к защищённой странице разрешён, "
        "что свидетельствует о том, что сессия не аннулирована."
    )
