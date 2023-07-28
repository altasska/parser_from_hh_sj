from typing import List


def filter_vacancies_by_criteria(vacancies_list: List, criteria: str) -> List:
    """
    функция для фильтрации списка вакансии по заданому критерию
    """
    filtered_vacancies = []

    for job in vacancies_list:
        job_dict = job.to_dict()
        if not any(criteria.lower() in value.lower() for value in job_dict.values()):
            filtered_vacancies.append(job)

    return filtered_vacancies


def filter_vacancies_by_keywords(vacancies_list: List, keywords: list) -> List:
    """
    функция для фильтрации списка вакансии по заданным ключевым словам в описании
    """
    filtered_vacancies = []

    for job in vacancies_list:
        job_description = job.get_description()
        if job_description is not None and any(keyword.lower() in job_description.lower() for keyword in keywords):
            filtered_vacancies.append(job)

    return filtered_vacancies


def filter_vacancies_by_salary(vacancies_list: List, desired_salary: int) -> List:
    """
    функция для фильтрации списка вакансий по желаемой минимальной зарплате (по 'from').
    """
    desired_salary = int(desired_salary)

    filtered_vacancies = []

    for vacancy in vacancies_list:
        from_salary, to_salary = vacancy.get_salary_amount()

        if from_salary is not None and from_salary != "":
            from_salary = int(from_salary)

        from_salary = from_salary or 0

        if from_salary >= desired_salary:
            filtered_vacancies.append(vacancy)

    return filtered_vacancies
