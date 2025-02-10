import pytest
from pages.navigation_page import NavigationPage
from pages.login_page import LoginPage

# Фикстура для входа в систему и инициализации объекта NavigationPage


@pytest.fixture
def nav_page(driver, base_url):
    """
    Фикстура для выполнения входа в систему и возврата объекта NavigationPage.

    Шаги:
      1. Открыть базовый URL.
      2. Выполнить вход с использованием учетной записи "john".
      3. Вернуть объект NavigationPage для дальнейшего использования в тестах.
    """
    driver.get(base_url)
    login_page = LoginPage(driver)
    login_page.login("john", "demo")
    return NavigationPage(driver)


def test_welcome_message(driver, base_url):
    """
    Проверяет, что после входа в систему на странице отображается приветственное сообщение "Welcome".
    """
    driver.get(base_url)
    login_page = LoginPage(driver)
    login_page.login("john", "demo")
    assert "Welcome" in driver.page_source, "Приветственное сообщение не отображается."

# Параметризированный тест для проверки навигационных ссылок.


@pytest.mark.parametrize("link_text, expected_text", [
    ("Open New Account", "Open New Account"),
    ("Accounts Overview", "Accounts Overview"),
    ("Transfer Funds", "Transfer Funds"),
    ("Bill Pay", "Bill Pay"),
    ("Find Transactions", "Find Transactions"),
    ("Update Contact Info", "Update Contact Info"),
    ("Request Loan", "Request Loan"),
    ("Log Out", "Customer Login")
])
def test_navigation_links(nav_page, driver, link_text, expected_text):
    """
    Тест переходит по каждой навигационной ссылке и проверяет, что после перехода
    на странице отображается ожидаемый текст.

    :param nav_page: Объект NavigationPage, предоставляемый фикстурой, после входа в систему.
    :param link_text: Текст ссылки, по которой происходит навигация.
    :param expected_text: Ожидаемый текст на целевой странице после навигации.
    """
    nav_page.navigate_to(link_text)
    assert expected_text in driver.page_source, (
        f"Страница '{link_text}' не отображается как ожидалось. Ожидается наличие '{expected_text}'."
    )
