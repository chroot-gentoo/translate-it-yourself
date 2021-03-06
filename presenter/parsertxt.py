import re
import os


class ParserText:
    """
    ParserText принимает file path или str и возвращает tuple
    """

    PATTERN = r'\n\s+'

    __slots__ = ['text_string']

    def __init__(self, text_string: str):
        self.text_string = text_string

    def _parser_text(self, user_text: str) -> list:
        # проверяем наличие паттерна в тексте
        if re.search(self.PATTERN, user_text):
            # делаем split() по паттерну
            split_text = re.split(self.PATTERN, user_text)
            # заменяем \n на пробел для тех случаев, когда \n остается после применения паттерна
            return [(re.sub(r'[\n]', ' ', i)).capitalize() for i in split_text]
        # возвращаем текст с заменой \n на пробелы, если паттерн не обнаружен
        return [re.sub(r'[\n]', ' ', user_text).capitalize()]

    def _get_text(self) -> str:
        try:
            # определяем, является ли пользовательский ввод file path
            with open(os.path.abspath(self.text_string), 'r', encoding='UTF-8') as file:
                return file.read()
        except Exception as e:
            print(e)
            # возвращаем пользовательский ввод без пробелов и табуляций в начале и в конце текста
            return self.text_string.strip()

    def get_blocks_dict(self) -> tuple:
        text = self._get_text()
        blocks_list = self._parser_text(text)
        return tuple(blocks_list)

    @staticmethod
    def convert_to_str(data) -> str:
        return '\n\t'.join(i for i in data).strip()


if __name__ == '__main__':
    print(ParserText('Привет\n как дела?').get_blocks_dict())
