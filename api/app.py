import celery.states as states
from flask import Flask, Response
from flask import url_for, jsonify
from worker import celery

dev_mode = True
app = Flask(__name__)


@app.route('/add/<int:param1>/<int:param2>')
def add(param1: int, param2: int) -> str:
    task = celery.send_task('tasks.add', args=[param1, param2], kwargs={})
    response = f"<a href='{url_for('check_task', task_id=task.id, external=True)}'>check status of {task.id} </a>"
    return response


@app.route('/check/<string:task_id>')
def check_task(task_id: str) -> str:
    res = celery.AsyncResult(task_id)
    if res.state == states.PENDING:
        return res.state
    else:
        return str(res.result)


@app.route('/health_check')
def health_check() -> Response:
    return jsonify("OK")
    
@app.route('/')
def main() -> Response:
    return str("Usages:<p>/</p><p>/add/&lt;int:param1&gt;/&lt;int:param2&gt;</p><p>/check/&lt;string:task_id&gt;</p><p>/health_check</p>")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
