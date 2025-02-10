import pytest
from pages.profile_page import ProfilePage
from pages.login_page import LoginPage


@pytest.fixture
def profile_page(driver, base_url):
    """
    Фикстура для входа в систему и перехода на страницу обновления профиля.

    Выполняет следующие шаги:
      1. Открывает базовый URL.
      2. Выполняет вход под учетной записью "john".
      3. Переходит на страницу обновления профиля.

    :return: Объект ProfilePage для дальнейших действий в тестах.
    """
    driver.get(base_url)
    login_page = LoginPage(driver)
    login_page.login("john", "demo")
    driver.get(f"{base_url}/updateprofile.htm")
    return ProfilePage(driver)


def test_update_profile(profile_page, driver):
    """
    Тест проверяет, что при обновлении профиля (например, изменении номера телефона)
    система обрабатывает ошибку корректно.

    В данном тестовом сценарии обновляется номер телефона на "555-0000", после чего
    ожидается, что страница либо в URL, либо в исходном коде будет содержать слово "error",
    что свидетельствует о возникновении ошибки.
    """
    # Обновляем номер телефона
    profile_page.update_phone_number("555-0000")

    # Вместо использования time.sleep мы полагаемся на ожидание внутри методов страниц,
    # однако, если требуется дополнительное время для обновления, можно заменить явное ожидание
    # на более точное ожидание (например, ожидание появления элемента ошибки).

    # Получаем текущий URL и исходный код страницы для проверки
    current_url = driver.current_url.lower()
    page_source = driver.page_source.lower()

    # Проверяем, что слово "error" присутствует либо в URL, либо в содержимом страницы.
    assert "error" in current_url or "error" in page_source, (
        "Ожидалась страница ошибки после обновления номера, но она не была отображена."
    )
