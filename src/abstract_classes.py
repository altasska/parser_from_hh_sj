from abc import ABC, abstractmethod
from typing import Dict, List

class AbstractJobParser(ABC):
    """
    абстрактный класс для парсинга вакансий с различных
    платформ
    """

    @abstractmethod
    def connect(self) -> Dict:
        """
        метод для подключения к API
        """
        pass

    @abstractmethod
    def get_vacancies(self, search_query: str) -> Dict:
        """
        метод для получения вакансий по запросу
        """
        pass


class AbstractJobSaver(ABC):
    """
    абстрактный класс для работы с вакансиями в файле (получение, добавление,
    удаление)
    """

    @abstractmethod
    def get_job(self, criteria: List) -> List:
        """
        метод для поиска вакансий, соответствующих определенным критериям
        """
        pass

    @abstractmethod
    def add_job(self, job) -> None:
        """
        метод для добавления новой записи о вакансии
        """
        pass

    @abstractmethod
    def remove_job(self, job) -> None:
        """
        метод для удаления записи из списка данных
        """
        pass
