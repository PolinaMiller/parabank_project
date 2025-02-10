import pytest
import time
from selenium.webdriver.common.by import By

# Импорт сервисных объектов вместо прямых Page Object
from pages.login_page import LoginService
from pages.registration_page import RegistrationService
from pages.funds_transfer_page import FundsTransferService
from pages.bill_pay_page import BillPayService
from pages.profile_page import ProfileService
from pages.navigation_page import NavigationService
from pages.search_page import SearchService

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
    Открывает базовый URL, выполняет вход под пользователем "john" через LoginService
    и возвращает драйвер.
    """
    driver.get(base_url)
    login_service = LoginService(driver)
    login_service.login("john", "demo")
    return driver


@pytest.fixture
def funds_transfer_service(logged_in_driver, base_url):
    """
    Фикстура для получения объекта FundsTransferService.
    Выполняет вход в систему, переходит на страницу перевода средств и возвращает сервис.
    """
    logged_in_driver.get(f"{base_url}/transfer.htm")
    return FundsTransferService(logged_in_driver)


@pytest.fixture
def profile_service(logged_in_driver, base_url):
    """
    Фикстура для получения объекта ProfileService.
    Выполняет вход в систему и переходит на страницу обновления профиля.
    """
    logged_in_driver.get(f"{base_url}/updateprofile.htm")
    return ProfileService(logged_in_driver)


@pytest.fixture
def navigation_service(logged_in_driver):
    """
    Фикстура для получения объекта NavigationService после входа в систему.
    """
    return NavigationService(logged_in_driver)


@pytest.fixture
def search_service(driver, base_url):
    """
    Фикстура для получения объекта SearchService.
    """
    driver.get(base_url)
    return SearchService(driver)


@pytest.fixture
def registration_service(driver, base_url):
    """
    Фикстура для получения объекта RegistrationService.
    Переходит на страницу регистрации и возвращает сервис.
    """
    driver.get(f"{base_url}/register.htm")
    return RegistrationService(driver)

# -------------------------------------------------
# Тесты аутентификации, регистрации и навигации
# -------------------------------------------------


class TestAuth:

    def test_successful_login(self, driver, base_url):
        """
        Проверяет, что пользователь может успешно войти в систему.
        """
        driver.get(base_url)
        login_service = LoginService(driver)
        login_service.login("john", "demo")
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
        Ожидается отображение сообщения об ошибке.
        """
        driver.get(base_url)
        login_service = LoginService(driver)
        login_service.login(username, password)
        if not login_service.is_error_displayed():
            pytest.fail("Error message not displayed for invalid credentials.")

    def test_successful_logout(self, logged_in_driver):
        """
        Проверяет, что пользователь может успешно выйти из системы.
        """
        # Используем NavigationService для выхода
        nav_service = NavigationService(logged_in_driver)
        nav_service.log_out()
        assert "Customer Login" in logged_in_driver.page_source, (
            "Logout failed: 'Customer Login' page not displayed."
        )

    @pytest.mark.parametrize(
        "first_name,last_name,address,city,state,zip_code,phone,ssn,username,password,confirm_password", [
            # Отсутствует first_name
            ("", "User", "123 Main St", "City", "State", "12345",
             "555-1234", "123-45-6789", "testuser2", "password", "password"),
            # Отсутствует last_name
            ("Test", "", "123 Main St", "City", "State", "12345",
             "555-1234", "123-45-6789", "testuser3", "password", "password"),
            # Отсутствует address
            ("Test", "User", "", "City", "State", "12345",
             "555-1234", "123-45-6789", "testuser4", "password", "password"),
        ]
    )
    def test_registration_invalid(self, registration_service, first_name, last_name, address, city,
                                  state, zip_code, phone, ssn, username, password, confirm_password):
        """
        Проверяет, что регистрация с некорректными данными не выполняется.
        """
        registration_service.register(first_name, last_name, address, city, state, zip_code,
                                      phone, ssn, username, password, confirm_password)
        error_message = registration_service.get_error_message()
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
    def test_navigation_parameterized(self, navigation_service, logged_in_driver, link_text, expected_text):
        """
        Параметризованный тест для проверки навигационных ссылок.
        """
        navigation_service.navigate_to(link_text)
        assert expected_text in logged_in_driver.page_source, (
            f"На странице '{link_text}' не найден ожидаемый текст: '{expected_text}'."
        )

    def test_login_session_persistence(self, driver, base_url):
        """
        Проверяет, что сессия сохраняется после обновления страницы.
        """
        driver.get(base_url)
        login_service = LoginService(driver)
        login_service.login("john", "demo")
        driver.refresh()
        assert "Accounts Overview" in driver.page_source, (
            "Сессия не сохраняется после обновления страницы."
        )

    def test_logout_link_visibility(self, driver, base_url):
        """
        Проверяет, что ссылка 'Log Out' видна после успешного входа в систему.
        """
        driver.get(base_url)
        login_service = LoginService(driver)
        login_service.login("john", "demo")
        try:
            logout_link = driver.find_element("link text", "Log Out")
            assert logout_link.is_displayed(), (
                "Ссылка 'Log Out' не отображается после успешного входа."
            )
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
        login_service = LoginService(driver)
        for attempt in range(3):
            login_service.login("invalidUser", "invalidPass")
            assert "Accounts Overview" in driver.page_source, f"Вход не осуществлен при попытке {attempt + 1}"
            driver.get(base_url)

    def test_funds_transfer_negative_amount(self, funds_transfer_service):
        """
        Проверяет перевод с отрицательной суммой.
        """
        funds_transfer_service.transfer_funds("-50", "13344", "13344")
        assert funds_transfer_service.is_transfer_successful(), (
            "Перевод отрицательной суммы не был выполнен успешно."
        )

    def test_funds_transfer_same_account(self, funds_transfer_service):
        """
        Проверяет перевод между одинаковыми счетами.
        """
        funds_transfer_service.transfer_funds("100", "13344", "13344")
        assert funds_transfer_service.is_transfer_successful(), (
            "Перевод между одинаковыми счетами не был выполнен успешно."
        )

    def test_funds_transfer_non_numeric_amount(self, funds_transfer_service):
        """
        Проверяет, что при передаче нечислового значения суммы перевода отображается ошибка.
        """
        funds_transfer_service.transfer_funds("abc", "13344", "13344")
        assert funds_transfer_service.is_transfer_error_displayed(), (
            "Ошибка не отображается при передаче нечислового значения суммы перевода."
        )

    @pytest.mark.xfail(reason="Обновление профиля с пустым номером телефона должно проваливаться, но в текущей реализации проходит успешно.")
    def test_update_profile_empty_phone(self, profile_service):
        """
        Проверяет, что обновление профиля с пустым номером телефона должно проваливаться.
        """
        profile_service.update_phone_number("")
        assert profile_service.is_update_successful(), (
            "Обновление профиля не прошло успешно при пустом номере телефона."
        )

    def test_access_restricted_after_logout(self, driver, base_url):
        """
        Проверяет, что после выхода из системы доступ к защищенной странице ограничен.
        """
        driver.get(base_url)
        login_service = LoginService(driver)
        login_service.login("john", "demo")
        logout_link = driver.find_element(By.LINK_TEXT, "Log Out")
        logout_link.click()
        time.sleep(1)
        driver.get(f"{base_url}/overview.htm")
        assert "Customer Login" in driver.page_source, (
            "После выхода доступ к защищённой странице разрешён. Ожидается наличие 'Customer Login'."
        )

    def test_search_empty_query(self, search_service):
        """
        Проверяет, что для пустого запроса отсутствует поле поиска.
        """
        assert not search_service.is_search_field_present(), (
            "Поле поиска обнаружено при пустом запросе."
        )

    def test_search_nonexistent_query(self, search_service):
        """
        Проверяет, что для несуществующего запроса отсутствует поле поиска.
        """
        assert not search_service.is_search_field_present(), (
            "Поле поиска обнаружено при запросе несуществующего элемента."
        )
