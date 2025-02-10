import pytest
from pages.funds_transfer_page import FundsTransferPage
from pages.login_page import LoginPage

# Фикстура для входа в систему и перехода на страницу перевода средств.


@pytest.fixture
def transfer_page(driver, base_url):
    # Открываем главную страницу приложения
    driver.get(base_url)
    # Создаем объект страницы входа и выполняем вход с корректными учетными данными
    login_page = LoginPage(driver)
    login_page.login("john", "demo")
    # Переходим на страницу перевода средств
    driver.get(f"{base_url}/transfer.htm")
    # Возвращаем объект страницы перевода средств для дальнейшего использования в тестах
    return FundsTransferPage(driver)

# Параметризованный тест для проверки перевода средств.
# Используются два набора данных:
# 1. Корректная сумма перевода ("100")
# 2. Сумма, превышающая доступный баланс ("1000000"), при которой система всё равно должна инициировать перевод


@pytest.mark.parametrize("amount, error_message", [
    ("100", "Funds transfer was not successful."),
    ("1000000", "Funds transfer was not successful, even though insufficient balance scenario is allowed.")
])
def test_funds_transfer(driver, base_url, transfer_page, amount, error_message):
    # Инициируем перевод средств с заданной суммой,
    # где "13344" — номер счета списания и зачисления.
    transfer_page.transfer_funds(amount, "13344", "13344")
    # Проверяем, что перевод средств был выполнен успешно.
    assert transfer_page.is_transfer_successful(), error_message
