from pages.search_page import SearchPage
from pages.login_page import LoginPage

def test_search_field_absence(driver, base_url):
    driver.get(base_url)
    search_page = SearchPage(driver)
    assert not search_page.is_search_field_present(), "Поле поиска обнаружено, хотя его быть не должно."
