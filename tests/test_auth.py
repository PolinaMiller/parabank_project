import pytest
import allure
from selenium.webdriver.common.by import By
from pages.login_page import LoginPage
from pages.registration_page import RegistrationPage


@allure.feature("Аутентификация")
class TestAuth:

    @allure.story("Успешный вход")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_successful_login(self, driver, base_url):
        """
        Тест проверяет, что пользователь может успешно войти в систему.
        """
        with allure.step("Открыть базовый URL приложения"):
            driver.get(base_url)
        with allure.step("Ввести корректные учетные данные (john/demo) и выполнить вход"):
            login_page = LoginPage(driver)
            login_page.login("john", "demo")
        with allure.step("Проверить, что после входа отображается 'Accounts Overview'"):
            assert "Accounts Overview" in driver.page_source, "Login failed: 'Accounts Overview' not found."

    @allure.story("Неуспешный вход")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("username,password", [
        ("invalidUser", "invalidPass"),  # Некорректные учетные данные
        ("", "demo"),                    # Пустой username
        ("john", "")                     # Пустой password
    ])
    @pytest.mark.xfail(reason="Приложение ошибочно допускает вход с некорректными данными")
    def test_unsuccessful_login(self, driver, base_url, username, password):
        """
        Тест проверяет, что вход с неверными учетными данными не выполняется.
        Ожидается отображение сообщения об ошибке.
        """
        with allure.step("Открыть базовый URL приложения"):
            driver.get(base_url)
        with allure.step(f"Попытаться выполнить вход с данными: username='{username}', password='{password}'"):
            login_page = LoginPage(driver)
            login_page.login(username, password)
        with allure.step("Проверить, что отображается сообщение об ошибке"):
            if not login_page.is_error_displayed():
                pytest.fail(
                    "Error message not displayed for invalid credentials.")

    @allure.story("Успешный выход")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_successful_logout(self, driver, base_url):
        """
        Тест проверяет, что пользователь может успешно выйти из системы.
        """
        with allure.step("Открыть базовый URL и выполнить вход (john/demo)"):
            driver.get(base_url)
            login_page = LoginPage(driver)
            login_page.login("john", "demo")
        with allure.step("Найти и кликнуть по ссылке 'Log Out'"):
            logout_link = driver.find_element(
                By.XPATH, "//a[@href='logout.htm']")
            logout_link.click()
        with allure.step("Проверить, что после выхода отображается страница 'Customer Login'"):
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
    def test_registration_invalid(self, driver, base_url, first_name, last_name, address, city,
                                  state, zip_code, phone, ssn, username, password, confirm_password):
        """
        Тест проверяет, что регистрация с некорректными данными не выполняется.
        Ожидается отображение сообщения об ошибке.
        """
        with allure.step("Открыть страницу регистрации"):
            driver.get(f"{base_url}/register.htm")
            registration_page = RegistrationPage(driver)
        with allure.step("Заполнить форму регистрации с некорректными данными"):
            registration_page.register(first_name, last_name, address, city, state, zip_code,
                                       phone, ssn, username, password, confirm_password)
        with allure.step("Проверить, что отображается сообщение об ошибке"):
            error_message = registration_page.get_error_message()
            assert error_message is not None, "Expected error message not displayed for invalid registration."
