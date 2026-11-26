from typing import List


def clean_number(raw_value) -> str:
    """
    Очищает входное значение от разрешенных разделителей и проверяет на посторонние символы.
    """
    # Преобразуем в строку на случай, если передан int (число без кавычек)
    text_number = str(raw_value).strip()

    # Разрешенные разделители по условию задания
    allowed_chars = {'+', '-', '(', ')', ' '}

    digits = []
    for char in text_number:
        if char.isdigit():
            digits.append(char)
        elif char in allowed_chars:
            continue
        else:
            raise ValueError("Обнаружены недопустимые символы")

    return "".join(digits)


def validate_number(digits: str) -> str:
    """
    Проверяет номер на допустимость (количество цифр и первая цифра).
    """
    length = len(digits)

    if length not in (10, 11):
        raise ValueError("Неверное количество цифр")

    if length == 11:
        first_digit = digits[0]
        if first_digit not in ('7', '8'):
            raise ValueError("11-значный номер должен начинаться с 7 или 8")
        return digits[1:]
    else:  # length == 10
        if digits[0] != '9':
            raise ValueError("10-значный номер должен начинаться с 9")
        return digits


def format_number(clean_digits: str) -> str:
    """
    Форматирует 10-значный код в единый стандарт +7 (XXX) XXX-XX-XX.
    """
    code = clean_digits[0:3]
    part1 = clean_digits[3:6]
    part2 = clean_digits[6:8]
    part3 = clean_digits[8:10]

    return f"+7 ({code}) {part1}-{part2}-{part3}"


def process_phone_list(numbers: List) -> List[str]:
    """
    Основная функция для обработки списка номеров с использованием try-except.
    """
    processed_results: List[str] = []

    for num in numbers:
        try:
            only_digits = clean_number(num)
            validated_digits = validate_number(only_digits)
            formatted = format_number(validated_digits)
            processed_results.append(formatted)
        except ValueError:
            processed_results.append("Некорректный номер")

    return processed_results


# Исходный список тестовых данных из задания
test_numbers: List = [
    "+7 (916) 123-45-67",
    "8-916-123-45-67",
    "9161234567",
    "89161234567",
    "+7 916 123 45 67",
    "12345",
    "791612345678",
    12345678901,
    "abc"
]
print(test_numbers)
# Запуск программы
final_list = process_phone_list(test_numbers)

for result in final_list:
    print(result)
