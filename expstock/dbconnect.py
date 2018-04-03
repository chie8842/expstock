import os
import sqlite3

class DbConnect(object):

    def __init__(self, filepath):
        self.dbfile = filepath
        self.c = self.db_connect()
        _create_tables_if_not_exists()
        self.sqlite_tables = get_tables()

    def _create_table_if_not_exists(self):
        if 'experiments' not in sqlite_tables:
            _create_table_experiments()
        if 'params' not in sqlite_tables:
            _create_table_params()

    def db_connect(self):
        conn = sqlite3.connect(self.dbfile)
        c = conn.cursor()
        return c

    def get_tables(self):
        query = 'select name from sqlite_master where type="table"'
        tables = []
        for table_info in self.c.execute(query):
            tables.append(table_info[0])
        return tables

    def _create_table_experiments(self):
        query = """
            create if not exists experiments(
                experiment_id integer primary key autoincrement
                , experiment_name text
                , memo text
                , start_time text
                , finish_time text
                , git_head text
                , log_dir)
        """
        self.c.execute(query)
        self.c.commit()

    def _create_table_params(self):
        query = """
            create if not exists params(
                param_id integer primary key autoincrement
                , experiment_id integer
                , param_name text
                , value text)
        """
        self.c.execute(query)
        self.c.commit()

    def _get_ids(self):
        querys = { 'get_experiment_id': 'select max(experiment_id) from experiments',
                'get_param_id': 'select max(param_id) from params',
                'get_memo_id': 'select max(memo_id) from memos'}
        self.experiment_id = c.execute(querys['get_experiment_id'])[0]
        self.param_id = c.execute(querys['get_param_id'])
        self.memo_id = c.execute(querys['get_memo_id'])

    def _insert_into_experiments(self, e):
        query = """
        insert into experiments values (?, ?, ?, ?, ?, ?)
        """
        value = (
                self.experiment_id
                , e.experiment_name
                , e.memo
                , e.start_time
                , e.finish_time
                , e.git_head
                , e.log_dirname)
        self.c.execute(query, value)
        self.c.commit()

    def _insert_into_params(self, e):
        query = """
        insert into params values (?, ?, ?, ?)
        """
        value = e.params
        self.c.executemany(query, value)
        self.c.commit()


