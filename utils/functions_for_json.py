from src.JSON_saver import JsonSaver
import json
from typing import List


def add_vacancies_to_json_file(file_name: str, vacancies_list: List) -> None:
    """
    функция для добавления списка вакансий в JSON
    """
    with open(file_name, 'w', encoding='utf-8') as file:
        data = [job.to_dict() for job in vacancies_list]
        json.dump(data, file, ensure_ascii=False, indent=2)


def remove_vacancies_from_json_file(file_name: str, criteria: str):
    job_saver = JsonSaver(file_name)

    try:
        with open(file_name, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        print("Файл не найден.")
        return

    for vacancy in data:
        # проверкаЮ содержит ли хотя бы одно поле критерий
        if any(criteria.lower() in str(value).lower() for value in vacancy.values()):
            job_saver.remove_job(vacancy)


def get_nessesary_vacancies(file_name: str, criteria_input: str) -> None:
    """
    функция для отбора вакансий по хапросу
    """
    job_saver = JsonSaver(file_name)
    criteria_list = criteria_input.strip().split()
    matching_jobs = job_saver.get_job(criteria_list)

    for vacancy in matching_jobs:
        print_vacancy_info(vacancy)


def print_vacancy_info(vacancy: dict) -> None:
    """
    функция для вывода краткой информации о вакансиях
    """
    title = vacancy["title"]
    url = vacancy["url"]
    salary_data = vacancy["salary_data"]
    description = vacancy["description"]

    if salary_data is not None:
        from_salary = salary_data.get("from")
        to_salary = salary_data.get("to")
        currency = salary_data.get("currency")

        if (from_salary is None or from_salary == 0) and (to_salary is None or to_salary == 0):
            salary_info = "зарплата не указана"
        elif (from_salary is None or from_salary == 0) and (to_salary is not None and to_salary != 0):
            salary_info = f"зарплата до {to_salary} {currency}"
        elif (from_salary is not None and from_salary != 0) and (to_salary is None or to_salary == 0):
            salary_info = f"зарплата от {from_salary} {currency}"
        elif (from_salary is not None and from_salary != 0) and (to_salary is not None and to_salary != 0):
            salary_info = f"зарплата от {from_salary} до {to_salary} {currency}"
    else:
        salary_info = "зарплата не указана"

    print(f"Вакансия - {title}, {salary_info}, подробная информация - {url}\n")
