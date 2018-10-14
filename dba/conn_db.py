import sqlite3
from os.path import abspath, join

DB_PATH = join(abspath('.'), 'tiy.db')


# TODO: все запросы на создание таблиц обернуть в один метот create_base, который должен запускаться в __init__
class CDataBase:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()

    def create_table_local_projects(self):
        try:
            self.cursor.execute('create table if not exists local_projects '
                                '(prj_id integer unique primary key, prj_name text, '
                                'author text, link_original text)')
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()

    def create_table_book_en(self):
        try:
            self.cursor.execute('create table if not exists book_en'
                                '(prj_id integer, block_id integer, '
                                'en_text text, primary key(prj_id, block_id))')
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()

    def create_table_book_ru(self):
        try:
            self.cursor.execute('create table if not exists book_ru'
                                '(prj_id integer, block_id integer, '
                                'ru_text text, primary key(prj_id, block_id))')
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()

    def set_project(self, prj_name, author, link_original):
        try:
            self.cursor.execute('select prj_name from local_projects where prj_name = :prj_name',
                                (prj_name,))
            if self.cursor.fetchone():
                # TODO: вернуть в обработчик, для повторного запроса и сообщений пользователю
                print('проект существует')
            else:
                self.cursor.execute('insert into local_projects (prj_name, author, link_original) '
                                    'values (:prj_name, :author, :link_original)', (prj_name, author, link_original))
                self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()

    def set_en_text(self, prj_id, block_id, en_text):
        try:
            self.cursor.execute('select * from book_en where prj_id = :prj_id and block_id = :block_id',
                                (prj_id, block_id))
            if self.cursor.fetchone():
                self.cursor.execute('update book_en set en_text = :en_text '
                                    'where prj_id = :prj_id and block_id = :blk_id', (en_text, prj_id, block_id))
            else:
                self.cursor.execute('insert into book_en ( prj_id,  block_id,  en_text) '
                                    'values (:prj_id, :block_id, :en_text);', (prj_id, block_id, en_text))
            # self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()

    def set_ru_text(self, prj_id, block_id, ru_text):
        try:
            self.cursor.execute('select * from book_ru where prj_id = :prj_id and block_id = :block_id',
                                (prj_id, block_id))
            if self.cursor.fetchone():
                self.cursor.execute('update book_ru set ru_text = :ru_text '
                                    'where prj_id = :prj_id and block_id = :blk_id', (ru_text, prj_id, block_id))
            else:
                self.cursor.execute('insert into book_ru (prj_id, block_id, ru_text) '
                                    'values (:prj_id, :block_id, :ru_text);', (prj_id, block_id, ru_text))
            # self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()

    def drop_project(self, prj_id):
        try:
            self.cursor.execute('delete from local_projects where prj_id = :prj_id', (prj_id,))
            self.cursor.execute('delete from book_en where prj_id = :prj_id', (prj_id,))
            self.cursor.execute('delete from book_ru where prj_id = :prj_id', (prj_id,))
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()

    def get_project_id(self, prj_name):
        try:
            self.cursor.execute('select prj_id from local_projects where prj_name = :prj_name', (prj_name,))
            fetch = tuple(self.cursor.fetchone())
            if len(fetch) > 0:
                print('id is', fetch)
                return fetch[0]
            else:
                return None
        except Exception as e:
            print(e)

    def get_all_block(self, prj_id):
        try:
            self.cursor.execute('select en_text, ru_text from book_en '
                                'left join book_ru on book_en.prj_id = book_ru.prj_id '
                                'and book_en.block_id = book_ru.block_id '
                                'where book_en.prj_id = :prj_id', (prj_id,))
            fetch = tuple(self.cursor.fetchall())
            if len(fetch) > 0:
                return fetch
            else:
                return None
        except Exception as e:
            print(e)

    def make_commit(self):
        self.conn.commit()

    def update_data_ru(self, ru_text, prj_id, blk_id):
        try:
            self.cursor.execute('update book_ru set ru_text = :ru_text '
                                'where prj_id = :prj_id and block_id = :blk_id', (ru_text, prj_id, blk_id))

            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()

    def update_data_en(self, en_text, prj_id, blk_id):
        try:
            self.cursor.execute('update book_en set en_text = :en_text '
                                'where prj_id = :prj_id and block_id = :blk_id', (en_text, prj_id, blk_id))

            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()

    def get_projects_names(self):
        try:
            self.cursor.execute('select prj_name from local_projects')
            fetch = tuple(self.cursor.fetchall())
            if len(fetch) > 0:
                return fetch
            else:
                return None
        except Exception as e:
            print(e)

    def get_full_ru(self, prj_id):
        try:
            self.cursor.execute('select ru_text from book_ru where prj_id = :prj_id', (prj_id,))
            fetch = tuple(self.cursor.fetchall())
            if len(fetch) > 0:
                return fetch
            else:
                return None
        except Exception as e:
            print(e)

    def close(self):
        self.conn.close()


if __name__ == '__main__':
    a = CDataBase()
    print(a.get_projects_names())
    print(a.get_project_id('python'))
