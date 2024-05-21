from typing import Iterable
from fuzzywuzzy import fuzz
from typing import List


async def aiter(object: Iterable):
    for item in object:
        yield item


def sort_strings_by_similarity(pattern: str, strings: List[str]):
    """
    Сортирует список строк strings в порядке
    убывания их схожести со строкой pattern.
    """
    # Используем функцию fuzz.ratio() для сравнения схожести строк.
    # key=lambda x: fuzz.ratio(s, x) - компаратор
    # На первом месте должны быть наиболее подходящие, поэтому reverse=True.
    return sorted(strings, key=lambda x: fuzz.ratio(pattern, x), reverse=True)
