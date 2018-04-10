from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os
import sqlite3

class DbConnect(object):

    def __init__(self, filepath):
        self.dbfile = filepath
        self.conn, self.c = self.db_connect()
        self._create_table_if_not_exists()
        self.experiment_id, self.param_id = self._get_ids()

    def _create_table_if_not_exists(self):
        sqlite_tables = self._get_tables()
        if 'experiments' not in sqlite_tables:
            self._create_table_experiments()
        if 'params' not in sqlite_tables:
            self._create_table_params()

    def db_connect(self):
        conn = sqlite3.connect(self.dbfile)
        c = conn.cursor()
        return conn, c

    def _get_tables(self):
        query = 'select name from sqlite_master where type="table"'
        tables = []
        for table_info in self.c.execute(query):
            tables.append(table_info[0])
        return tables

    def _create_table_experiments(self):
        query = """
            create table if not exists experiments(
                experiment_id integer primary key autoincrement
                , experiment_name text
                , memo text
                , start_time text
                , finish_time text
                , execution_time text
                , result text
                , git_head text
                , log_dir)
        """
        self.c.execute(query)
        self.conn.commit()

    def _create_table_params(self):
        query = """
            create table if not exists params(
                param_id integer primary key autoincrement
                , experiment_id integer
                , param_name text
                , value text)
        """
        self.c.execute(query)
        self.conn.commit()

    def _get_experiments_count(self):
        query = 'select count(*) from experiments'
        experiments_count = self.c.execute(query).__next__()
        return experiments_count[0]

    def _get_params_count(self):
        query = 'select count(*) from params'
        params_count = self.c.execute(query).__next__()
        return params_count[0]

    def _get_ids(self):
        querys = { 'get_experiment_id': 'select max(experiment_id) from experiments',
                'get_param_id': 'select max(param_id) from params' }
        if self._get_experiments_count() == 0:
            experiment_id = 1
        else:
            experiment_id = self.c.execute(querys['get_experiment_id']).__next__()[0] + 1

        if self._get_params_count() == 0:
            param_id = 1
        else:
            # param_id = 3
            param_id = self.c.execute(querys['get_param_id']).__next__()[0] + 1
        return experiment_id, param_id

    def insert_into_experiments(self, e):
        query = """
        insert into experiments values (?, ?, ?, ?, ?, ?, ?, ?)
        """
        value = (
                self.experiment_id
                , e.exp_name
                , e.memo
                , e.start_time_str
                , e.finish_time_str
                , e.execution_time_str
                , e.result
                , e.git_head
                , e.log_dirname)
        self.c.execute(query, value)
        self.conn.commit()

    def insert_into_experiments_pre(self, e):
        query = """
        insert into experiments(
          experiment_id
          , experiment_name
          , memo
          , start_time
          , git_head
          , log_dir
        ) values (?, ?, ?, ?, ?, ?)
        """
        value = (
                self.experiment_id
                , e.exp_name
                , e.memo
                , e.start_time_str
                , e.git_head
                , e.log_dirname)
        self.c.execute(query, value)
        self.conn.commit()

    def update_experiments(self, e):
        query = """
        update experiments set
          finish_time = ?
          , execution_time = ?
          , result = ?
        where experiment_id = ?
        """
        value = (
                e.finish_time_str
                , e.execution_time_str
                , e.result
                , self.experiment_id)
        self.c.execute(query, value)
        self.conn.commit()


    def insert_into_params(self, e):
        query = """
        insert into params values (?, ?, ?, ?)
        """
        values = []
        for param in e.params:
            values.append(
                    (
                        self.param_id,
                        self.experiment_id,
                        param[0],
                        str(param[1])
                    ))
            self.param_id += 1
        self.c.executemany(query, values)
        self.conn.commit()


