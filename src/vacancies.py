import requests
from bs4 import BeautifulSoup
from typing import Dict, Tuple, Union


class Vacancies:

    def __init__(self, title: str, url: str, salary_data: Dict, description: str, api_url: str):
        """
        инициализация класса вакансии
        """
        self.title = title
        self.url = url
        self.salary_data = salary_data
        self.description = description
        self.api_url = api_url

    def to_dict(self) -> Dict:
        """
        метод для преобразованя объекта в словарь для корректной работы JSON-saver
        """
        data = {
            "title": self.title,
            "url": self.url,
            "salary_data": self.salary_data,
            "description": self.get_description(),
        }

        return data

    def format_salary(self) -> str:
        """
        метод для форматирования данных о зарплате и представления
        в читабельном виде.
        """
        formatted_salary_str = ""

        if isinstance(self.salary_data, dict):
            from_salary = self.salary_data.get('from')
            to_salary = self.salary_data.get('to')
            currency = self.salary_data.get('currency')
            gross = None

            if from_salary and to_salary:
                formatted_salary_str = f"Зарплата от {from_salary} до {to_salary} {currency}"
            elif from_salary:
                formatted_salary_str = f"Зарплата от {from_salary} {currency}"
            elif to_salary:
                formatted_salary_str = f"Зарплата до {to_salary} {currency}"
        else:
            formatted_salary_str = "Зарплата не указана"

        return formatted_salary_str

    def get_description(self) -> str:
        """
        метод для считывания описания вакансии и представления
        в читабельном виде без HTML-тегов
        """
        if self.api_url:
            # если description в принимаемом json не содержится (как в HH)
            response = requests.get(self.api_url)

            if response.status_code == 200:
                data = response.json()
                description = data.get('description')

                if description:
                    soup = BeautifulSoup(description, 'html.parser')
                    clean_text = soup.get_text()
                    return clean_text
                else:
                    return "Описание не доступно"

            else:
                return f"Ошибка {response.status_code}"

        # если ключ есть в принимаемом json (как в SJ)
        elif self.description:
            return self.description

        else:
            return "Описание не доступно"

    def validate(self) -> bool:
        """
        метод для валидации данных, которыми инициализируются атрибуты класса
        """
        if not self.title or not self.url or self.salary_data is None or not self.description:
            return False
        else:
            return True

    def get_salary_amount(self) -> Tuple:
        """
        метод для извлечения числовых значений зарплаты из словаря salary_data.
        """
        if isinstance(self.salary_data, dict):
            from_salary = self.salary_data.get('from')
            to_salary = self.salary_data.get('to')
            return from_salary, to_salary
        else:
            return None, None

    def __le__(self, other) -> Union[bool, str]:
        """
        метод для сравнения вакансий по зарплате
        """
        if isinstance(other, Vacancies):
            self_from_salary, self_to_salary = self.get_salary_amount()
            other_from_salary, other_to_salary = other.get_salary_amount()

            # преобразование строк в числа
            if self_from_salary is not None and self_from_salary != "":
                self_from_salary = int(self_from_salary)
            if self_to_salary is not None and self_to_salary != "":
                self_to_salary = int(self_to_salary)
            if other_from_salary is not None and other_from_salary != "":
                other_from_salary = int(other_from_salary)
            if other_to_salary is not None and other_to_salary != "":
                other_to_salary = int(other_to_salary)

            # если зарплата не указана
            if self_from_salary is None and self_to_salary is None:
                return True
            elif other_from_salary is None and other_to_salary is None:
                return False

            # отсутствует значение 'from', то оно равно 0
            self_from_salary = self_from_salary or 0
            other_from_salary = other_from_salary or 0

            # если поля 'from' и 'to' пустые
            if self_from_salary == 0 and self_to_salary == 0 and other_from_salary == 0 and other_to_salary == 0:
                return True

            # равенство зарплат
            if self_from_salary == other_from_salary and self_to_salary == other_to_salary:
                return "Зарплаты одинаковые"

            # сравнение зарплат
            if self_from_salary < other_from_salary:
                return True
            elif self_from_salary > other_from_salary:
                return False

            # если  'from' одинаковые - сравнение по значению 'to'
            if self_to_salary is None:
                return False
            elif other_to_salary is None:
                return True
            else:
                return self_to_salary <= other_to_salary

        else:
            raise TypeError

    def __lt__(self, other) -> bool:
        """
        метод для сравнения вакансий по зарплате (меньше)
        """
        result = self.__le__(other)
        if result == "Зарплаты одинаковые":
            return False
        return result

    def __gt__(self, other) -> bool:
        """
        метод для сравнения вакансий по зарплате (больше)
        """
        result = self.__le__(other)
        if result == "Зарплаты одинаковые":
            return False
        return not result

    def __ge__(self, other) -> bool:
        """
        метод для сравнения вакансий по зарплате (больше или равно)
        """
        result = self.__le__(other)
        return result or (result == "Зарплаты одинаковые")
