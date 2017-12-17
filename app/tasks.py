from . import celery

def run_celery():
    celery.worker_main(['', '-B'])

@celery.task()
def example_task():
    print("EXAMPLE")
