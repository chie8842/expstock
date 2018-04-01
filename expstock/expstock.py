from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from datetime import datetime
import functools
import os
import platform
import sys
import subprocess


class ExpStock(object):
    """ExpStock
    e.g. Now, you have variables `a`, `b` and experimental function `hoge`, 

    >>> a = 1
    >>> b = 2
    >>> e = ExpStock()
    >>> @e.expstock
    ... def exp_func(x, y):
    ...     print(a + b)
    >>> e.append_param(param_1, param_2, param_3)
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

    def __init__(self, log_dirname='', params=[], memos=[], git_check=True):
        """__init__

        :param log_dirname: name of the directory to stock expriments
        :param params: parameters of the function of the experiments.
                       `params` should be a list of tuples.
                       e.g. [('param_1', 1), ('param_2', 'hoge')]
                       At there, `param_1` and `param_2` are the names of variables,
                       and `1` and `hoge` are the variables for experiments
        :param memos:
        :param git_check:
        """
        self.stock_root_dir = 'experiments'
        self.params = params
        self.log_dirname = log_dirname
        self.memos = memos
        self.git_check = git_check
        self._set_dirname(log_dirname)

    def _set_dirname(self, log_dirname):
        if log_dirname != '':
            self.log_dirname = log_dirname
        else:
            current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
            self.log_dirname = os.path.join(self.stock_root_dir, current_time)

    def _mk_logdir(self):
        if not os.path.isdir(self.log_dirname):
            os.makedirs(self.log_dirname)

    def _get_machine_info(self):
        """get_machine_info
        TODO: add function to get resource usage
        """
        machine_info = []
        machine_info.append(('system', platform.system()))
        machine_info.append(('node', platform.node()))
        machine_info.append(('release', platform.release()))
        machine_info.append(('version', platform.version()))
        machine_info.append(('machine', platform.machine()))
        machine_info.append(('processor', platform.processor()))

        return machine_info

    def _get_git_info(self):
        git_head = subprocess.check_output(['git', 'log', '-n', '1', '--format=%H'])
        git_diff = subprocess.check_output(['git', 'diff'])
        return git_head, git_diff


    def append_param(self, **kwargs):
        flg = 1
        kwargs = locals()['kwargs']
        for obj in kwargs:
            self.params.append((obj, kwargs[obj]))

    def append_memo(self, *args):
        for obj in args[0:]:
            self.memos.append(obj)

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

    def pre_stock(self):
        self._mk_logdir()
        machine_info = self._get_machine_info()

        if self.git_check == True:
            git_head, git_diff = self._get_git_info()
            self._write_log('git_head.txt', git_head, 'wb')
            self._write_log('git_diff.txt', git_diff, 'wb')
        self._write_logs('params.txt', self.params)
        self._write_logs('memo.txt', self.memos)
        self._write_logs('machine_info.txt', machine_info)

        start_time = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        self._write_log('exec_time.txt', 'start_time: {}\n'.format(start_time), 'w')

        # Change target of stdout and stderr to log files
        stdout_path = os.path.join(self.log_dirname, 'stdout.txt')
        stderr_path = os.path.join(self.log_dirname, 'stderr.txt')
        sys.stdout = open(stdout_path, 'w')
        sys.stderr = open(stderr_path, 'w')

    def post_stock(self, func_result=''):
        sys.stdout.close()
        sys.stdout = sys.__stdout__
        sys.stderr.close()
        sys.stderr = sys.__stdout__
        finish_time = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        self._write_log('exec_time.txt', 'finish_time: {}\n'.format(finish_time), 'a')
        self._write_log('func_result.txt', func_result)

def expstock(e):
    """expstock

    :param func:
    """

    def _expstock(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            e.pre_stock()
            func_result = func(*args, **kwargs)
            e.post_stock(func_result)
            return func_result
        return wrapper
    return _expstock


