from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class ContactPageElementary(BasePage):
    """
    Элементарный объект страницы "Contact Us".
    Содержит локаторы и базовые методы для непосредственного взаимодействия с элементами страницы.
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
        By.XPATH,
        "//div[@id='rightPanel']//p[contains(text(),'A Customer Care Representative will be contacting you.')]"
    )

    def enter_name(self, name: str) -> None:
        """Вводит имя в поле 'Name'."""
        self.send_keys(self.NAME_INPUT, name)

    def enter_email(self, email: str) -> None:
        """Вводит адрес электронной почты в поле 'Email'."""
        self.send_keys(self.EMAIL_INPUT, email)

    def enter_phone(self, phone: str) -> None:
        """Вводит номер телефона в поле 'Phone'."""
        self.send_keys(self.PHONE_INPUT, phone)

    def enter_message(self, message: str) -> None:
        """Вводит текст сообщения в поле 'Message'."""
        self.send_keys(self.MESSAGE_INPUT, message)

    def click_send(self) -> None:
        """Нажимает на кнопку 'Send to Customer Care'."""
        self.click(self.SEND_BUTTON)

    def is_element_visible(self, locator: tuple, timeout: int = 15) -> bool:
        """
        Проверяет, что элемент, заданный локатором, появляется на странице в течение указанного времени.

        :param locator: Локатор элемента (например, (By.XPATH, "..."))
        :param timeout: Максимальное время ожидания появления элемента (по умолчанию 15 секунд).
        :return: True, если элемент появляется, иначе False.
        """
        try:
            self.wait_for_element(locator, timeout=timeout)
            return True
        except Exception:
            return False


class ContactPage(ContactPageElementary):
    """
    Page Object для страницы "Contact Us".
    Объединяет элементарные методы в высокоуровневые операции для заполнения и отправки контактной формы,
    а также проверки успешной отправки.
    """

    def submit_contact_form(self, name: str, email: str, phone: str, message: str) -> None:
        """
        Заполняет и отправляет форму "Contact Us".

        Шаги:
          1. Вводит имя в поле "Name".
          2. Вводит адрес электронной почты в поле "Email".
          3. Вводит номер телефона в поле "Phone".
          4. Вводит текст сообщения в поле "Message".
          5. Нажимает на кнопку отправки формы.

        :param name: Имя отправителя.
        :param email: Адрес электронной почты отправителя.
        :param phone: Телефонный номер отправителя.
        :param message: Текст сообщения для отправки.
        """
        self.enter_name(name)
        self.enter_email(email)
        self.enter_phone(phone)
        self.enter_message(message)
        self.click_send()

    def is_submission_successful(self) -> bool:
        """
        Проверяет, что сообщение об успешной отправке формы отображается на странице.

        Ожидается, что после отправки формы появится сообщение:
        "A Customer Care Representative will be contacting you."

        :return: True, если сообщение об успехе найдено в течение 15 секунд, иначе False.
        """
        return self.is_element_visible(self.SUCCESS_MESSAGE, timeout=15)


class ContactService:
    """
    Сервисный объект для работы со страницей "Contact Us".
    Инкапсулирует бизнес-логику заполнения и отправки контактной формы,
    используя Page Object ContactPage.
    """

    def __init__(self, driver):
        self.page = ContactPage(driver)

    def submit_contact_form(self, name: str, email: str, phone: str, message: str) -> None:
        """
        Заполняет и отправляет форму контактов через Page Object.

        :param name: Имя отправителя.
        :param email: Адрес электронной почты отправителя.
        :param phone: Телефонный номер отправителя.
        :param message: Текст сообщения для отправки.
        """
        self.page.submit_contact_form(name, email, phone, message)

    def is_submission_successful(self) -> bool:
        """
        Проверяет успешность отправки контактной формы.

        :return: True, если сообщение об успешной отправке найдено, иначе False.
        """
        return self.page.is_submission_successful()
