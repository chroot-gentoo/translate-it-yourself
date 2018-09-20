import json
from abc import ABCMeta, abstractmethod


class AbsModel:
    """
    Абстрактный класс для описания стандартных методов для моделей
    """

    def __init__(self, file_name=None, data=None):
        self.file_name = file_name
        self.data = data

    __metaclass__ = ABCMeta

    @abstractmethod
    def create_project(self, project_name: str):
        pass

    @abstractmethod
    def open_project(self, project_name: str):
        pass

    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def set_data(self):
        pass

    def dumpto_file(self):
        try:
            with open(self.file_name, 'w') as file:
                file.write(self.data)
        except Exception as e:
            print('Error (so bad):', e)

    def loadfrom_file(self):
        try:
            with open(self.file_name, 'r') as file:
                self.data = file.read()
            return self.data
        except Exception as e:
            print('Error (so bad):', e)


class SQLiteRepository(AbsModel):

    __slots__ = ['file_name', 'data']

    def __init__(self, file_name, data):
        super().__init__(file_name, data)

    def create_project(self, project_name: str):
        pass

    def open_project(self, project_name: str):
        pass

    def get_data(self):
        pass

    def set_data(self):
        pass


class TempRepository(AbsModel):

    __slots__ = ['file_name', 'data']

    def __init__(self, file_name, data):
        super().__init__(file_name, data)

    def create_project(self, project_name):
        pass

    def open_project(self, project_name: str):
        return self.get_data()

    def set_data(self):
        print(self.file_name, self.data)
        try:
            with open(self.file_name, 'w') as file:
                file.write(json.dumps(self.data))
            print('done')
        except Exception as e:
            print('Error (so bad):', e)

    def get_data(self):
        try:
            with open(self.file_name, 'r') as file:
                data = dict(json.loads(file.read(), encoding='utf-8'))
            print('done')
            return data
        except Exception as e:
            print('Error (so bad):', e)


class Repository(TempRepository):

    __slots__ = ['file_name', 'data']

    def __init__(self, file_name='Hello.json', data=None):
        super().__init__(file_name, data)
