import pytest
import allure
import logging
from selenium.webdriver.common.by import By
from pages.login_page import LoginService
from pages.registration_page import RegistrationService
from pages.navigation_page import NavigationService

# Настройка логирования: вывод сообщений уровня INFO и выше.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@allure.feature("Аутентификация")
class TestAuth:

    @allure.story("Успешный вход")
    @allure.severity(allure.severity_level.CRITICAL)
    # TC-1: Успешный вход в систему
    def test_successful_login(self, driver, base_url):
        """
        Тест проверяет, что пользователь может успешно войти в систему.
        """
        with allure.step("Открыть базовый URL приложения"):
            logger.info("Открытие базового URL: %s", base_url)
            driver.get(base_url)
        with allure.step("Ввести корректные учетные данные (john/demo) и выполнить вход"):
            logger.info("Выполняется вход с данными: john/demo")
            login_service = LoginService(driver)
            login_service.login("john", "demo")
        with allure.step("Проверить, что после входа отображается 'Accounts Overview'"):
            logger.info(
                "Проверка наличия текста 'Accounts Overview' на странице")
            assert "Accounts Overview" in driver.page_source, "Login failed: 'Accounts Overview' not found."

    @allure.story("Неуспешный вход")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("username,password", [
        ("invalidUser", "invalidPass"),  # Некорректные учетные данные
        ("", "demo"),                    # Пустой username
        ("john", "")                     # Пустой password
    ])
    @pytest.mark.xfail(reason="Приложение ошибочно допускает вход с некорректными данными")
    # TC-2: Неуспешный вход с некорректными данными
    def test_unsuccessful_login(self, driver, base_url, username, password):
        """
        Тест проверяет, что вход с неверными учетными данными не выполняется.
        Ожидается отображение сообщения об ошибке.
        """
        with allure.step("Открыть базовый URL приложения"):
            logger.info("Открытие базового URL: %s", base_url)
            driver.get(base_url)
        with allure.step(f"Попытаться выполнить вход с данными: username='{username}', password='{password}'"):
            logger.info(
                "Попытка входа с username='%s' и password='%s'", username, password)
            login_service = LoginService(driver)
            login_service.login(username, password)
        with allure.step("Проверить, что отображается сообщение об ошибке"):
            logger.info("Проверка наличия сообщения об ошибке на странице")
            if not login_service.is_error_displayed():
                pytest.fail(
                    "Error message not displayed for invalid credentials.")

    @allure.story("Успешный выход")
    @allure.severity(allure.severity_level.CRITICAL)
    # TC-3: Успешный выход из системы
    def test_successful_logout(self, driver, base_url):
        """
        Тест проверяет, что пользователь может успешно выйти из системы.
        """
        with allure.step("Открыть базовый URL и выполнить вход (john/demo)"):
            logger.info("Открытие базового URL: %s", base_url)
            driver.get(base_url)
            login_service = LoginService(driver)
            logger.info("Выполняется вход с учетными данными: john/demo")
            login_service.login("john", "demo")
        with allure.step("Выполнить выход из системы"):
            logger.info("Выполнение выхода из системы через NavigationService")
            nav_service = NavigationService(driver)
            nav_service.log_out()
        with allure.step("Проверить, что после выхода отображается страница 'Customer Login'"):
            logger.info("Проверка наличия текста 'Customer Login' на странице")
            assert "Customer Login" in driver.page_source, "Logout failed: 'Customer Login' page not displayed."

    @allure.story("Некорректная регистрация")
    @allure.severity(allure.severity_level.NORMAL)
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
    # TC-4: Некорректная регистрация
    def test_registration_invalid(self, driver, base_url, first_name, last_name, address, city,
                                  state, zip_code, phone, ssn, username, password, confirm_password):
        with allure.step("Открыть страницу регистрации"):
            registration_url = f"{base_url}/register.htm"
            logger.info("Переход на страницу регистрации: %s",
                        registration_url)
            driver.get(registration_url)
            registration_service = RegistrationService(driver)
        with allure.step("Заполнить форму регистрации с некорректными данными"):
            logger.info(
                "Заполнение формы регистрации с данными: first_name='%s', last_name='%s'", first_name, last_name)
            registration_service.register(first_name, last_name, address, city, state, zip_code,
                                          phone, ssn, username, password, confirm_password)
        with allure.step("Проверить, что отображается сообщение об ошибке"):
            error_message = registration_service.get_error_message()
            logger.info(
                "Проверка наличия сообщения об ошибке. Получено сообщение: %s", error_message)
            assert error_message is not None, "Expected error message not displayed for invalid registration."
