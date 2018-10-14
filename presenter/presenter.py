from presenter.parsertxt import ParserText


# TODO: в большой степени методы носят тестовый характер. Изменим при реализации базы
class Presenter(object):

    def __init__(self, view, model):
        self._model = model
        self._view = view
        self._view.set_text_blocks.connect(self.set_blocks)
        self._view.load_from_file.connect(self.loadfrom_file)
        self._view.dump_to_file.connect(self.dumpto_file)
        self._view.open_cur_project.connect(self.open_project)
        self._view.create_project.connect(self.create_project)
        self._view.get_projects_names.connect(self.get_projects_names)
        self._view.delete_project.connect(self.del_project)

    def get_projects_names(self, action):
        projects_names = self._model.get_projects_names()
        if projects_names is not None:
            if action == 'open':
                self._view.open_projects(projects_names)
            elif action == 'delete':
                self._view.delete_projects(projects_names)

    def create_project(self, dict_):
        self._model.create_project(**dict_)
        self.loadfrom_file(dict_['file_path'])
        if self._model.get_project_id(dict_['project_name']):
            self._view.save_project()

    def get_blocks(self, data: tuple):
        self._view.add_text(data)

    def set_blocks(self, data):
        self._model.set_data(data)

    def dumpto_file(self, data, file_name):
        data_str = ParserText.convert_to_str(data)
        self._model.file_name = file_name
        self._model.data = data_str
        self._model.dumpto_file()

    def loadfrom_file(self, file_name):
        data = ParserText(file_name).get_blocks_dict()
        data_tuple = ((i, '') for i in data)
        self._view.add_text(data_tuple)

    def open_project(self, project_name):
        data = self._model.open_project(project_name)
        if data is not None:
            self.get_blocks(data)

    def del_project(self, project_name):
        self._model.del_project(project_name)
