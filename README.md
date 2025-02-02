Parabank Project
Этот проект содержит автотесты для сайта parabank.parasoft.com с использованием Selenium, pytest и методологии Page Object Model (POM). Проект также включает поддержку Docker и CI/CD (GitHub Actions).

Зависимости
Проект использует следующие библиотеки:
Selenium
pytest
pytest-xdist (для параллельного запуска тестов)
pytest-html (для генерации HTML отчётов)
allure-pytest (для Allure отчётов)
webdriver-manager (опционально, для автоматического управления драйвером)

Чтобы установить все зависимости, выполните:
pip install -r requirements.txt

Запуск тестов
Локально
Для запуска тестов с генерацией HTML отчёта:
pytest --html=report.html

Для запуска тестов с Allure отчётом:
pytest --alluredir=allure-results
allure serve allure-results

Через Docker
Соберите Docker образ:
docker build -t parabank_project .

Запустите тесты через Docker:
docker run --rm parabank_project

Или, если используете Docker Compose:
docker-compose up --build

CI/CD
В каталоге .github/workflows/ находится пример файла ci.yml, который автоматически запускает тесты при пушах в ветку main и пулл‑реквестах. 

Страница документации
Pages:
Каждый модуль в каталоге pages соответствует определённой странице сайта и реализует методы для взаимодействия с элементами страницы. Например, login_page.py содержит методы для входа в систему, а profile_page.py – для обновления профиля.

Tests:
Тесты в каталоге tests используют фикстуры из conftest.py и классы страниц из каталога pages для проверки функциональности сайта.

