import pytest
from pages.account_overview_page import AccountOverviewPage
from pages.login_page import LoginPage


@pytest.fixture
def account_overview(driver, base_url):
    """
    Фикстура для входа в систему и получения объекта AccountOverviewPage.

    Шаги:
      1. Переход на базовый URL (эта логика реализована здесь, а не в тесте).
      2. Выполнение входа в систему с использованием корректных учетных данных ("john"/"demo").
      3. Возвращает объект AccountOverviewPage для дальнейшего использования в тестах.
    """
    driver.get(base_url)
    login_page = LoginPage(driver)
    login_page.login("john", "demo")
    return AccountOverviewPage(driver)


def test_account_overview_displayed(account_overview):
    """
    Проверяет, что страница обзора аккаунтов отображается корректно.

    Ожидается, что после входа в систему на странице будет найден заголовок раздела "Accounts Overview".
    """
    assert account_overview.is_account_overview_displayed(
    ), "Account Overview is not displayed."


def test_view_transaction_history(account_overview, driver):
    """
    Проверяет, что после запроса истории транзакций для аккаунта с номером "13344"
    отображается страница с текстом 'Account Activity'.
    """
    # Переход на страницу истории транзакций для аккаунта "13344"
    account_overview.view_transaction_history("13344")
    # Проверка, что на странице присутствует ожидаемый текст
    assert "Account Activity" in driver.page_source, "Transaction history is not displayed."
