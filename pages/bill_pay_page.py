from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


class BillPayPageElementary(BasePage):
    """
    Элементарный объект страницы оплаты счета (Bill Pay).
    Содержит локаторы и базовые методы для непосредственного взаимодействия с элементами формы.
    """
    # Локаторы элементов формы оплаты
    PAYEE_NAME_INPUT = (By.XPATH, "//input[@name='payee.name']")
    ADDRESS_INPUT = (By.XPATH, "//input[@name='payee.address.street']")
    CITY_INPUT = (By.XPATH, "//input[@name='payee.address.city']")
    STATE_INPUT = (By.XPATH, "//input[@name='payee.address.state']")
    ZIP_CODE_INPUT = (By.XPATH, "//input[@name='payee.address.zipCode']")
    PHONE_INPUT = (By.XPATH, "//input[@name='payee.phoneNumber']")
    ACCOUNT_INPUT = (By.XPATH, "//input[@name='payee.accountNumber']")
    VERIFY_ACCOUNT_INPUT = (By.XPATH, "//input[@name='verifyAccount']")
    AMOUNT_INPUT = (By.XPATH, "//input[@name='amount']")
    FROM_ACCOUNT_SELECT = (By.XPATH, "//select[@name='fromAccountId']")
    SEND_PAYMENT_BUTTON = (
        By.XPATH, "//div[@id='billpayForm']//input[@value='Send Payment']")

    # Локаторы сообщений
    SUCCESS_MESSAGE = (
        By.XPATH, "//h1[contains(text(),'Bill Payment Complete')]")
    ERROR_MESSAGE = (
        By.XPATH, "//span[@id='validationModel-name' and contains(text(),'Payee name is required')]")
    VERIFY_ACCOUNT_MISMATCH_ERROR = (
        By.XPATH, "//span[@id='validationModel-verifyAccount-mismatch' and contains(text(),'The account numbers do not match')]"
    )
    AMOUNT_INVALID_ERROR = (
        By.XPATH, "//span[@id='validationModel-amount-invalid' and contains(text(),'Please enter a valid amount')]"
    )

    def clear_and_send_keys(self, locator: tuple, text: str) -> None:
        """
        Очищает найденное поле и вводит в него заданный текст.

        :param locator: Кортеж с локатором элемента.
        :param text: Текст для ввода.
        """
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def enter_payee_name(self, payee_name: str) -> None:
        self.clear_and_send_keys(self.PAYEE_NAME_INPUT, payee_name)

    def enter_address(self, address: str) -> None:
        self.clear_and_send_keys(self.ADDRESS_INPUT, address)

    def enter_city(self, city: str) -> None:
        self.clear_and_send_keys(self.CITY_INPUT, city)

    def enter_state(self, state: str) -> None:
        self.clear_and_send_keys(self.STATE_INPUT, state)

    def enter_zip_code(self, zip_code: str) -> None:
        self.clear_and_send_keys(self.ZIP_CODE_INPUT, zip_code)

    def enter_phone(self, phone: str) -> None:
        self.clear_and_send_keys(self.PHONE_INPUT, phone)

    def enter_account(self, account: str) -> None:
        self.clear_and_send_keys(self.ACCOUNT_INPUT, account)

    def enter_verify_account(self, verify_account: str) -> None:
        self.clear_and_send_keys(self.VERIFY_ACCOUNT_INPUT, verify_account)

    def enter_amount(self, amount: str) -> None:
        self.clear_and_send_keys(self.AMOUNT_INPUT, amount)

    def select_from_account(self, from_account: str) -> None:
        """
        Выбирает исходный счет из выпадающего списка по значению.

        :param from_account: Значение атрибута value для выбора счета.
        """
        select_element = self.find_element(self.FROM_ACCOUNT_SELECT)
        select = Select(select_element)
        select.select_by_value(from_account)

    def click_send_payment(self) -> None:
        """Нажимает на кнопку отправки платежа."""
        self.click(self.SEND_PAYMENT_BUTTON)

    def is_element_visible(self, locator: tuple, timeout: int) -> bool:
        """
        Вспомогательный метод для проверки появления элемента на странице.

        :param locator: Локатор элемента.
        :param timeout: Время ожидания появления элемента.
        :return: True, если элемент найден, иначе False.
        """
        try:
            self.wait_for_element(locator, timeout=timeout)
            return True
        except Exception:
            return False

    def wait_for_success_message(self, timeout: int = 15) -> bool:
        return self.is_element_visible(self.SUCCESS_MESSAGE, timeout)

    def wait_for_error_message(self, timeout: int = 15) -> bool:
        return self.is_element_visible(self.ERROR_MESSAGE, timeout)

    def wait_for_verify_account_mismatch_error(self, timeout: int = 15) -> bool:
        return self.is_element_visible(self.VERIFY_ACCOUNT_MISMATCH_ERROR, timeout)

    def wait_for_amount_invalid_error(self, timeout: int = 15) -> bool:
        return self.is_element_visible(self.AMOUNT_INVALID_ERROR, timeout)


