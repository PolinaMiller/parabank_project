import pytest
from pages.search_page import SearchService


@pytest.fixture
def search_service(driver, base_url):
    """
    Фикстура для инициализации страницы поиска.

    Открывает базовый URL и возвращает сервисный объект SearchService,
    который использует Page Object SearchPage (построенный на основе PageElementary)
    для взаимодействия со страницей.
    """
    driver.get(base_url)
    return SearchService(driver)


def test_search_field_absence(search_service):
    """
    Тест проверяет, что поле поиска отсутствует на странице.

    Если метод is_search_field_present() возвращает True,
    тест завершится с ошибкой с сообщением:
    "Поле поиска обнаружено, хотя его быть не должно."
    """
    assert not search_service.is_search_field_present(
    ), "Поле поиска обнаружено, хотя его быть не должно."
