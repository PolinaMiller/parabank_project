import pytest
from pages.search_page import SearchPage


@pytest.fixture
def search_page(driver, base_url):
    """
    Фикстура для инициализации страницы поиска.
    Открывает базовый URL и возвращает объект SearchPage.
    """
    driver.get(base_url)
    return SearchPage(driver)


def test_search_field_absence(search_page):
    """
    Тест проверяет, что поле поиска отсутствует на странице.

    Если метод is_search_field_present() возвращает True,
    тест завершится с ошибкой с сообщением:
    "Поле поиска обнаружено, хотя его быть не должно."
    """
    assert not search_page.is_search_field_present(
    ), "Поле поиска обнаружено, хотя его быть не должно."
