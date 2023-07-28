from src.abstract_classes import AbstractJobSaver
import json
from typing import Dict, List


class JsonSaver(AbstractJobSaver):
    """
    класс для сохранения данных в json-формат
    """

    def __init__(self, file_name: str):
        self.file_name = file_name

    def _read_data(self) -> Dict[List]:
        """
        внутренний метод для чтения данных
        """
        try:
            with open(self.file_name, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []
        return data

    def _write_data(self, data) -> None:
        """
        внутренний метод для записи данных
        """
        with open(self.file_name, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    def get_job(self, criteria_list):
        """
        метод для поиска вакансий, соответствующих определенным критериям
        """
        data = self._read_data()

        matching_jobs = []

        for job in data:
            for value in job.values():
                # проверка, является ли значение строкой и удовлетворяет ли хотя бы одному критерию
                if any(isinstance(value, str) and criteria.lower() in value.lower() for criteria in criteria_list):
                    matching_jobs.append(job)
                    break

        return matching_jobs

    def add_job(self, job):
        """
        метод для добавления новой записи о вакансии
        """
        data = self._read_data()
        data.append(job.to_dict())  # преобразование объекта в словарь перед добавлением, используется метод класса Vacancies
        self._write_data(data)

    def remove_job(self, job):
        """
        метод для удаления записи из списка данных
        """
        data = self._read_data()
        new_data = []

        for item in data:
            if item != job:
                new_data.append(item)
        self._write_data(new_data)
