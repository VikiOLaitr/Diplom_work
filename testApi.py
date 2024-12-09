import allure
from Page.ApiPage import ApiPage


@allure.epic("API Тестирование")
@allure.feature("Поиск книг")
@allure.title("Тестирование поиска книги по названию")
@allure.description("Проверка, что API возвращает книгу с ожидаемым названием")
def test_api_book_by_title():
    response = ApiPage.search_product("Таня Гроттер")

    # Вывод текста ответа и статус кода для отладки
    print("Ответ:", response.text)
    print("Статус код:", response.status_code)

    # Проверьте статус ответа
    assert response.status_code == 200, f"Тест провален: статус код {
        response.status_code}."

    expected_title = "Таня Гроттер"
    response_json = response.json()
    book_titles = ApiPage.extract_book_titles(response_json)

    assert any(expected_title.lower() in title.lower()
               for title in book_titles)
    f"Тест провален: название книги '{expected_title}' не найдено в ответе."


@allure.epic("API Тестирование")
@allure.feature("Поиск книг")
@allure.title("Тестирование поиска книги по автору")
@allure.description("Проверка, что API возвращает книги с ожидаемым автором.")
def test_api_book_by_author():
    response = ApiPage.search_product("Дмитрий Емец")

    print("Ответ:", response.text)
    print("Статус код:", response.status_code)

    assert response.status_code == 200, f"Тест провален: статус код {
        response.status_code}."

    expected_author = "Дмитрий Емец"
    response_json = response.json()
    book_authors = ApiPage.extract_book_authors(response_json)

    assert any(expected_author.lower()
               in author.lower() for author in book_authors), \
        f"Тест провален: автор '{expected_author}' не найден в ответе."


@allure.epic("API Тестирование")
@allure.feature("Поиск книг")
@allure.title("Тестирование поиска книги по названию на английском")
@allure.description("Проверка, что API возвращает книгу с "
                    "ожидаемым названием на английском.")
def test_api_name_in_english():
    response = ApiPage.search_product("Harry Potter")

    print("Ответ:", response.text)
    print("Статус код:", response.status_code)

    assert response.status_code == 200, f"Тест провален: статус код {
        response.status_code}."

    expected_title = "Harry Potter"
    response_json = response.json()
    book_titles = ApiPage.extract_book_titles(response_json)

    assert any(expected_title.lower()
               in title.lower() for title in book_titles), \
        f"Тест провален: название книги '{expected_title}' не найдено в ответе"


@allure.epic("API Тестирование")
@allure.feature("Поиск книг")
@allure.title("Тестирование поиска на корейском языке")
@allure.description("Проверка, что API возвращает ошибку "
                    "при поиске на корейском языке.")
def test_api_Korea():
    response = ApiPage.search_product("오만과 편견")

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
    response = ApiPage.search_product("")

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


@allure.epic("API Тестирование")
@allure.feature("Поиск книг")
@allure.title("Тестирование поиска с пробелами в запросе")
@allure.description("Проверка, что API возвращает "
                    "ошибку с пробелами в запросе.")
def test_api_spaces_search():
    response = ApiPage.search_product("     ")

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
