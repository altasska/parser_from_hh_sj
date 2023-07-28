import requests
from src.abstract_classes import AbstractJobParser
from typing import Dict
import os


class SuperJobParser(AbstractJobParser):
    """
    класс для парсинга с SuperJob
    """

    def __init__(self):
        self.base_url = "https://api.superjob.ru/2.0/vacancies/"
        self.secret_key = os.environ.get('API_KEY_SJ')

    def connect(self) -> Dict:
        """
        метод для подключения к API
        """
        headers = {"X-Api-App-Id": self.secret_key}
        response = requests.get(self.base_url, headers=headers)
        response.raise_for_status()  # проверка на ошибки
        return response.json()

    def get_vacancies(self, search_query: str) -> Dict:
        """
        метод для получения вакансий по запросу
        """
        url = f"{self.base_url}?keyword={search_query}"
        headers = {"X-Api-App-Id": self.secret_key}

        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Проверка на ошибки в запросе
        data = response.json()

        if not data.get('objects'):
            return "Извините, по вашему поисковому запросу не нашлось вакансий."
        return data
