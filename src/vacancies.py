import requests
from bs4 import BeautifulSoup


class Vacancies:

    def __init__(self, title, url, salary_data, description, api_url):
        """
        инициализация класса вакансии
        """
        self.title = title
        self.url = url
        self.salary_data = salary_data
        self.description = description
        self.api_url = api_url

    def format_salary(self):
        """
        метод для форматирования данных о зарплате и представлении
        в читабельном виде
        """
        if isinstance(self.salary_data, dict):
            from_salary = self.salary_data.get('from')
            to_salary = self.salary_data.get('to')
            currency = self.salary_data.get('currency')

            if from_salary and to_salary:
                formatted_salary = f"Зарплата от {from_salary} до {to_salary} {currency}"
            elif from_salary:
                formatted_salary = f"Зарплата от {from_salary} {currency}"
            elif to_salary:
                formatted_salary = f"Зарплата до {to_salary} {currency}"
        else:
            formatted_salary = "Зарплата не указана"

        return formatted_salary

    def get_description(self):
        """
        метод для считывания описания вакансии и представлении
        в читабельном виде без HTML-тегов
        """
        if self.api_url:
            response = requests.get(self.api_url)

            if response.status_code == 200:
                data = response.json()
                description = data.get('description')

                soup = BeautifulSoup(description, 'html.parser')
                clean_text = soup.get_text()

                return clean_text

            else:
                return f"Ошибка {response.status_code}"

    def validate(self):
        """
        метод для валидации данных, которыми инициализируются атрибуты класса
        """
        if not self.title or not self.url or self.salary_data is None or not self.description:
            return False
        else:
            return True

    def __le__(self, other):
        """
        метод для сравнения вакансий по зарплате
        """
        if isinstance(other, Vacancies):
            if self.salary_data is None and other.salary_data is None:
                return True
            elif self.salary_data is None:
                return False
            elif other.salary_data is None:
                return True
            else:
                return self.salary_data <= other.salary_data
        else:
            raise TypeError
