import json
from abc import ABCMeta, abstractmethod
import conn_db


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
    def set_data(self, data: tuple):
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
        self.db_ = conn_db.CDataBase()
        self.project_name = None

    def create_project(self, **kwargs):
        print(kwargs)
        self.project_name = kwargs['project_name']
        self.db_.set_project(prj_name=kwargs['project_name'],
                             author=kwargs['author_name'],
                             link_original=kwargs['source_link'])

    def open_project(self, project_name: str):
        self.project_name = project_name
        return self.get_data()

    def get_data(self):
        en_ = self.db_.get_few_block_en(self.project_name)
        ru_ = self.db_.get_few_block_ru(self.project_name)
        return tuple((en_[i], ru_[i]) for i in en_)

    def set_data(self, data: tuple):
        print(data)
        for idx, i in enumerate(data):
            print('en', i[0])
            print('ru', i[1])
            self.db_.set_en_text(prj_name=self.project_name, block_id=idx, en_text=i[0])
            self.db_.set_ru_text(prj_name=self.project_name, block_id=idx, ru_text=i[1])


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


class Repository(SQLiteRepository):

    __slots__ = ['file_name', 'data']

    def __init__(self, file_name='Hello.json', data=None):
        super().__init__(file_name, data)
