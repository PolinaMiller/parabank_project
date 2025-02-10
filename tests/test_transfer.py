import pytest
from pages.funds_transfer_page import FundsTransferService
from pages.login_page import LoginService

# Фикстура для входа в систему и перехода на страницу перевода средств через сервисные объекты.


@pytest.fixture
def transfer_service(driver, base_url):
    # Открываем главную страницу приложения
    driver.get(base_url)

    # Используем сервисный объект для входа в систему
    login_service = LoginService(driver)
    login_service.login("john", "demo")

    # Переходим на страницу перевода средств
    driver.get(f"{base_url}/transfer.htm")

    # Возвращаем сервисный объект страницы перевода средств для дальнейшего использования в тестах
    return FundsTransferService(driver)

# Параметризованный тест для проверки перевода средств.
# Используются два набора данных:
# 1. Корректная сумма перевода ("100")
# 2. Сумма, превышающая доступный баланс ("1000000"), при которой система всё равно должна инициировать перевод


@pytest.mark.parametrize("amount, error_message", [
    ("100", "Funds transfer was not successful."),
    ("1000000", "Funds transfer was not successful, even though insufficient balance scenario is allowed.")
])
def test_funds_transfer(driver, base_url, transfer_service, amount, error_message):
    # Инициируем перевод средств с заданной суммой,
    # где "13344" — номер счета списания и зачисления.
    transfer_service.transfer_funds(amount, "13344", "13344")

    # Проверяем, что перевод средств выполнен успешно.
    assert transfer_service.is_transfer_successful(), error_message
