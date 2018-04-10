from bottle import route, get, run, template
from bottle import TEMPLATE_PATH, jinja2_template as template
import os
import sqlite3
from dbconnect import DbConnect

dbfile = os.path.expanduser('~/.experiments.db')
host = '0.0.0.0'
port = 8000
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH.append(os.path.join(BASE_DIR, 'template'))


@route('/')
def show_experiments():
    experiments = get_experiments()
    return template('index', experiments=experiments)

#@route("/delete/<todo_id:int>")
#def delete(todo_id):
#    delete_todo(todo_id)
#    return redirect("/")

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
    return experiments

run(host=host, port=port, debug=True, reloader=True)
