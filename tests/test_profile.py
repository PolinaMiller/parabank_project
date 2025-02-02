import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.profile_page import ProfilePage


def test_update_profile_success_message(driver, base_url):
    driver.get(base_url)
    login_page = LoginPage(driver)
    login_page.login("john", "demo")

    driver.get("https://parabank.parasoft.com/parabank/updateprofile.htm")
    profile_page = ProfilePage(driver)

    profile_page.update_phone_number("555-0000")

    time.sleep(3)

    try:
        success_element = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.ID, "updateProfileResult"))
        )
        print("DEBUG: Текст сообщения:", success_element.text)
    except Exception as e:
        print("DEBUG: Страница после обновления профиля:\n", driver.page_source)
        raise e

    assert "Profile Updated" in success_element.text, "Сообщение об успешном обновлении профиля не найдено."
