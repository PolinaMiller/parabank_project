from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class ContactPage(BasePage):
    """
    Класс ContactPage реализует функциональность страницы "Contact Us".
    Он предоставляет методы для заполнения и отправки контактной формы,
    а также для проверки успешной отправки формы.
    """

    # Локаторы элементов страницы "Contact Us"
    NAME_INPUT = (By.XPATH, "//form[@id='contactForm']//input[@id='name']")
    EMAIL_INPUT = (By.XPATH, "//form[@id='contactForm']//input[@id='email']")
    PHONE_INPUT = (By.XPATH, "//form[@id='contactForm']//input[@id='phone']")
    MESSAGE_INPUT = (
        By.XPATH, "//form[@id='contactForm']//textarea[@id='message']")
    SEND_BUTTON = (
        By.XPATH, "//form[@id='contactForm']//input[@value='Send to Customer Care']")
    SUCCESS_MESSAGE = (
        By.XPATH, "//div[@id='rightPanel']//p[contains(text(),'A Customer Care Representative will be contacting you.')]")

    def submit_contact_form(self, name: str, email: str, phone: str, message: str) -> None:
        """
        Заполняет и отправляет форму контактов.

        Шаги:
          1. Вводит имя отправителя в поле "Name".
          2. Вводит адрес электронной почты в поле "Email".
          3. Вводит номер телефона в поле "Phone".
          4. Вводит текст сообщения в поле "Message".
          5. Отправляет форму, кликая по кнопке "Send to Customer Care".

        :param name: Имя отправителя.
        :param email: Адрес электронной почты отправителя.
        :param phone: Телефонный номер отправителя.
        :param message: Текст сообщения для отправки.
        """
        self.send_keys(self.NAME_INPUT, name)
        self.send_keys(self.EMAIL_INPUT, email)
        self.send_keys(self.PHONE_INPUT, phone)
        self.send_keys(self.MESSAGE_INPUT, message)
        self.click(self.SEND_BUTTON)

    def _is_element_visible(self, locator: tuple, timeout: int = 15) -> bool:
        """
        Вспомогательный метод для проверки видимости элемента на странице.

        :param locator: Локатор элемента, например, (By.XPATH, "...")
        :param timeout: Максимальное время ожидания появления элемента (по умолчанию 15 секунд).
        :return: True, если элемент появляется в течение timeout секунд, иначе False.
        """
        try:
            self.wait_for_element(locator, timeout=timeout)
            return True
        except Exception:
            return False

    def is_submission_successful(self) -> bool:
        """
        Проверяет, что сообщение об успешной отправке формы контактов отображается на странице.

        Ожидается, что после отправки формы появится сообщение, подтверждающее, что 
        "A Customer Care Representative will be contacting you."

        :return: True, если сообщение об успехе найдено в течение 15 секунд, иначе False.
        """
        return self._is_element_visible(self.SUCCESS_MESSAGE, timeout=15)
