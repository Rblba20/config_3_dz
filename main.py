import argparse
import re
import json
import sys


class ConfigParser:
    def __init__(self):
        self.constants = {}

    def parse(self, text):
        text = self.remove_comments(text)  # Убираем комментарии
        blocks = self.tokenize_blocks(text)  # Разбиваем на конструкции
        result = {}

        for block in blocks:
            block = block.strip()
            if match := re.match(r'\(def ([a-z]+) (.+)\);', block, re.DOTALL):  # Объявление константы
                name, value = match.groups()
                parsed_value = self.parse_value(value)
                self.constants[name] = parsed_value
                result[name] = parsed_value
            else:
                raise SyntaxError(f"Invalid syntax in block: {block}")

        return self.resolve_constants(result)

    def parse_value(self, value):
        value = value.strip()
        if value.isdigit():  # Числа
            return int(value)
        elif value.startswith('#{') and value.endswith('}'):  # Подстановки
            const_name = value[2:-1]
            if const_name in self.constants:
                return self.constants[const_name]
            else:
                raise ValueError(f"Undefined constant '{const_name}'")
        elif value.startswith('"') and value.endswith('"'):  # Строки
            return value[1:-1]
        elif value.startswith('[') and value.endswith(']'):  # Словари
            return self.parse_dict(value[1:-1])  # обработкa вложенных словарей
        else:
            raise ValueError(f"Invalid value: {value}")

    def parse_dict(self, body):
        # Парсит тело словаря в формате 'ключ => значение'
        result = {}
        items = self.tokenize_dict_items(body)
        for item in items:
            if match := re.match(r'([a-z]+)\s*=>\s*(.+)', item.strip()):
                key, value = match.groups()
                result[key] = self.parse_value(value.strip())
            else:
                raise SyntaxError(f"Invalid dictionary item: {item}")
        return result

    def tokenize_dict_items(self, body):
        # Разделяет элементы словаря, учитывая вложенность, на отдельные пары ключ-значение.
        depth = 0
        current_item = []
        items = []

        for char in body:
            if char == ',' and depth == 0:
                items.append("".join(current_item).strip())
                current_item = []
            else:
                if char == '[':
                    depth += 1
                elif char == ']':
                    depth -= 1
                current_item.append(char)

        if current_item:
            items.append("".join(current_item).strip())

        return items

    def resolve_constants(self, data):
        # Рекурсивно заменяем подстановки в словаре или списке.
        if isinstance(data, dict):
            return {k: self.resolve_constants(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.resolve_constants(item) for item in data]
        elif isinstance(data, str) and data.startswith('#{') and data.endswith('}'):
            const_name = data[2:-1]
            if const_name in self.constants:
                return self.constants[const_name]
            else:
                raise ValueError(f"Undefined constant '{const_name}'")
        return data

    def remove_comments(self, text):
        # Удаляет комментарии из текста.
        text = re.sub(r'::.*', '', text)  # Однострочные комментарии
        text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)  # Многострочные комментарии
        return text.strip()

    def tokenize_blocks(self, text):
        # Разделяет текст на блоки по структуре `(def ...)`.
        return re.findall(r'\(def [a-z]+ .*?\);', text, re.DOTALL)


def main():
    parser = argparse.ArgumentParser(description="Учебный конфигурационный язык в JSON")
    parser.add_argument("output_file", help="Путь к файлу для вывода JSON")
    args = parser.parse_args()

    input_text = sys.stdin.read()
    config_parser = ConfigParser()

    try:
        result = config_parser.parse(input_text)
        with open(args.output_file, 'w') as f:
            json.dump(result, f, indent=4)
        print("Конфигурация успешно преобразована в JSON.")
    except (SyntaxError, ValueError) as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
