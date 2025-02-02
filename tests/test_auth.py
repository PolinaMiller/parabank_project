import pytest
from pages.login_page import LoginPage
from pages.registration_page import RegistrationPage


@pytest.mark.usefixtures("driver", "base_url")
class TestAuth:

    def test_successful_login(self, driver, base_url):
        driver.get(base_url)
        login_page = LoginPage(driver)
        login_page.login("john", "demo")
        assert "Accounts Overview" in driver.page_source, "Login failed: Accounts Overview not found."

    @pytest.mark.parametrize("username,password", [
        ("invalidUser", "invalidPass"),
        ("", "demo"),
        ("john", "")
    ])
    def test_unsuccessful_login(self, driver, base_url, username, password):
        driver.get(base_url)
        login_page = LoginPage(driver)
        login_page.login(username, password)
        assert login_page.is_error_displayed(
        ), "Error message not displayed for invalid credentials."

    def test_successful_logout(self, driver, base_url):
        driver.get(base_url)
        login_page = LoginPage(driver)
        login_page.login("john", "demo")
        logout_link = driver.find_element("link text", "Log Out")
        logout_link.click()
        assert "Customer Login" in driver.page_source, "Logout failed: Customer Login page not displayed."

    def test_registration_valid(self, driver, base_url):
        driver.get(f"{base_url}/register.htm")
        registration_page = RegistrationPage(driver)
        registration_page.register("Test", "User", "123 Main St", "City", "State", "12345",
                                   "555-1234", "123-45-6789", "testuser1", "password", "password")
        assert registration_page.is_registration_successful(
        ), "Registration failed with valid data."

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
        driver.get(f"{base_url}/register.htm")
        registration_page = RegistrationPage(driver)
        registration_page.register(first_name, last_name, address, city, state, zip_code,
                                   phone, ssn, username, password, confirm_password)
        assert not registration_page.is_registration_successful(
        ), "Registration succeeded with invalid data."
