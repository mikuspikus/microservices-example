from .JobRequester import JobRequester
from .celery import app

from celery import Task
from requests.exceptions import RequestException

# celery -A cqueue worker -l info -P gevent


class CustomTask(Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print(f'{task_id} failed: {exc}')

    def on_success(self, retval, task_id, args, kwargs):
        print(f'{task_id} returned code : *{retval}*')


JREQ = JobRequester()


@app.task(base=CustomTask, autoretry_for=(RequestException,), retry_kwargs={'max_retries': 5}, retry_backoff=True)
def post(payload: dict):
    return JREQ.post(payload)


@app.task(base=CustomTask, autoretry_for=(RequestException,), retry_kwargs={'max_retries': 5}, retry_backoff=True)
def patch(payload: dict):
    return JREQ.patch(payload)


@app.task(base=CustomTask, autoretry_for=(RequestException,), retry_kwargs={'max_retries': 5}, retry_backoff=True)
def delete(payload: dict):
    return JREQ.delete(payload)
