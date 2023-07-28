import json
import sys
from utils.parsers_from_hh_sj import all_from_hh, all_from_sj
from utils.filter_functions import filter_vacancies_by_keywords, filter_vacancies_by_salary
from utils.get_keywords import get_keywords_from_user
from utils.functions_for_json import remove_vacancies_from_json_file, add_vacancies_to_json_file, get_nessesary_vacancies, print_vacancy_info
from typing import List

FILE_NAME = "vacancies.json"


def process_action(vacancies_list: List, action: str, file_name: str, user_platform: str) -> None:
    """
    функция для обработки вызванного пользователем действия
    """
    if action == "1":
        if user_platform == "1":

            for job in vacancies_list:
                formatted_salary = job.format_salary()
                job_description = job.get_description()
                print(f"{job.title}\n{job.url}\n{formatted_salary}\n{job_description}\n")

                add_vacancies_to_json_file(file_name, vacancies_list)

        elif user_platform == "2":
            for job in vacancies_list:
                formatted_salary = job.format_salary()
                print(f"{job.title}\n{job.url}\n{formatted_salary}\n{job.description}\n")

                add_vacancies_to_json_file(file_name, vacancies_list)

    elif action == "2":
        if user_platform == "1":
            keywords_hh = get_keywords_from_user()
            filtered_vacancies_hh = filter_vacancies_by_keywords(vacancies_list, keywords_hh)

            if not filtered_vacancies_hh:
                print("Нет вакансий, соответствующих заданным критериям.")

            else:

                for job in filtered_vacancies_hh:
                    formatted_salary = job.format_salary()
                    job_description = job.get_description()
                    print(f"{job.title}\n{job.url}\n{formatted_salary}\n{job_description}\n")
                    add_vacancies_to_json_file(file_name, filtered_vacancies_hh)

        elif user_platform == "2":
            keywords_sj = get_keywords_from_user()
            filtered_vacancies_sj = filter_vacancies_by_keywords(vacancies_list, keywords_sj)

            if not filtered_vacancies_sj:
                print("Нет вакансий, соответствующих заданным критериям.")

            else:

                for job in filtered_vacancies_sj:
                    formatted_salary = job.format_salary()
                    print(f"{job.title}\n{job.url}\n{formatted_salary}\n{job.description}\n")

                    add_vacancies_to_json_file(file_name, filtered_vacancies_sj)

    elif action == "3":
        if user_platform == "1" or user_platform == "2":
            vacancies_list.sort(reverse=True)

            for job in vacancies_list:
                formatted_salary = job.format_salary()
                job_description = job.get_description()
                print(f"{job.title}\n{job.url}\n{formatted_salary}\n{job_description}\n")

                add_vacancies_to_json_file(file_name, vacancies_list)

    elif action == "4":
        desire_salary = int(input("Укажите минимальную желаемую зарплату:\n"))

        if user_platform == "1":
            filtered_vacancies_by_salary = filter_vacancies_by_salary(vacancies_list, desire_salary)

            if not filtered_vacancies_by_salary:
                print("Нет вакансий, соответствующих заданным критериям.")

            else:

                for job in filtered_vacancies_by_salary:
                    formatted_salary = job.format_salary()
                    job_description = job.get_description()
                    print(f"{job.title}\n{job.url}\n{formatted_salary}\n{job_description}\n")

                    add_vacancies_to_json_file(file_name, filtered_vacancies_by_salary)

        elif user_platform == "2":
            filtered_vacancies_by_salary = filter_vacancies_by_salary(vacancies_list, desire_salary)

            if not filtered_vacancies_by_salary:
                print("Нет вакансий, соответствующих заданным критериям.")

            else:

                for job in filtered_vacancies_by_salary:
                    formatted_salary = job.format_salary()
                    print(f"{job.title}\n{job.url}\n{formatted_salary}\n{job.description}\n")
                    add_vacancies_to_json_file(file_name, filtered_vacancies_by_salary)

    else:
        print("Ошибка: Введен некорректный номер действия. Пожалуйста, выберите 1, 2, 3, 4, 5 или 6.")


def user_interract() -> None:
    """
    основная функция для взаимодействия с пользователем через командную
    строку
    """
    print("Вас приветствует программа-парсер вакансий.")
    user_platform = ""

    while user_platform != "3":

        user_platform = input("Выберите платформу для парсинга:\n"
                              "1. HeadHunter.ru\n"
                              "2. SuperJob.ru\n"
                              "3. Выйти из программы\n"
                              "Пожалуйста, выберите цифру, соответствущую запросу:\n")

        if user_platform == "1":
            search = input("Введите основной ключ:\n")
            vacancies_list = all_from_hh(search)

        elif user_platform == "2":
            search = input("Введите основной ключ:\n")
            vacancies_list = all_from_sj(search)

        elif user_platform == "3":
            print("Программа завершена.")
            sys.exit()

        else:
            print("Ошибка: Введен некорректный номер платформы. Пожалуйста, выберите 1, 2 или 3.\n")
            continue

        action = ""
        while action != "5":
            action = input("Выберите действие:\n"
                           "1. Показать список вакансий по вашему основному ключу\n"
                           "2. Показать список вакансий по вашему основному ключу, учитывая дополнительные ключевые слова\n"
                           "    Примечание: вакансия будет показана в том случае, если содержит хотя бы одно дополнительное ключевое слово\n"
                           "3. Показать отсортированный по зарплате список вакансий по вашему основному ключу\n"
                           "4. Показать список вакансий по вашему основному ключу, где зарплата не менее желаемой\n"
                           "5. Выйти из программы\n"
                           "6. Переход к обработке полученных данных\n")

            if action == "5":
                print("Программа завершена.")
                sys.exit()

            if action == "6":
                break

            if action in ["1", "2", "3", "4"]:
                process_action(vacancies_list, action, FILE_NAME, user_platform)

        if action == "6":
            user_input = ""

            while user_input != "4":
                user_input = input("1. Сохранить собранные данные\n"
                                   "2. Сохранить данные по вашему ключу\n"
                                   "3. Удалить данные по вашему ключу\n"
                                   "4. Выйти из программы\n")

                if user_input == "4":
                    print("Программа завершена.")
                    sys.exit()

                if user_input == "1":
                    with open("vacancies.json", "r", encoding="utf-8") as file:
                        data = json.load(file)
                    for vacancy in data:
                        print_vacancy_info(vacancy)

                elif user_input == "2":
                    print("Введите критерии для отбора вакансий (через пробел):")
                    criteria_input = input().strip()
                    get_nessesary_vacancies(FILE_NAME, criteria_input)

                elif user_input == "3":
                    delete_criteria = input("Введите критерий для удаления вакансий (через пробел): ")
                    remove_vacancies_from_json_file(FILE_NAME, delete_criteria)

                    with open(FILE_NAME, "r", encoding="utf-8") as file:
                        data = json.load(file)  # обновление data после удаления данных

                    for vacancy in data:
                        print_vacancy_info(vacancy)

                else:
                    print("Ошибка: Введен некорректный номер действия. Пожалуйста, выберите 1, 2, 3, 4 или 5.\n")
                    continue

    # завершение программы по выбору цифры 3
    print("Программа завершена.")
