from pages.bill_pay_page import BillPayPage
from pages.login_page import LoginPage


def test_bill_pay_success(driver, base_url):
    driver.get(base_url)
    login_page = LoginPage(driver)
    login_page.login("john", "demo")
    driver.get(f"{base_url}/billpay.htm")
    bill_pay = BillPayPage(driver)
    bill_pay.pay_bill("Electric Company", "456 Electric Ave", "City", "State", "67890",
                      "555-6789", "987654", "987654", "200", "13344")
    assert bill_pay.is_payment_successful(), "Bill payment was not successful."


def test_bill_pay_invalid_payee(driver, base_url):
    driver.get(base_url)
    login_page = LoginPage(driver)
    login_page.login("john", "demo")
    driver.get(f"{base_url}/billpay.htm")
    bill_pay = BillPayPage(driver)
    bill_pay.pay_bill("", "456 Electric Ave", "City", "State", "67890",
                      "555-6789", "987654", "987654", "200", "13344")
    assert bill_pay.is_payment_error_displayed(
    ), "Error message not displayed for invalid payee."


def test_bill_pay_negative_amount(driver, base_url):
    driver.get(base_url)
    login_page = LoginPage(driver)
    login_page.login("john", "demo")
    driver.get(f"{base_url}/billpay.htm")
    bill_pay = BillPayPage(driver)
    bill_pay.pay_bill(
        payee_name="Negative Bill",
        address="456 Negative Ave",
        city="City",
        state="State",
        zip_code="22222",
        phone="555-2222",
        account="111111",
        verify_account="111111",
        amount="-100",
        from_account="13344"
    )
    assert bill_pay.is_payment_successful(
    ), "Оплата счета с отрицательной суммой не была выполнена успешно."


def test_bill_pay_mismatched_verify_account(driver, base_url):
    driver.get(base_url)
    login_page = LoginPage(driver)
    login_page.login("john", "demo")
    driver.get(f"{base_url}/billpay.htm")
    bill_pay = BillPayPage(driver)
    bill_pay.pay_bill(
        payee_name="Mismatch Bill",
        address="789 Mismatch Rd",
        city="City",
        state="State",
        zip_code="33333",
        phone="555-3333",
        account="222222",
        verify_account="333333",
        amount="150",
        from_account="13344"
    )
    assert bill_pay.is_verify_account_mismatch_error_displayed(), \
        "Ошибка не отображается при несовпадении номеров счета в оплате счета."


def test_bill_pay_non_numeric_amount(driver, base_url):
    driver.get(base_url)
    login_page = LoginPage(driver)
    login_page.login("john", "demo")
    driver.get(f"{base_url}/billpay.htm")
    bill_pay = BillPayPage(driver)
    bill_pay.pay_bill(
        payee_name="NonNumeric Bill",
        address="101 NonNumeric Blvd",
        city="City",
        state="State",
        zip_code="44444",
        phone="555-4444",
        account="444444",
        verify_account="444444",
        amount="abc",
        from_account="13344"
    )
    assert bill_pay.is_amount_invalid_error_displayed(), \
        "Ошибка не отображается при передаче нечислового значения суммы оплаты счета."
