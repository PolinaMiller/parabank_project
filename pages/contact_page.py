from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class ContactPage(BasePage):
    NAME_INPUT = (By.XPATH, "//form[@id='contactForm']//input[@id='name']")
    EMAIL_INPUT = (By.XPATH, "//form[@id='contactForm']//input[@id='email']")
    PHONE_INPUT = (By.XPATH, "//form[@id='contactForm']//input[@id='phone']")
    MESSAGE_INPUT = (
        By.XPATH, "//form[@id='contactForm']//textarea[@id='message']")
    SEND_BUTTON = (
        By.XPATH, "//form[@id='contactForm']//input[@value='Send to Customer Care']")
    SUCCESS_MESSAGE = (
        By.XPATH, "//div[@id='rightPanel']//p[contains(text(),'A Customer Care Representative will be contacting you.')]")

    def submit_contact_form(self, name, email, phone, message):
        self.send_keys(self.NAME_INPUT, name)
        self.send_keys(self.EMAIL_INPUT, email)
        self.send_keys(self.PHONE_INPUT, phone)
        self.send_keys(self.MESSAGE_INPUT, message)
        self.click(self.SEND_BUTTON)

    def is_submission_successful(self):
        try:
            self.wait_for_element(self.SUCCESS_MESSAGE, timeout=15)
            return True
        except Exception:
            return False
