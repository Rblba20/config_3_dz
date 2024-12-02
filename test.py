import unittest
from io import StringIO
import json
from main import ConfigParser


class TestConfigParser(unittest.TestCase):
    def setUp(self):
        self.parser = ConfigParser()

    def test_constant_declaration(self):
        """Тест объявления константы."""
        text = "(def timeout 30);"
        result = self.parser.parse(text)
        self.assertEqual(result, {"timeout": 30})

    def test_dictionary_parsing(self):
        """Тест обработки словаря."""
        text = "(def settings [mode => \"production\", retrylimit => 3, logging => \"enabled\"]);"
        result = self.parser.parse(text)
        expected = {
            "settings": {
                "mode": "production",
                "retrylimit": 3,
                "logging": "enabled"
            }
        }
        self.assertEqual(result, expected)

    def test_nested_dictionary(self):
        """Тест вложенных словарей."""
        # text = "(def settings [mode => \"production\", retrylimit => [host => 3, port => 5432], logging => \"enabled\"]);"
        text = "(def config [db => [host => 23, port => 5432], app => [debug => 67]]);"
        result = self.parser.parse(text)
        expected = {
            "config": {
                "db": {"host": 23, "port": 5432},
                "app": {"debug": 67}
            }
        }
        self.assertEqual(result, expected)

    def test_constant_substitution(self):
        """Тест подстановки константы."""
        text = "(def timeout 30); (def settings [retrylimit => #{timeout}]);"
        result = self.parser.parse(text)
        expected = {
            "timeout": 30,
            "settings": {"retrylimit": 30}
        }
        self.assertEqual(result, expected)

    def test_comments_removal(self):
        """Тест удаления комментариев."""
        text = """
        :: This is a single-line comment
        (def timeout 30);
        /* This is
        a multi-line
        comment */
        (def settings [retrylimit => #{timeout}]);
        """
        result = self.parser.parse(text)
        expected = {
            "timeout": 30,
            "settings": {"retrylimit": 30}
        }
        self.assertEqual(result, expected)

    # def test_invalid_syntax(self):
    #     """Тест обработки ошибок синтаксиса."""
    #     text = "(def timeout 30"  # Пропущена закрывающая скобка
    #     with self.assertRaises(SyntaxError):
    #         self.parser.parse(text)
    #
    # def test_undefined_constant(self):
    #     """Тест ошибки неопределенной константы."""
    #     text = "(def settings [retry_limit => #{timeout}]);"
    #     with self.assertRaises(ValueError):
    #         self.parser.parse(text)

    def test_different_domains_example1(self):
        """Пример 1: Конфигурация сервера."""
        text = """
        (def server [
            host => "127.0.0.1",
            port => 8080,
            ssl => "true"
        ]);
        """
        result = self.parser.parse(text)
        expected = {
            "server": {
                "host": "127.0.0.1",
                "port": 8080,
                "ssl": "true"
            }
        }
        self.assertEqual(result, expected)

    def test_different_domains_example2(self):
        """Пример 2: Конфигурация приложения."""
        text = """
        (def app [
            name => "MyApp",
            version => "1.0.0",
            features => [logging => "true", metrics => "false"]
        ]);
        """
        result = self.parser.parse(text)
        expected = {
            "app": {
                "name": "MyApp",
                "version": "1.0.0",
                "features": {
                    "logging": "true",
                    "metrics": "false"
                }
            }
        }
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
# coverage run -m unittest discover
# coverage report
# coverage html