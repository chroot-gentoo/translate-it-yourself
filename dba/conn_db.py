import sqlite3


# TODO: все запросы на создание таблиц обернуть в один метот create_base, который должен запускаться в __init__
# TODO: все запросы должны быть с ловлей исключений
# TODO: все методы должны работать только с текстовым именем проекта, если нужен id, он должен получаться отдельным запросом
# TODO: некоторые методы я переписал, чтобы просто опробовать связи, нужно еще раз связываться и уже допиливать
class CDataBase:
    def __init__(self):
        self.conn = sqlite3.connect("tiy.db")
        self.cursor = self.conn.cursor()

    def create_table_local_projects(self):
        self.cursor.execute('create table if not exists local_projects '
                            '(prj_id integer unique primary key, prj_name text, '
                            'author text, link_original text)')
        self.conn.commit()

    def create_table_book_en(self):
        self.cursor.execute('create table if not exists book_en'
                            '(prj_id integer, block_id integer, '
                            'en_text text, primary key(prj_id, block_id))')
        self.conn.commit()

    def create_table_book_ru(self):
        self.cursor.execute('create table if not exists book_ru'
                            '(prj_id integer, block_id integer, '
                            'ru_text text, primary key(prj_id, block_id))')
        self.conn.commit()

    def set_project(self, prj_name, author, link_original):
        try:
            self.cursor.execute(f'select prj_name from local_projects where prj_name = \'{prj_name}\'')
            if self.cursor.fetchone():
                # TODO: вернуть в обработчик, для повторного запроса и сообщений пользователю
                print('проект существует')
            else:
                self.cursor.execute('insert or replace into local_projects (prj_name, author, link_original) '
                                    'values (:prj_name, :author, :link_original)', (prj_name, author, link_original))
                self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()

    def set_en_text(self, prj_name, block_id, en_text):
        try:
            self.cursor.execute(f'select prj_id from local_projects where prj_name = \'{prj_name}\'')
            prj_id = self.cursor.fetchone()[0]
            self.cursor.execute(f'select * from book_en where prj_id = \'{prj_id}\' and block_id = \'{block_id}\'')
            if self.cursor.fetchone():
                self.cursor.execute('update book_en set en_text = :en_text '
                                    'where prj_id = :prj_id and block_id = :blk_id', (en_text, prj_id, block_id))
            else:
                self.cursor.execute('insert into book_en ( prj_id,  block_id,  en_text) '
                                    'values (:prj_id, :block_id, :en_text);', (prj_id, block_id, en_text))
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()

    def set_ru_text(self, prj_name, block_id, ru_text):
        try:
            self.cursor.execute(f'select prj_id from local_projects where prj_name = \'{prj_name}\'')
            prj_id = self.cursor.fetchone()[0]
            self.cursor.execute(f'select * from book_ru where prj_id = \'{prj_id}\' and block_id = \'{block_id}\'')
            if self.cursor.fetchone():
                self.cursor.execute('update book_ru set ru_text = :ru_text '
                                    'where prj_id = :prj_id and block_id = :blk_id', (ru_text, prj_id, block_id))
            else:
                self.cursor.execute('insert into book_ru (prj_id, block_id, ru_text) '
                                    'values (:prj_id, :block_id, :ru_text);', (prj_id, block_id, ru_text))
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()

    def drop_project(self, prj_id):
        self.cursor.execute('delete from local_projects where prj_id = :prj_id; '
                            'delete from book_en where prj_id = :prj_id;'
                            'delete from book_ru where prj_id = :prj_id;', prj_id)
        self.conn.commit()

    def get_few_block_en(self, prj_name, blk_begin=None, blk_end=None):
        try:
            self.cursor.execute(f'select prj_id from local_projects where prj_name = \'{prj_name}\'')
            prj_id = self.cursor.fetchone()[0]
            self.cursor.execute(f'select en_text from book_en where prj_id = \'{prj_id}\'')

            if self.cursor.fetchall():
                return self.cursor.fetchall()
            else:
                return None
        except Exception as e:
            print(e)

    def get_few_block_ru(self, prj_name, blk_begin=None, blk_end=None):
        try:
            self.cursor.execute(f'select prj_id from local_projects where prj_name = \'{prj_name}\'')
            prj_id = self.cursor.fetchone()[0]
            self.cursor.execute(f'select ru_text from book_ru where prj_id = \'{prj_id}\'')

            if self.cursor.fetchall():
                return self.cursor.fetchall()
            else:
                return None
        except Exception as e:
            print(e)

    def update_data_ru(self, ru_text, prj_name, blk_id):
        try:
            self.cursor.execute(f'select prj_id from local_projects where prj_name = \'{prj_name}\'')
            prj_id = self.cursor.fetchone()[0]
            self.cursor.execute('update book_ru set ru_text = :ru_text '
                                'where prj_id = :prj_id and block_id = :blk_id', (ru_text, prj_id, blk_id))

            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()

    def update_data_en(self, en_text, prj_name, blk_id):
        try:
            self.cursor.execute(f'select prj_id from local_projects where prj_name = \'{prj_name}\'')
            prj_id = self.cursor.fetchone()[0]
            self.cursor.execute('update book_en set en_text = :en_text '
                                'where prj_id = :prj_id and block_id = :blk_id', (en_text, prj_id, blk_id))

            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()

    def get_project_names(self):
        try:
            self.cursor.execute('select prj_name from local_projects')
            return self.cursor.fetchall()
        except Exception as e:
            print(e)

    def get_full_ru(self, prj_id):
        self.cursor.execute('select ru_text from book_ru where prj_id = :prj_id', prj_id)
        return self.cursor.fetchall()


if __name__ == '__main__':
    a = CDataBase()
    # a.set_project('python', 'Guido', 'python.org')
    print(a.get_project_names())
