from celery import Celery

app = Celery(
    'cqueue',
    broker = 'redis://localhost:6379/0',
    include = ['cqueue.tasks']
)

if __name__ == "__main__":
    app.start()