import pytest
import allure
import logging
from selenium.webdriver.common.by import By
# Используем сервисный объект, а не прямой Page Object
from pages.bill_pay_page import BillPayService
from pages.login_page import LoginService

# Настройка логирования: вывод сообщений уровня INFO и выше.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@pytest.fixture
def bill_pay_service(driver, base_url):
    """
    Выполняет вход в систему и переходит на страницу оплаты счетов.

    Шаги:
      1. Открывает базовый URL.
      2. Выполняет вход под учетными данными "john"/"demo" через LoginService.
      3. Переходит на страницу "billpay.htm".
      4. Возвращает объект BillPayService для дальнейших действий в тестах.
    """
    with allure.step("Открыть базовый URL"):
        logger.info("Открытие базового URL: %s", base_url)
        driver.get(base_url)
    with allure.step("Выполнить вход под пользователем 'john'"):
        logger.info("Выполняется вход с учетными данными: john/demo")
        login_service = LoginService(driver)
        login_service.login("john", "demo")
    with allure.step("Перейти на страницу оплаты счетов"):
        page_url = f"{base_url}/billpay.htm"
        logger.info("Переход на страницу оплаты счетов: %s", page_url)
        driver.get(page_url)
    return BillPayService(driver)


@pytest.mark.parametrize(
    "payee_name, address, city, state, zip_code, phone, account, verify_account, amount, from_account, expected_result, error_msg",
    [
        # TC-7: Корректная оплата счета
        (
            "Electric Company", "456 Electric Ave", "City", "State", "67890",
            "555-6789", "987654", "987654", "200", "13344",
            "success", "Bill payment was not successful."
        ),
        # TC-8: Оплата с пустым полем получателя (Invalid Payee)
        (
            "", "456 Electric Ave", "City", "State", "67890",
            "555-6789", "987654", "987654", "200", "13344",
            "payee_error", "Error message not displayed for invalid payee."
        ),
        # TC-9: Оплата с отрицательной суммой
        (
            "Negative Bill", "456 Negative Ave", "City", "State", "22222",
            "555-2222", "111111", "111111", "-100", "13344",
            "success", "Оплата счета с отрицательной суммой не была выполнена успешно."
        ),
        # TC-10: Несоответствие номера счета и его подтверждения
        (
            "Mismatch Bill", "789 Mismatch Rd", "City", "State", "33333",
            "555-3333", "222222", "333333", "150", "13344",
            "mismatch_error", "Ошибка не отображается при несовпадении номеров счета в оплате счета."
        ),
        # TC-11: Оплата с нечисловым значением суммы
        (
            "NonNumeric Bill", "101 NonNumeric Blvd", "City", "State", "44444",
            "555-4444", "444444", "444444", "abc", "13344",
            "amount_invalid", "Ошибка не отображается при передаче нечислового значения суммы оплаты счета."
        ),
    ]
)
@allure.feature("Bill Pay")
@allure.story("Проверка сценариев оплаты счета")
def test_bill_pay_scenarios(
    bill_pay_service,
    payee_name, address, city, state, zip_code, phone,
    account, verify_account, amount, from_account,
    expected_result, error_msg
):
    """
    Параметризированный тест для проверки различных сценариев оплаты счета:
      - Корректная оплата счета.
      - Оплата с пустым именем получателя (Invalid Payee).
      - Оплата с отрицательной суммой.
      - Оплата с несовпадающими номерами счета и подтверждения.
      - Оплата с нечисловым значением суммы.
    """
    with allure.step("Заполнить форму оплаты счета"):
        logger.info(
            "Заполнение формы оплаты счета: payee_name='%s', address='%s', city='%s', state='%s', "
            "zip_code='%s', phone='%s', account='%s', verify_account='%s', amount='%s', from_account='%s'",
            payee_name, address, city, state, zip_code, phone, account, verify_account, amount, from_account
        )
        bill_pay_service.pay_bill(
            payee_name, address, city, state, zip_code, phone,
            account, verify_account, amount, from_account
        )
    with allure.step("Проверить результат оплаты"):
        if expected_result == "success":
            logger.info("Ожидается успешная оплата счета.")
            assert bill_pay_service.is_payment_successful(), error_msg
        elif expected_result == "payee_error":
            logger.info(
                "Ожидается отображение ошибки из-за пустого имени получателя.")
            assert bill_pay_service.is_payment_error_displayed(), error_msg
        elif expected_result == "mismatch_error":
            logger.info(
                "Ожидается отображение ошибки из-за несовпадения номеров счета.")
            assert bill_pay_service.is_verify_account_mismatch_error_displayed(), error_msg
        elif expected_result == "amount_invalid":
            logger.info(
                "Ожидается отображение ошибки из-за нечислового значения суммы оплаты.")
            assert bill_pay_service.is_amount_invalid_error_displayed(), error_msg
