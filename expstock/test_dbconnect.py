from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
from expstock.dbconnect import DbConnect
from freezegun import freeze_time

def test_variables(init_DbConnect_with_empty_db):
    dbconn = init_DbConnect_with_empty_db
    tables = dbconn._get_tables()
    print(tables)
    assert 'experiments' in tables
    assert 'params' in tables

def test__get_ids(init_DbConnect_with_empty_db):
    dbconn = init_DbConnect_with_empty_db
    experiment_id, param_id = dbconn._get_ids()
    assert experiment_id == 1
    assert param_id == 1

@freeze_time('2018-04-01')
def test_insert_into_experiments(init_DbConnect_with_empty_db, init_ExpStock_with_args):
    dbconn = init_DbConnect_with_empty_db
    e = init_ExpStock_with_args.__next__()
    e.pre_stock()
    e.post_stock(result='test result')
    dbconn.insert_into_experiments(e)

    query = 'select * from experiments where experiment_id = {}'.format(dbconn.experiment_id)
    actual = dbconn.c.execute(query).__next__()

    expected = (dbconn.experiment_id,
            'test_experiment',
            'This is a test memo',
            '2018/04/01 00:00:00',
            '2018/04/01 00:00:00',
            '0:00:00',
            'test result',
            None,
            os.path.abspath('test_logs/test'))
    assert expected == actual

def test_insert_into_params(init_DbConnect_with_empty_db, init_ExpStock_with_args):
    dbconn = init_DbConnect_with_empty_db
    param_id = dbconn.param_id
    e = init_ExpStock_with_args.__next__()
    e.pre_stock()
    e.post_stock(result='test result')
    print(e.params)
    dbconn.insert_into_params(e)
    query = 'select count(*) from params where experiment_id = {}'.format(dbconn.experiment_id)
    assert dbconn.c.execute(query).__next__()[0] == len(e.params)

    query = 'select * from params where experiment_id = {}'.format(dbconn.experiment_id)
    for row in dbconn.c.execute(query):
        assert row[0] == param_id
        assert row[1] == dbconn.experiment_id
        assert row[2] in ['a', 'b', 'c']
        assert row[3] in [str(param[1]) for param in e.params]
        param_id += 1

@freeze_time('2018-04-01')
def test_insert_into_experiments_pre(init_DbConnect_with_empty_db, init_ExpStock_with_args):
    dbconn = init_DbConnect_with_empty_db
    e = init_ExpStock_with_args.__next__()
    e.pre_stock()
    e.post_stock(result='test result')
    dbconn.insert_into_experiments_pre(e)

    query = 'select * from experiments where experiment_id = {}'.format(dbconn.experiment_id)
    actual = dbconn.c.execute(query).__next__()

    expected = (dbconn.experiment_id,
            'test_experiment',
            'This is a test memo',
            '2018/04/01 00:00:00',
            None,
            None,
            None,
            None,
            os.path.abspath('test_logs/test'))
    assert expected == actual

@freeze_time('2018-04-01')
def test_update_experiments(init_DbConnect_with_empty_db, init_ExpStock_with_args):
    dbconn = init_DbConnect_with_empty_db
    e = init_ExpStock_with_args.__next__()
    e.pre_stock()
    dbconn.insert_into_experiments_pre(e)
    e.post_stock(result='test result')
    dbconn.update_experiments(e)

    query = 'select * from experiments where experiment_id = {}'.format(dbconn.experiment_id)
    actual = dbconn.c.execute(query).__next__()

    expected = (dbconn.experiment_id,
            'test_experiment',
            'This is a test memo',
            '2018/04/01 00:00:00',
            '2018/04/01 00:00:00',
            '0:00:00',
            'test result',
            None,
            os.path.abspath('test_logs/test'))
    assert expected == actual

