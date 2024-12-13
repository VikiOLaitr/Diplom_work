import allure
from page.api_page import ApiPage

# Определите базовые данные
base_url = "https://web-gate.chitai-gorod.ru/api/v2/search/product"
token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL3VzZXItcmlnaHQiLCJzdWIiOjIxMjY4MTgzLCJpYXQiOjE3MzQxMTA1NDUsImV4cCI6MTczNDExNDE0NSwidHlwZSI6MjB9.xvZ62ytCy6HKGZWOpyiZinGI9CQJl6FwS3LwEA1Hi10"

# Инициализация объекта API
api_page = ApiPage(base_url, token)


@allure.epic("API Тестирование")
@allure.feature("Поиск книг")
@allure.title("Тестирование поиска книги по названию")
@allure.description("Проверка, что API возвращает книгу с ожидаемым названием")
def test_api_book_by_title():
    response = api_page.search_product("Таня Гроттер")

    # Вывод текста ответа и статус кода для отладки
    print("Ответ:", response.text)
    print("Статус код:", response.status_code)

    # Проверьте статус ответа
    assert response.status_code == 200, f"Тест провален: статус код {
        response.status_code}."

    expected_title = "Таня Гроттер"
    response_json = response.json()
    book_titles = api_page.extract_book_titles(response_json)

    assert any(expected_title.lower() in title.lower()
               for title in book_titles)
    f"Тест провален: название книги '{expected_title}' не найдено в ответе."


@allure.epic("API Тестирование")
@allure.feature("Поиск книг")
@allure.title("Тестирование поиска книги по автору")
@allure.description("Проверка, что API возвращает книги с ожидаемым автором.")
def test_api_book_by_author():
    response = api_page.search_product("Дмитрий Емец")

    print("Ответ:", response.text)
    print("Статус код:", response.status_code)

    assert response.status_code == 200, f"Тест провален: статус код {
        response.status_code}."

    expected_author = "Дмитрий Емец"
    response_json = response.json()
    book_authors = api_page.extract_book_authors(response_json)

    assert any(expected_author.lower()
               in author.lower() for author in book_authors), \
        f"Тест провален: автор '{expected_author}' не найден в ответе."


@allure.epic("API Тестирование")
@allure.feature("Поиск книг")
@allure.title("Тестирование поиска книги по автору на английском")
@allure.description("Проверка, что API возвращает книгу с "
                    "ожидаемым названием на английском.")
def test_api_author_in_english():
    response = api_page.search_product("Harry Potter")

    print("Ответ:", response.text)
    print("Статус код:", response.status_code)

    assert response.status_code == 200, f"Тест провален: статус код {
        response.status_code}."

    expected_title = "Harry Potter"
    response_json = response.json()
    book_titles = api_page.extract_book_titles(response_json)

    assert any(expected_title.lower()
               in title.lower() for title in book_titles), \
        f"Тест провален: название книги '{expected_title}' не найдено в ответе"


@allure.epic("API Тестирование")
@allure.feature("Поиск книг")
@allure.title("Тестирование поиска с недопустимой корейской фразой")
@allure.description("Проверка, что API возвращает ошибку "
                    "при поиске с недопустимой корейской фразой.")
def test_api_Korea():
    response = api_page.search_product("오만과 편견")

    print("Ответ:", response.text)
    print("Статус код:", response.status_code)

    assert response.status_code == 422, f"Тест провален: статус код {
        response.status_code}."

    response_json = response.json()
    error = response_json.get('errors', [{}])[0]
    assert error.get('status') == "422", "Тест провален: "
    "ожидаемый статус не найден в ответе."
    assert error.get('title') == "Недопустимая поисковая фраза", "Тест "
    "провален: сообщение об ошибке неверно."


@allure.epic("API Тестирование")
@allure.feature("Поиск книг")
@allure.title("Тестирование поиска с пустым запросом")
@allure.description("Проверка, что API возвращает "
                    "ошибку при пустом поисковом запросе.")
def test_api_empty_search():
    response = api_page.search_product("")

    print("Ответ:", response.text)
    print("Статус код:", response.status_code)

    assert response.status_code == 400, f"Тест провален: статус код {
        response.status_code}."

    response_json = response.json()
    error = response_json.get('errors', [{}])[0]
    assert error.get('status') == "400", "Тест провален: ожидаемый статус "
    "не найден в ответе."
    assert error.get('title') == "Phrase обязательное поле", "Тест провален: "
    "сообщение об ошибке неверно."
