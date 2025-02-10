import pytest
from pages.bill_pay_page import BillPayPage
from pages.login_page import LoginPage

# Фикстура для инициализации страницы оплаты счетов.


@pytest.fixture
def bill_pay_page(driver, base_url):
    """
    Выполняет вход в систему и переходит на страницу оплаты счетов.

    Шаги:
      1. Открывает базовый URL.
      2. Выполняет вход под учетными данными "john"/"demo".
      3. Переходит на страницу "billpay.htm".
      4. Возвращает объект BillPayPage для дальнейших действий в тестах.
    """
    driver.get(base_url)
    login_page = LoginPage(driver)
    login_page.login("john", "demo")
    driver.get(f"{base_url}/billpay.htm")
    return BillPayPage(driver)

# Параметризированный тест для проверки различных сценариев оплаты счета.


@pytest.mark.parametrize(
    "payee_name, address, city, state, zip_code, phone, account, verify_account, amount, from_account, expected_result, error_msg",
    [
        # 1. Корректная оплата счета
        (
            "Electric Company", "456 Electric Ave", "City", "State", "67890",
            "555-6789", "987654", "987654", "200", "13344",
            "success", "Bill payment was not successful."
        ),
        # 2. Неверный получатель (пустое поле для payee_name)
        (
            "", "456 Electric Ave", "City", "State", "67890",
            "555-6789", "987654", "987654", "200", "13344",
            "payee_error", "Error message not displayed for invalid payee."
        ),
        # 3. Отрицательная сумма оплаты (система ожидаемо обрабатывает отрицательные суммы как корректные)
        (
            "Negative Bill", "456 Negative Ave", "City", "State", "22222",
            "555-2222", "111111", "111111", "-100", "13344",
            "success", "Оплата счета с отрицательной суммой не была выполнена успешно."
        ),
        # 4. Несоответствие номера счета и его подтверждения
        (
            "Mismatch Bill", "789 Mismatch Rd", "City", "State", "33333",
            "555-3333", "222222", "333333", "150", "13344",
            "mismatch_error", "Ошибка не отображается при несовпадении номеров счета в оплате счета."
        ),
        # 5. Нечисловое значение суммы оплаты
        (
            "NonNumeric Bill", "101 NonNumeric Blvd", "City", "State", "44444",
            "555-4444", "444444", "444444", "abc", "13344",
            "amount_invalid", "Ошибка не отображается при передаче нечислового значения суммы оплаты счета."
        ),
    ]
)
def test_bill_pay_scenarios(
    bill_pay_page,
    payee_name, address, city, state, zip_code, phone,
    account, verify_account, amount, from_account,
    expected_result, error_msg
):
    """
    Параметризированный тест для проверки различных сценариев оплаты счета:
      - Корректная оплата счета.
      - Оплата с пустым именем получателя (invalid payee).
      - Оплата с отрицательной суммой (ожидается, что система выполнит операцию успешно).
      - Оплата с несовпадающими номерами счета и подтверждения.
      - Оплата с нечисловым значением суммы.
    """
    bill_pay_page.pay_bill(
        payee_name, address, city, state, zip_code, phone,
        account, verify_account, amount, from_account
    )

    if expected_result == "success":
        assert bill_pay_page.is_payment_successful(), error_msg
    elif expected_result == "payee_error":
        assert bill_pay_page.is_payment_error_displayed(), error_msg
    elif expected_result == "mismatch_error":
        assert bill_pay_page.is_verify_account_mismatch_error_displayed(), error_msg
    elif expected_result == "amount_invalid":
        assert bill_pay_page.is_amount_invalid_error_displayed(), error_msg
