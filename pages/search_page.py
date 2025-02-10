from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class SearchPageElementary(BasePage):
    """
    Элементарный объект страницы поиска.
    Содержит локаторы и базовые методы для доступа к элементам страницы.
    """
    SEARCH_INPUT = (By.XPATH, "//*[@id='search']")
    RESULTS = (By.ID, "searchResults")

    def get_search_input_elements(self):
        """
        Возвращает список найденных элементов поля поиска.

        Returns:
            list: Список найденных элементов по локатору SEARCH_INPUT.
        """
        return self.driver.find_elements(*self.SEARCH_INPUT)

    def get_results_elements(self):
        """
        Возвращает список найденных элементов результатов поиска.

        Returns:
            list: Список найденных элементов по локатору RESULTS.
        """
        return self.driver.find_elements(*self.RESULTS)


class SearchService:
    """
    Сервисный объект для работы со страницей поиска.
    Инкапсулирует бизнес-логику, используя элементарный объект страницы.
    """
    # Добавляем локатор RESULTS в сервис, чтобы тесты могли к нему обращаться.
    RESULTS = SearchPageElementary.RESULTS

    def __init__(self, driver):
        self.page = SearchPageElementary(driver)

    def is_search_field_present(self):
        """
        Проверяет, присутствует ли на странице поле поиска.

        Returns:
            bool: True, если найден хотя бы один элемент по локатору SEARCH_INPUT, иначе False.
        """
        elements = self.page.get_search_input_elements()
        return len(elements) > 0
