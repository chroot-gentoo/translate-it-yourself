import json
from abc import ABCMeta, abstractmethod
import dba.conn_db as conn_db


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
        self.project_id = None
        self.projects_names = None

    def create_project(self, **kwargs):
        print(kwargs)
        self.project_name = kwargs['project_name']
        self.db_.set_project(prj_name=kwargs['project_name'],
                             author=kwargs['author_name'],
                             link_original=kwargs['source_link'])
        if self.get_project_id(self.project_name) is not None:
            self.project_id = self.get_project_id(self.project_name)

    def open_project(self, project_name: str):
        print('hi, im open project')
        self.project_name = project_name
        self.project_id = self.get_project_id(self.project_name)
        return self.get_data()

    def get_project_id(self, project_name):
        print('hi, im get project id')
        return self.db_.get_project_id(project_name)

    def get_projects_names(self):
        print('im here!')
        self.projects_names = self.db_.get_projects_names()
        return tuple(str(i[0]) for i in self.projects_names)

    def get_data(self):
        print('hi im get data for id:', self.project_id)
        blocks = self.db_.get_all_block(self.project_id)
        if blocks:
            return tuple((i[0], i[1]) for i in blocks)

    # TODO: делать commit каждые 100 записей (подумать про декоратор)
    def set_data(self, data: dict):
        print('hi, im set the', data)
        for idx in data:
            # print('en', data[idx][0])
            # print('ru', data[idx][1])
            self.db_.set_en_text(prj_id=self.project_id, block_id=idx, en_text=data[idx][0])
            self.db_.set_ru_text(prj_id=self.project_id, block_id=idx, ru_text=data[idx][1])
        self.db_.make_commit()

    def del_project(self, project_name):
        self.db_.drop_project(self.get_project_id(project_name))


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
