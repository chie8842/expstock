#!/usr/bin/env python

from bottle import route, get, run, template, redirect
from bottle import TEMPLATE_PATH, jinja2_template as template
import os
import sqlite3
from expstock.dbconnect import DbConnect

dbfile = os.path.expanduser('~/.experiments.db')
host = '0.0.0.0'
port = 8000
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH.append(os.path.join(BASE_DIR, 'template'))


@route('/')
def show_experiments():
    experiments = get_experiments()
    return template('index', experiments=experiments)

@route('/experiment/<experiment_id:int>')
def show_params(experiment_id):
    experiments = get_experiments()
    params = get_params(experiment_id)
    return template(
            'params',
            experiments=experiments,
            experiment_id=experiment_id,
            params=params)

@route('/delete/<experiment_id:int>')
def delete(experiment_id):
    delete_experiment(experiment_id)
    return redirect('/')

def get_params(experiment_id):
    dbconn = DbConnect(dbfile)
    query = 'select param_id, experiment_id, param_name, value from params where experiment_id = ?'
    params = []
    for row in dbconn.c.execute(query, (experiment_id,)):
        params.append(
                {
                    'param_id': row[0],
                    'experiment_id': row[1],
                    'param_name': row[2],
                    'value': row[3]
                    }
                )
    dbconn.conn.close()
    return params

def get_experiments():
    dbconn = DbConnect(dbfile)
    query = 'select experiment_id, experiment_name, memo, start_time, finish_time, execution_time, git_head, log_dir from experiments'
    #experiments = dbconn.c.execute(query)
    experiments = []
    for row in dbconn.c.execute(query):
        experiments.append(
                {
                    'experiment_id': row[0],
                    'experiment_name': row[1],
                    'memo': row[2],
                    'start_time': row[3],
                    'finish_time': row[4],
                    'execution_time': row[5],
                    'git_head': row[6],
                    'log_dir': row[7]
                    }
                )
    dbconn.conn.close()
    return experiments

def delete_experiment(experiment_id):
    print(experiment_id)
    print(type(experiment_id))
    dbconn = DbConnect(dbfile)
    query = 'delete from experiments where experiment_id = ?'
    dbconn.c.execute(query, (experiment_id,))
    dbconn.conn.commit()
    dbconn.conn.close()

#run(host=host, port=port, debug=True, reloader=True)
