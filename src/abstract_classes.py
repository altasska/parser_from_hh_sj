from abc import ABC, abstractmethod


class AbstractJobParser(ABC):
    """
    абстрактный класс для парсинга вакансий с различных
    платформ
    """

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass


class AbstractJobSaver(ABC):
    """
    абстрактный класс для работы с вакансиями в файле (получение, добавление,
    удаление)
    """

    @abstractmethod
    def get_job(self, criteria):
        pass

    @abstractmethod
    def add_job(self, job):
        pass

    @abstractmethod
    def remove_job(self, job):
        pass
