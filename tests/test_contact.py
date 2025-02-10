import pytest
from pages.contact_page import ContactService


@pytest.fixture
def contact_service(driver, base_url):
    """
    Фикстура для инициализации страницы "Contact Us" через сервисный объект.

    Шаги:
      1. Переход на страницу контактов.
      2. Возвращает объект ContactService для дальнейших действий в тестах.
    """
    driver.get(f"{base_url}/contact.htm")
    return ContactService(driver)


@pytest.mark.parametrize("email, message, error_message", [
    # Тестовый сценарий с корректными данными
    ("test@example.com", "This is a test message.",
     "Contact form submission failed."),
    # Тестовый сценарий с некорректным форматом email
    ("invalidemail", "Проверка неверного email.",
     "Контактная форма не приняла email с неверным форматом.")
])
def test_contact_form_submission(contact_service, email, message, error_message):
    """
    Тест проверяет отправку контактной формы как с корректными, так и с некорректными данными email.

    Ожидается, что система примет данные и отобразит сообщение об успешной отправке формы.
    """
    # Заполнение и отправка формы через сервисный объект
    contact_service.submit_contact_form(
        "Test User", email, "555-1234", message)
    # Проверка, что сообщение об успешной отправке формы отображается на странице
    assert contact_service.is_submission_successful(), error_message
