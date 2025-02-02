from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class SearchPage(BasePage):
    SEARCH_INPUT = (By.XPATH, "//*[@id='search']")
    RESULTS = (By.ID, "searchResults")

    def is_search_field_present(self):
        """Возвращает True, если поле поиска найдено на странице, иначе False."""
        elements = self.driver.find_elements(*self.SEARCH_INPUT)
        return len(elements) > 0
