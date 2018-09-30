import sqlite3


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
        self.cursor.execute('insert into local_projects (prj_name, author, link_original) '
                            'values (:prj_name, :author, :link_original)', (prj_name, author, link_original))
        self.conn.commit()

    def set_en_text(self, prj_id, block_id, en_text):
        self.cursor.execute('import into book_en ( prj_id,  block_id,  en_text) '
                            'values (:prj_id, :block_id, :en_text);', (prj_id, block_id, en_text))
        self.conn.commit()

    def set_ru_text(self, prj_id, block_id, ru_text):
        self.cursor.execute('import into book_ru (prj_id, block_id, ru_text) '
                            'values (:prj_id, :block_id, :ru_text);', (prj_id, block_id, ru_text))
        self.conn.commit()

    def drop_project(self, prj_id):
        self.cursor.execute('delete from local_projects where prj_id = :prj_id; '
                            'delete from book_en where prj_id = :prj_id;'
                            'delete from book_ru where prj_id = :prj_id;', prj_id)
        self.conn.commit()

    def get_few_block_en(self, prj_id, blk_begin, blk_end):
        self.cursor.execute('select en_text from book_en where prj_id = :prj_id '
                            'and block_id >= :blk_begin and block_id <= :blk_end', (prj_id, blk_begin, blk_end))
        self.conn.commit()

    def get_few_block_ru(self, prj_id, blk_begin, blk_end):
        self.cursor.execute('select ru_text from book_ru where prj_id = :prj_id '
                            'and block_id >= :blk_begin and block_id <= :blk_end', (prj_id, blk_begin, blk_end))
        self.conn.commit()

    def update_data_ru(self, ru_text, prj_id, blk_id):
        self.cursor.execute('update book_ru set ru_text = :ru_text '
                            'where prj_id = :prj_id and block_id = :blk_id', (ru_text, prj_id, blk_id))
        self.conn.commit()

    def update_data_en(self, en_text, prj_id, blk_id):
        self.cursor.execute('update book_en set en_text = :en_text '
                            'where prj_id = :prj_id and block_id = :blk_id', (en_text, prj_id, blk_id))
        self.conn.commit()

    def get_full_ru(self, prj_id):
        self.cursor.execute('select ru_text from book_ru where prj_id = :prj_id', prj_id)
        self.conn.commit()


if __name__ == '__main__':
    pass     # место для тестов.
