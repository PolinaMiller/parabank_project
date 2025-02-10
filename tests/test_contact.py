import pytest
from pages.contact_page import ContactPage


@pytest.fixture
def contact_page(driver, base_url):
    """
    Фикстура для инициализации страницы "Contact Us".

    Шаги:
      1. Переход на страницу контактов.
      2. Возвращает объект ContactPage для дальнейших действий в тестах.
    """
    driver.get(f"{base_url}/contact.htm")
    return ContactPage(driver)


@pytest.mark.parametrize("email, message, error_message", [
    # Тестовый сценарий с корректными данными
    ("test@example.com", "This is a test message.",
     "Contact form submission failed."),
    # Тестовый сценарий с некорректным форматом email
    ("invalidemail", "Проверка неверного email.",
     "Контактная форма не приняла email с неверным форматом.")
])
def test_contact_form_submission(contact_page, email, message, error_message):
    """
    Тест проверяет отправку контактной формы как с корректными, так и с некорректными данными email.

    Ожидается, что система примет данные и отобразит сообщение об успешной отправке формы.
    """
    # Заполнение и отправка формы обратной связи с указанными параметрами
    contact_page.submit_contact_form("Test User", email, "555-1234", message)
    # Проверяем, что сообщение об успешной отправке формы отображается на странице
    assert contact_page.is_submission_successful(), error_message
