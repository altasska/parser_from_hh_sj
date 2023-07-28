from typing import List


def get_keywords_from_user() -> List:
    """
    функция для получения ключевых слов для фильтрации вакансий
    """
    print("Введите ключевые слова для фильтрации вакансий (через пробел):")
    keywords_input = input().strip()
    keywords = keywords_input.split()
    return keywords
