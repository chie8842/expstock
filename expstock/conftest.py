import os
import pytest
from expstock import ExpStock
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
            memos=['This is a test memo'],
            git_check=False)
    yield e
    pass
    # if os.path.isdir(e.log_dirname):
    #     subprocess.run(['rm', '-rf', e.log_dirname])
