from presenter.parsertxt import ParserText


class Presenter(object):

    def __init__(self, view, model):
        self._model = model
        self._view = view
        self._view.set_text_blocks.connect(self.set_blocks)
        self._view.load_from_file.connect(self.loadfrom_file)
        self._view.dump_to_file.connect(self.dumpto_file)
        self._view.open_cur_project.connect(self.open_project)

    def get_blocks(self, data: dict):
        # data = self._model.get_data()
        data_tuple = (data[i] for i in data.keys())
        self._view.add_text(data_tuple)

    def set_blocks(self, data):
        data_dict = {}
        for idx, item in enumerate(data):
            data_dict.update({idx: item})
        self._model.data = data_dict
        self._model.set_data()

    def dumpto_file(self, data, file_name):
        data_str = ParserText.convert_to_str(data)
        self._model.file_name = file_name
        self._model.data = data_str
        self._model.dumpto_file()

    def loadfrom_file(self, file_name):
        data = ParserText(file_name).get_blocks_dict()
        data_tuple = ((data[i], '') for i in data.keys())
        self._view.add_text(data_tuple)

    def open_project(self, project_name):
        data = self._model.open_project(project_name)
        self.get_blocks(data)

