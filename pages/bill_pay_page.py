from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


class BillPayPage(BasePage):
    """
    Класс BillPayPage предоставляет методы для работы с формой оплаты счета.
    Он инкапсулирует действия по заполнению и отправке формы, а также методы проверки результатов оплаты.
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

    # Локаторы для сообщений об успешной оплате и ошибок
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
          3. Отправляет форму оплаты, кликая по кнопке "Send Payment".

        :param payee_name: Название получателя оплаты.
        :param address: Адрес получателя.
        :param city: Город получателя.
        :param state: Штат получателя.
        :param zip_code: Почтовый индекс получателя.
        :param phone: Номер телефона получателя.
        :param account: Номер счета получателя.
        :param verify_account: Подтверждение номера счета получателя.
        :param amount: Сумма оплаты.
        :param from_account: Номер счета, с которого будет списана сумма.
        """
        self.send_keys(self.PAYEE_NAME_INPUT, payee_name)
        self.send_keys(self.ADDRESS_INPUT, address)
        self.send_keys(self.CITY_INPUT, city)
        self.send_keys(self.STATE_INPUT, state)
        self.send_keys(self.ZIP_CODE_INPUT, zip_code)
        self.send_keys(self.PHONE_INPUT, phone)
        self.send_keys(self.ACCOUNT_INPUT, account)
        self.send_keys(self.VERIFY_ACCOUNT_INPUT, verify_account)
        self.send_keys(self.AMOUNT_INPUT, amount)

        # Выбираем исходный счет из выпадающего списка
        from_select = Select(self.find_element(self.FROM_ACCOUNT_SELECT))
        from_select.select_by_value(from_account)

        # Отправляем форму оплаты, кликая по кнопке
        self.click(self.SEND_PAYMENT_BUTTON)

    def is_payment_successful(self) -> bool:
        """
        Проверяет, что сообщение об успешной оплате счета отображается на странице.

        :return: True, если сообщение найдено в течение 15 секунд; иначе, False.
        """
        try:
            self.wait_for_element(self.SUCCESS_MESSAGE, timeout=15)
            return True
        except Exception:
            return False

    def is_payment_error_displayed(self) -> bool:
        """
        Проверяет, что сообщение об ошибке (например, отсутствие имени получателя) отображается на странице.

        :return: True, если сообщение об ошибке найдено в течение 15 секунд; иначе, False.
        """
        try:
            self.wait_for_element(self.ERROR_MESSAGE, timeout=15)
            return True
        except Exception:
            return False

    def is_verify_account_mismatch_error_displayed(self) -> bool:
        """
        Проверяет, что сообщение об ошибке несовпадения номеров счета отображается на странице.

        :return: True, если сообщение найдено; иначе, False.
        """
        try:
            self.wait_for_element(
                self.VERIFY_ACCOUNT_MISMATCH_ERROR, timeout=15)
            return True
        except Exception:
            return False

    def is_amount_invalid_error_displayed(self) -> bool:
        """
        Проверяет, что сообщение об ошибке неверного формата суммы оплаты отображается на странице.

        :return: True, если сообщение найдено; иначе, False.
        """
        try:
            self.wait_for_element(self.AMOUNT_INVALID_ERROR, timeout=15)
            return True
        except Exception:
            return False
