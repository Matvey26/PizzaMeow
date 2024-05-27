from fuzzywuzzy import fuzz
from typing import List


def search_by_similarity(
    records: List[dict],
    threshold: int = 90,
    **kwargs
) -> list:
    """Ищет записи по указанным ключам и значениям
    с использованием нечеткого поиска.

    Параметры
    ---------
    threshold : int
        Минимальный порог похожести для включения записи в результаты.
    **kwargs
        Ключи и значения, по которым нужно искать записи.

    Возвращает
    ----------
    list :
        Список найденных записей, удовлетворяющих условиям нечеткого поиска.
    """

    results = []

    for record in records:
        for key, value in kwargs.items():
            record_value = str(record.get(key, ''))
            if fuzz.ratio(
                    record_value.lower(), str(value).lower()) >= threshold:
                results.append(record)
                # Не добавлять запись несколько раз,
                # если совпало по нескольким полям
                break

    return results
