from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from datetime import datetime
import mock
import os
import platform
import pytest
from freezegun import freeze_time
from expstock.expstock import ExpStock

@freeze_time('2018-04-01')
def test_variables(init_ExpStock):
    e = init_ExpStock.__next__()
    assert e.stock_root_dir == 'experiments'
    assert e.params == []
    assert e.memos == []
    assert e.git_check == True
    print(datetime.now())
    print(e.log_dirname)
    assert e.log_dirname == 'experiments/20180401_000000'

def test_variables_with_args(init_ExpStock_with_args):
    e = init_ExpStock_with_args.__next__()
    #patched_time = datetime.now()
    #mocker.patch.object(e._set_dirname, autospec='experiments/20180401')
    assert e.stock_root_dir == 'experiments'
    assert e.params == [('a', 'This is a test param'),
            ('b', 12345),
            ('c', {'Name': 'Chie Hayashida'})
            ]
    assert e.memos == ['This is a test memo']
    assert e.git_check == False
    print(datetime.now())
    print(e.log_dirname)
    assert e.log_dirname == 'test_logs/test'

def test__mk_logdir(init_ExpStock_with_args):
    e = init_ExpStock_with_args.__next__()
    print(e.log_dirname)
    e._mk_logdir()
    assert os.path.isdir(e.log_dirname)

def test__get_machine_info(init_ExpStock):
    e = init_ExpStock.__next__()
    machine_info = e._get_machine_info()
    assert machine_info[0] == ('system', platform.system())
    assert machine_info[1] == ('node', platform.node())
    assert machine_info[2] == ('release', platform.release())
    assert machine_info[3] == ('version', platform.version())
    assert machine_info[4] == ('machine', platform.machine())
    assert machine_info[5] == ('processor', platform.processor())


def test__get_git_info(init_ExpStock):
    import subprocess
    e = init_ExpStock.__next__()
    git_head, git_diff = e._get_git_info()
    expect_git_head = subprocess.check_output(['git', 'log', '-n', '1', '--format=%H'])
    expect_git_diff = subprocess.check_output(['git', 'diff'])

    print(git_head)
    print('test')
    assert git_head == expect_git_head
    assert git_diff == expect_git_diff

def test_append_param(init_ExpStock):
    e = init_ExpStock.__next__()
    test_param1 = 12345
    test_param2 = 'test_param'
    e.append_param(test_param1=test_param1, test_param2=test_param2)
    e.params.sort() 
    assert e.params == [('test_param1', 12345), ('test_param2', 'test_param')]
    print(e.params.sort())

def test_append_memo(init_ExpStock):
    e = init_ExpStock.__next__()
    test_memo = '''
    test memo
    Experiment 1
    ...
    ...
    ...
    '''
    test_memo2 = 'x = 1, y = 2'
    e.append_memo(test_memo, test_memo2)
    print(e.memos)
    assert e.memos == ['\n    test memo\n    Experiment 1\n    ...\n    ...\n    ...\n    ',  'x = 1, y = 2']

def test__write_log(init_ExpStock_with_args):
    e = init_ExpStock_with_args.__next__()
    filename = 'git_head.txt'
    filepath = os.path.join(e.log_dirname, filename)

    e._write_log(filename, b'testtesttest', 'wb')
    assert os.path.isfile(filepath)
    with open(filepath) as f:
        data = f.read()
    assert data == 'testtesttest'

def test__write_logs(init_ExpStock_with_args):
    e = init_ExpStock_with_args.__next__()
    filename = 'params.txt'
    filepath = os.path.join(e.log_dirname, filename)

    e._write_logs(filename, e.params)
    assert os.path.isfile(filepath)
    with open(filepath) as f:
        data = f.read()
    print(data)
    assert data == '''a = This is a test param
b = 12345
c = {'Name': 'Chie Hayashida'}
'''

def test__create_report(init_ExpStock_with_args):
    e = init_ExpStock_with_args.__next__()
    e._create_report()

    filename = 'report.txt'
    filepath = os.path.join(e.log_dirname, filename)

    assert os.path.isfile(filepath)

