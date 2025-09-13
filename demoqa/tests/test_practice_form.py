import allure
from selene import browser

from demoqa.pages.practice_form_page import PracticeFormPage
from demoqa.data.users import UserData


@allure.title("Успешное заполнение формы")
def test_field_practice_form(setup_browser):
    """Передача кастомного браузера из фикстуры conftest"""
    browser = setup_browser


    """Инициализация экземпляров класса PracticeFormPage и UserData"""
    alexandra = UserData(
        "Alexandra",
        "Levina",
        "alexandralevina1@gmail.com",
        "Female",
        "8912345678",
        ("February", "2002", "17"),
        "Computer Science",
        ("Sports", "Reading", "Music"),
        "test_file.txt",
        "Россия, г.Москва, ул.Маршала Жукова 1",
        ("NCR", "Delhi"),
    )

    practice_form_page = PracticeFormPage()


    with allure.step("Открытие страницы с формой"):
        browser.open("https://demoqa.com/automation-practice-form")


    with allure.step("Заполнение формы"):
        browser.execute_script("window.scrollBy(0, 500)")
        practice_form_page.completing_practice_form_fields(alexandra)

    with allure.step("Проверка заполненной формы"):
        practice_form_page.should_completed_registration_form(alexandra)

    with allure.step("Закрытие модального окна"):
        practice_form_page.button_close.click()