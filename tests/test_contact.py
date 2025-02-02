from pages.contact_page import ContactPage
from pages.login_page import LoginPage
import time


def test_contact_us_submission(driver, base_url):
    driver.get(base_url)
    driver.get(f"{base_url}/contact.htm")
    contact_page = ContactPage(driver)
    contact_page.submit_contact_form(
        "Test User", "test@example.com", "555-1234", "This is a test message.")
    assert contact_page.is_submission_successful(), "Contact form submission failed."


def test_contact_form_invalid_email(driver, base_url):
    """Проверка, что контактная форма принимает email с неверным форматом."""
    driver.get(f"{base_url}/contact.htm")
    contact_page = ContactPage(driver)
    contact_page.submit_contact_form(
        "Test User", "invalidemail", "555-1234", "Проверка неверного email."
    )
    time.sleep(1)
    assert contact_page.is_submission_successful(), \
        "Контактная форма не приняла email с неверным форматом."
