from src.abstract_classes import AbstractJobParser
import requests


class JobParserFromHH(AbstractJobParser):
    def connect(self):
        pass

    def get_vacancies(self):
        url = "https://api.hh.ru/vacancies"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            vacancies = data.get('items', [])
            return vacancies  # возврат вакансий в json-формате

        else:
            return f"Ошибка {response.status_code}"
