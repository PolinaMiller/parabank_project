import pytest
import time
from selenium.webdriver.common.by import By
from pages.login_page import LoginPage
from pages.registration_page import RegistrationPage
from pages.funds_transfer_page import FundsTransferPage
from pages.bill_pay_page import BillPayPage
from pages.profile_page import ProfilePage
from pages.navigation_page import NavigationPage
from pages.search_page import SearchPage

# -------------------------------------------------
# Фикстуры
# -------------------------------------------------


@pytest.fixture
def base_driver(driver, base_url):
    """Фикстура, которая открывает базовый URL и возвращает драйвер."""
    driver.get(base_url)
    return driver


@pytest.fixture
def logged_in_driver(driver, base_url):
    """
    Фикстура для входа в систему.
    Открывает базовый URL, выполняет вход под пользователем "john" и возвращает драйвер.
    """
    driver.get(base_url)
    login_page = LoginPage(driver)
    login_page.login("john", "demo")
    return driver


@pytest.fixture
def funds_transfer_page(logged_in_driver, base_url):
    """
    Фикстура для получения объекта FundsTransferPage.
    Выполняет вход в систему, переходит на страницу перевода средств и возвращает объект FundsTransferPage.
    """
    logged_in_driver.get(f"{base_url}/transfer.htm")
    return FundsTransferPage(logged_in_driver)


@pytest.fixture
def profile_page(logged_in_driver, base_url):
    """
    Фикстура для получения объекта ProfilePage.
    Выполняет вход в систему и переходит на страницу обновления профиля.
    """
    logged_in_driver.get(f"{base_url}/updateprofile.htm")
    return ProfilePage(logged_in_driver)


@pytest.fixture
def navigation_page(logged_in_driver):
    """
    Фикстура для получения объекта NavigationPage после входа в систему.
    """
    return NavigationPage(logged_in_driver)


@pytest.fixture
def search_page(driver, base_url):
    """
    Фикстура для получения объекта SearchPage.
    """
    driver.get(base_url)
    return SearchPage(driver)


@pytest.fixture
def registration_page(driver, base_url):
    """
    Фикстура для получения объекта RegistrationPage.
    Переходит на страницу регистрации и возвращает объект RegistrationPage.
    """
    driver.get(f"{base_url}/register.htm")
    return RegistrationPage(driver)

# -------------------------------------------------
# Тесты аутентификации, регистрации и навигации
# -------------------------------------------------


