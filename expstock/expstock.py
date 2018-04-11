from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from datetime import datetime
import functools
import os
import platform
import sys
import subprocess
from expstock.dbconnect import DbConnect


class ExpStock(object):
    """ExpStock
    e.g. Now, you have variables `a`, `b` and experimental function `hoge`,

    >>> a = 1
    >>> b = 2
    >>> e = ExpStock()
    >>> e.append_param(param_1, param_2, param_3)
    >>> @e.expstock
    ... def exp_func(x, y):
    ...     print(a + b)
    >>> exp_func(a, b)

    or at a simple script, you can use `pre_stock` and `post_stock`, too.

    >>> a = 1
    >>> b = 2
    >>> e = ExpStock()
    >>> e.append_param(param_1, param_2, param_3)
    >>> pre_stock()
    >>> print(a + b)
    >>> post_stock()
    """

    def __init__(self,
                 log_dirname='',
                 params=[],
                 memo='',
                 git_check=True,
                 report=False,
                 exp_name='Untitled',
                 dbsave=False):
        """__init__

        :param log_dirname: name of the directory to stock expriments
        :param params: parameters of the function of the experiments.
                       `params` should be a list of tuples.
                       e.g. [('param_1', 1), ('param_2', 'hoge')]
                       At there, `param_1` and `param_2` are the names of variables,
                       and `1` and `hoge` are the variables for experiments
        :param memo:
        :param git_check:
        """
        self.stock_root_dir = 'experiments'
        self.params = params
        self.memo = memo
        self.git_check = git_check
        self.git_head = None
        self.git_diff = None
        self.start_time = None
        self.finish_time = None
        self.exp_name = exp_name
        self.result = ''
        self._set_dirname(log_dirname)
        self.report = report
        self.dbsave=dbsave
        self.dbfile = os.path.join(self.stock_root_dir, 'experiments.db')

    def _set_dirname(self, log_dirname):
        if log_dirname != '':
            self.log_dirname = os.path.abspath(log_dirname)
        else:
            current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
            self.log_dirname = os.path.abspath(
                    os.path.join(
                        self.stock_root_dir,
                        '{}_{}'.format(current_time, self.exp_name)
                        )
                    )

    def set_memo(self, memo):
        self.memo = memo

    def _mk_logdir(self):
        if not os.path.isdir(self.log_dirname):
            os.makedirs(self.log_dirname)

    def _get_machine_info(self):
        """_get_machine_info
        TODO: split to independent module
        TODO: add function to get resource usage
        """
        machine_info = []
        machine_info.append(('system', platform.system()))
        machine_info.append(('node', platform.node()))
        machine_info.append(('release', platform.release()))
        machine_info.append(('version', platform.version()))
        machine_info.append(('machine', platform.machine()))
        machine_info.append(('processor', platform.processor()))
        machine_info.append(('python_version', platform.python_version()))

        return machine_info

    def _get_git_info(self):
        """_get_git_info
        TODO: split to independent module
        :return: (git_head, git_diff)
        :return type: (str, str)
        """
        git_head = subprocess.check_output(['git', 'log', '-n', '1', '--format=%H'])
        git_diff = subprocess.check_output(['git', 'diff'])
        return git_head, git_diff

    def append_param(self, **kwargs):
        flg = 1
        kwargs = locals()['kwargs']
        for obj in kwargs:
            self.params.append((obj, kwargs[obj]))

    def set_memo(self, memo):
        self.memo = memo

    def _write_log(self, filename, value, open_type='w'):
        filepath = os.path.join(self.log_dirname, filename)
        with open(filepath, open_type) as f:
            f.write(value)

    def _write_logs(self, filename, values):
        filepath = os.path.join(self.log_dirname, filename)
        with open(filepath, 'w') as f:
            for value in values:
                if type(value) == tuple:
                    f.write('{} = {}\n'.format(value[0], value[1]))
                elif type(value) == str:
                    f.write(value + '\n')

    def _dbsave_pre(self):
        dbfile = os.path.expanduser('~/.experiments.db')
        self.dbconn = DbConnect(dbfile)
        self.dbconn.insert_into_experiments_pre(self)
        self.dbconn.insert_into_params(self)

    def _dbsave_post(self):
        try:
            self.dbconn.update_experiments(self)
        except NameError:
            pass

    def _create_report(self):
        """_create_report
        TODO: Jinja2を使って書き換える
        """

        filepath = os.path.join(self.log_dirname, 'report.txt')
        text = """
report
========

exp_name: {}
memo: {}

start_time: {}
finish_time: {}

git_head: {}

""".format(
                self.exp_name,
                self.memo,
                self.start_time,
                self.finish_time,
                self.git_head)

        params_text = 'params:\n'
        empty_row = '\n'

        with open(filepath, 'w') as f:
            f.write(text)
            f.write(params_text)
            for param in self.params:
                f.write('{} = {}\n'.format(param[0], param[1]))

            f.write(empty_row)

    def pre_stock(self):
        self._mk_logdir()
        self.machine_info = self._get_machine_info()

        if self.git_check == True:
            self.git_head, self.git_diff = self._get_git_info()
            self._write_log('git_head.txt', self.git_head, 'wb')
            self._write_log('git_diff.txt', self.git_diff, 'wb')
        self._write_log('memo.txt', self.memo, 'w')
        self._write_logs('params.txt', self.params)
        self._write_logs('machine_info.txt', self.machine_info)

        self.start_time = datetime.now()
        self.start_time_str = self.start_time.strftime('%Y/%m/%d %H:%M:%S')
        self._write_log('exec_time.txt', 'start_time: {}\n'.format(self.start_time_str), 'w')
        if self.dbsave == True:
            self._dbsave_pre()

        # Change target of stdout and stderr to log files
        stdout_path = os.path.join(self.log_dirname, 'stdout.txt')
        stderr_path = os.path.join(self.log_dirname, 'stderr.txt')
        sys.stdout = open(stdout_path, 'w')
        sys.stderr = open(stderr_path, 'w')

    def post_stock(self, result=''):
        self.result = result
        sys.stdout.close()
        sys.stdout = sys.__stdout__
        sys.stderr.close()
        sys.stderr = sys.__stderr__
        self.finish_time = datetime.now()
        self.finish_time_str = self.finish_time.strftime('%Y/%m/%d %H:%M:%S')
        self.execution_time = self.finish_time - self.start_time
        self.execution_time_str = str(self.execution_time)
        self._write_log(
                'exec_time.txt',
                'finish_time: {}\nexecution_time: {}\n'.format(
                    self.finish_time_str,
                    self.execution_time_str),
                'a')
        self._write_log('result.txt', result)

        if self.report == True:
            self._create_report()

        if self.dbsave == True:
            self._dbsave_post()

def expstock(e):
    """expstock

    :param e: ExpStock instance
    :return: return value of the decorated function
    """

    def _expstock(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            e.pre_stock()
            result = func(*args, **kwargs)
            e.post_stock(str(result))
            return result
        return wrapper
    return _expstock


