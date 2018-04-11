import os
import pytest
from expstock.expstock import ExpStock
from expstock.dbconnect import DbConnect
from freezegun import freeze_time

@pytest.fixture()
@freeze_time('2018-04-01')
def init_ExpStock():
    e = ExpStock()
    yield e
    if os.path.isdir(e.log_dirname):
        subprocess.run(['rm', '-rf', e.log_dirname])

@pytest.fixture()
@freeze_time('2018-04-01')
def init_ExpStock_with_args():
    param_a = 'This is a test param'
    param_b = 12345
    param_c = {'Name': 'Chie Hayashida'}
    e = ExpStock(
            log_dirname='test_logs/test',
            params=[('a', param_a), ('b', param_b), ('c', param_c)],
            memo='This is a test memo',
            git_check=False,
            report=True,
            exp_name='test_experiment')
    yield e
    pass
    if os.path.isdir(e.log_dirname):
        subprocess.run(['rm', '-rf', e.log_dirname])

@pytest.fixture()
def init_DbConnect_with_empty_db():
    filepath = 'experiments/test.db'
    dbconn = DbConnect(filepath)
    yield dbconn
    os.remove(filepath)
    pass

