import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.registration_page import RegistrationPage


class TestAuth:

    def test_successful_login(self, driver, base_url):
        """
        Проверяет, что пользователь может успешно войти в систему.
        """
        driver.get(base_url)
        login_page = LoginPage(driver)
        login_page.login("john", "demo")
        assert "Accounts Overview" in driver.page_source, "Login failed: 'Accounts Overview' not found."

    @pytest.mark.parametrize("username,password", [
        ("invalidUser", "invalidPass"),
        ("", "demo"),
        ("john", "")
    ])
    @pytest.mark.xfail(reason="Application erroneously logs in with invalid credentials")
    def test_unsuccessful_login(self, driver, base_url, username, password):
        """
        Проверяет, что вход с неверными учетными данными не выполняется.
        """
        driver.get(base_url)
        login_page = LoginPage(driver)
        login_page.login(username, password)

        if not login_page.is_error_displayed():
            pytest.fail("Error message not displayed for invalid credentials.")

    def test_successful_logout(self, driver, base_url):
        """
        Проверяет, что пользователь может успешно выйти из системы.
        """
        driver.get(base_url)
        login_page = LoginPage(driver)
        login_page.login("john", "demo")

        logout_link = driver.find_element(By.XPATH, "//a[@href='logout.htm']")
        logout_link.click()
        assert "Customer Login" in driver.page_source, "Logout failed: 'Customer Login' page not displayed."

    @pytest.mark.parametrize("first_name,last_name,address,city,state,zip_code,phone,ssn,username,password,confirm_password", [
        ("", "User", "123 Main St", "City", "State", "12345",
         "555-1234", "123-45-6789", "testuser2", "password", "password"),
        ("Test", "", "123 Main St", "City", "State", "12345",
         "555-1234", "123-45-6789", "testuser3", "password", "password"),
        ("Test", "User", "", "City", "State", "12345", "555-1234",
         "123-45-6789", "testuser4", "password", "password"),
    ])
    def test_registration_invalid(self, driver, base_url, first_name, last_name, address, city, state,
                                  zip_code, phone, ssn, username, password, confirm_password):
        """
        Проверяет, что регистрация с некорректными данными не выполняется.
        """
        driver.get(f"{base_url}/register.htm")
        registration_page = RegistrationPage(driver)
        registration_page.register(first_name, last_name, address, city, state, zip_code,
                                   phone, ssn, username, password, confirm_password)

        error_message = registration_page.get_error_message()
        assert error_message is not None, "Expected error message not displayed for invalid registration."