class BillPayPage(BillPayPageElementary):
    """
    Page Object для страницы оплаты счета.
    Объединяет элементарные методы в высокоуровневые операции для заполнения и отправки формы оплаты.
    """

    def pay_bill(self,
                 payee_name: str,
                 address: str,
                 city: str,
                 state: str,
                 zip_code: str,
                 phone: str,
                 account: str,
                 verify_account: str,
                 amount: str,
                 from_account: str) -> None:
        """
        Заполняет форму оплаты счета и отправляет её.

        Шаги:
          1. Заполняет поля формы значениями, переданными в параметрах.
          2. Выбирает исходный счет из выпадающего списка.
          3. Отправляет форму оплаты.

        :param payee_name: Название получателя оплаты.
        :param address: Адрес получателя.
        :param city: Город получателя.
          :param state: Штат получателя.
        :param zip_code: Почтовый индекс получателя.
        :param phone: Телефон получателя.
        :param account: Номер счета получателя.
        :param verify_account: Подтверждение номера счета получателя.
        :param amount: Сумма оплаты.
        :param from_account: Номер счета, с которого будет списана сумма.
        """
        self.enter_payee_name(payee_name)
        self.enter_address(address)
        self.enter_city(city)
        self.enter_state(state)
        self.enter_zip_code(zip_code)
        self.enter_phone(phone)
        self.enter_account(account)
        self.enter_verify_account(verify_account)
        self.enter_amount(amount)
        self.select_from_account(from_account)
        self.click_send_payment()

    def is_payment_successful(self) -> bool:
        """
        Проверяет, что сообщение об успешной оплате счета отображается на странице.

        :return: True, если сообщение найдено в течение 15 секунд, иначе False.
        """
        return self.wait_for_success_message(timeout=15)

    def is_payment_error_displayed(self) -> bool:
        """
        Проверяет, что сообщение об ошибке оплаты (например, отсутствие имени получателя) отображается на странице.

        :return: True, если сообщение найдено, иначе False.
        """
        return self.wait_for_error_message(timeout=15)

    def is_verify_account_mismatch_error_displayed(self) -> bool:
        """
        Проверяет, что сообщение о несовпадении номеров счета отображается на странице.

        :return: True, если сообщение найдено, иначе False.
        """
        return self.wait_for_verify_account_mismatch_error(timeout=15)

    def is_amount_invalid_error_displayed(self) -> bool:
        """
        Проверяет, что сообщение о неверном формате суммы оплаты отображается на странице.

        :return: True, если сообщение найдено, иначе False.
        """
        return self.wait_for_amount_invalid_error(timeout=15)


class BillPayService:
    """
    Сервисный объект для работы с оплатой счета.
    Инкапсулирует бизнес-логику оплаты, используя Page Object BillPayPage.
    """

    def __init__(self, driver):
        self.page = BillPayPage(driver)

    def pay_bill(self,
                 payee_name: str,
                 address: str,
                 city: str,
                 state: str,
                 zip_code: str,
                 phone: str,
                 account: str,
                 verify_account: str,
                 amount: str,
                 from_account: str) -> None:
        """
        Выполняет оплату счета через Page Object.

        :param payee_name: Название получателя оплаты.
        :param address: Адрес получателя.
        :param city: Город получателя.
        :param state: Штат получателя.
        :param zip_code: Почтовый индекс получателя.
        :param phone: Телефон получателя.
        :param account: Номер счета получателя.
        :param verify_account: Подтверждение номера счета.
        :param amount: Сумма оплаты.
        :param from_account: Номер счета для списания оплаты.
        """
        self.page.pay_bill(payee_name, address, city, state, zip_code,
                           phone, account, verify_account, amount, from_account)

    def is_payment_successful(self) -> bool:
        """
        Проверяет успешность оплаты.

        :return: True, если оплата выполнена успешно, иначе False.
        """
        return self.page.is_payment_successful()

    def is_payment_error_displayed(self) -> bool:
        """
        Проверяет, отображается ли сообщение об ошибке оплаты.

        :return: True, если сообщение об ошибке найдено, иначе False.
        """
        return self.page.is_payment_error_displayed()

    def is_verify_account_mismatch_error_displayed(self) -> bool:
        """
        Проверяет, отображается ли сообщение о несовпадении номеров счета.

        :return: True, если сообщение найдено, иначе False.
        """
        return self.page.is_verify_account_mismatch_error_displayed()

    def is_amount_invalid_error_displayed(self) -> bool:
        """
        Проверяет, отображается ли сообщение о неверном формате суммы оплаты.

        :return: True, если сообщение найдено, иначе False.
        """
        return self.page.is_amount_invalid_error_displayed()
