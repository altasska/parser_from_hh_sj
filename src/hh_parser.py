from src.abstract_classes import AbstractJobParser
import requests
from typing import Dict, Union


class JobParserFromHH(AbstractJobParser):
    def connect(self) -> None:
        pass

    def get_vacancies(self, search_query: str) -> Union[Dict, str]:
        """
        здесь просто возвращаем json-файл со всеми вакансиями по запросу
        """
        url = f"https://api.hh.ru/vacancies?text={search_query}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            vacancies = data.get('items', [])

            if not vacancies:
                return "Извините, по вашему поисковому запросу не нашлось вакансий."

            return vacancies
        else:
            return "Ошибка {response.status_code}"
