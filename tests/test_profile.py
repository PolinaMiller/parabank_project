from pages.profile_page import ProfilePage
from pages.login_page import LoginPage
import time


def test_update_profile(driver, base_url):
    driver.get(base_url)
    login_page = LoginPage(driver)
    login_page.login("john", "demo")
    driver.get(f"{base_url}/updateprofile.htm")
    profile_page = ProfilePage(driver)
    profile_page.update_phone_number("555-0000")

    time.sleep(2)

    current_url = driver.current_url.lower()
    page_source = driver.page_source.lower()

    assert "error" in current_url or "error" in page_source, \
        "Ожидалась страница ошибки после обновления номера, но она не была отображена."