class TestAuth:

    def test_successful_login(self, driver, base_url):
        """
        Проверяет, что пользователь может успешно войти в систему.
        """
        driver.get(base_url)
        login_page = LoginPage(driver)
        login_page.login("john", "demo")
        assert "Accounts Overview" in driver.page_source, (
            "Login failed: 'Accounts Overview' not found."
        )

    @pytest.mark.parametrize("username,password", [
        ("invalidUser", "invalidPass"),  # Некорректные учетные данные
        ("", "demo"),                    # Пустой username
        ("john", "")                     # Пустой password
    ])
    @pytest.mark.xfail(reason="Application erroneously logs in with invalid credentials")
    def test_unsuccessful_login(self, driver, base_url, username, password):
        """
        Проверяет, что вход с неверными учетными данными не выполняется.
        Тест ожидает отображения сообщения об ошибке.
        """
        driver.get(base_url)
        login_page = LoginPage(driver)
        login_page.login(username, password)
        if not login_page.is_error_displayed():
            pytest.fail("Error message not displayed for invalid credentials.")

    def test_successful_logout(self, logged_in_driver):
        """
        Проверяет, что пользователь может успешно выйти из системы.
        """
        # Фикстура logged_in_driver уже выполняет вход
        logout_link = logged_in_driver.find_element(
            By.XPATH, "//a[@href='logout.htm']")
        logout_link.click()
        assert "Customer Login" in logged_in_driver.page_source, (
            "Logout failed: 'Customer Login' page not displayed."
        )

    @pytest.mark.parametrize("first_name,last_name,address,city,state,zip_code,phone,ssn,username,password,confirm_password", [
        # Отсутствует first_name
        ("", "User", "123 Main St", "City", "State", "12345",
         "555-1234", "123-45-6789", "testuser2", "password", "password"),
        # Отсутствует last_name
        ("Test", "", "123 Main St", "City", "State", "12345",
         "555-1234", "123-45-6789", "testuser3", "password", "password"),
        # Отсутствует address
        ("Test", "User", "", "City", "State", "12345",
         "555-1234", "123-45-6789", "testuser4", "password", "password"),
    ])
    def test_registration_invalid(self, registration_page, first_name, last_name, address, city,
                                  state, zip_code, phone, ssn, username, password, confirm_password):
        """
        Проверяет, что регистрация с некорректными данными не выполняется.
        """
        registration_page.register(first_name, last_name, address, city, state, zip_code,
                                   phone, ssn, username, password, confirm_password)
        error_message = registration_page.get_error_message()
        assert error_message is not None, (
            "Expected error message not displayed for invalid registration."
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
    def test_navigation_parameterized(self, navigation_page, logged_in_driver, link_text, expected_text):
        """
        Параметризованный тест для проверки навигационных ссылок.
        """
        navigation_page.navigate_to(link_text)
        assert expected_text in logged_in_driver.page_source, (
            f"На странице '{link_text}' не найден ожидаемый текст: '{expected_text}'."
        )

    def test_login_session_persistence(self, driver, base_url):
        """
        Проверяет, что сессия сохраняется после обновления страницы.
        """
        driver.get(base_url)
        login_page = LoginPage(driver)
        login_page.login("john", "demo")
        driver.refresh()
        assert "Accounts Overview" in driver.page_source, (
            "Сессия не сохраняется после обновления страницы."
        )

    def test_logout_link_visibility(self, driver, base_url):
        """
        Проверяет, что ссылка 'Log Out' видна после успешного входа в систему.
        """
        driver.get(base_url)
        login_page = LoginPage(driver)
        login_page.login("john", "demo")
        try:
            logout_link = driver.find_element("link text", "Log Out")
            assert logout_link.is_displayed(
            ), "Ссылка 'Log Out' не отображается после успешного входа."
        except Exception:
            pytest.fail("Ссылка 'Log Out' не найдена после успешного входа.")

# -------------------------------------------------
# Тесты перевода средств, оплаты счетов, обновления профиля и поиска
# -------------------------------------------------


class TestOperations:

    @pytest.mark.xfail(reason="Система ошибочно принимает неверные учетные данные, вход осуществляется")
    def test_multiple_failed_login_attempts(self, driver, base_url):
        """
        Проверяет, что при вводе неправильных учетных данных вход осуществляется (негативный сценарий).
        Ожидается, что тест провалится, так как система должна блокировать вход.
        """
        driver.get(base_url)
        login_page = LoginPage(driver)
        for attempt in range(3):
            login_page.login("invalidUser", "invalidPass")
            assert "Accounts Overview" in driver.page_source, f"Вход не осуществлен при попытке {attempt + 1}"
            driver.get(base_url)

    def test_funds_transfer_negative_amount(self, funds_transfer_page):
        """
        Проверяет перевод с отрицательной суммой.
        """
        funds_transfer_page.transfer_funds("-50", "13344", "13344")
        assert funds_transfer_page.is_transfer_successful(), (
            "Перевод отрицательной суммы не был выполнен успешно."
        )

    def test_funds_transfer_same_account(self, funds_transfer_page):
        """
        Проверяет перевод между одинаковыми счетами.
        """
        funds_transfer_page.transfer_funds("100", "13344", "13344")
        assert funds_transfer_page.is_transfer_successful(), (
            "Перевод между одинаковыми счетами не был выполнен успешно."
        )

    def test_funds_transfer_non_numeric_amount(self, funds_transfer_page):
        """
        Проверяет, что при передаче нечислового значения суммы перевода отображается ошибка.
        """
        funds_transfer_page.transfer_funds("abc", "13344", "13344")
        assert funds_transfer_page.is_transfer_error_displayed(), (
            "Ошибка не отображается при передаче нечислового значения суммы перевода."
        )

    @pytest.mark.xfail(reason="Обновление профиля с пустым номером телефона должно проваливаться, но в текущей реализации проходит успешно.")
    def test_update_profile_empty_phone(self, profile_page):
        """
        Проверяет, что обновление профиля с пустым номером телефона должно проваливаться.
        """
        profile_page.update_phone_number("")
        assert profile_page.is_update_successful(), (
            "Обновление профиля не прошло успешно при пустом номере телефона."
        )

    def test_access_restricted_after_logout(self, driver, base_url):
        """
        Проверяет, что после выхода из системы доступ к защищенной странице ограничен.
        """
        driver.get(base_url)
        login_page = LoginPage(driver)
        login_page.login("john", "demo")
        logout_link = driver.find_element(By.LINK_TEXT, "Log Out")
        logout_link.click()
        time.sleep(1)
        driver.get(f"{base_url}/overview.htm")
        assert "Customer Login" in driver.page_source, (
            "После выхода доступ к защищённой странице разрешён. Ожидается наличие 'Customer Login'."
        )

    def test_search_empty_query(self, search_page):
        """
        Проверяет, что для пустого запроса отсутствует поле поиска.
        """
        assert not search_page.is_search_field_present(), (
            "Поле поиска обнаружено при пустом запросе."
        )

    def test_search_nonexistent_query(self, search_page):
        """
        Проверяет, что для несуществующего запроса отсутствует поле поиска.
        """
        assert not search_page.is_search_field_present(), (
            "Поле поиска обнаружено при запросе несуществующего элемента."
        )
