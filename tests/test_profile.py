import pytest
from pages.profile_page import ProfileService
from pages.login_page import LoginService


@pytest.fixture
def profile_service(driver, base_url):
    """
    Фикстура для входа в систему и перехода на страницу обновления профиля.

    Выполняет следующие шаги:
      1. Открывает базовый URL.
      2. Выполняет вход под учетной записью "john" через LoginService.
      3. Переходит на страницу обновления профиля.

    :return: Сервисный объект ProfileService для дальнейших действий в тестах.
    """
    driver.get(base_url)
    login_service = LoginService(driver)
    login_service.login("john", "demo")
    driver.get(f"{base_url}/updateprofile.htm")
    return ProfileService(driver)


def test_update_profile(profile_service, driver):
    """
    Тест проверяет, что при обновлении профиля (например, изменении номера телефона)
    система корректно обрабатывает ошибку.

    В данном тестовом сценарии обновляется номер телефона на "555-0000", после чего
    ожидается, что в URL или в исходном коде страницы появится слово "error",
    что свидетельствует о возникновении ошибки.
    """
    # Обновляем номер телефона через сервисный объект ProfileService
    profile_service.update_phone_number("555-0000")

    # Получаем текущий URL и исходный код страницы для проверки наличия ошибки
    current_url = driver.current_url.lower()
    page_source = driver.page_source.lower()

    # Проверяем, что слово "error" присутствует либо в URL, либо в содержимом страницы.
    assert "error" in current_url or "error" in page_source, (
        "Ожидалась страница ошибки после обновления номера, но она не была отображена."
    )
