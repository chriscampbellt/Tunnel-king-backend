from celery import Celery, Task

app = Celery("apps")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
app.conf.beat_schedule = {}


class BaseTaskWithRetry(Task):
    """
    Automatically retry task in case of failure (up to 3 times). This class
    is intended to be used as a base class for other tasks that need to be
    retried in case of failure.

    Attributes:
        autoretry_for (tuple): The list of exceptions that should be caught and retried.
        retry_kwargs (dict): The maximum number of retries this task can have.
        retry_backoff (int): The time in seconds to wait before retrying the task.
        retry_jitter (bool): Whether to apply exponential backoff when retrying.
    """

    # The list of exceptions that should be caught and retried
    autoretry_for = (Exception, KeyError)

    # The maximum number of retries this task can have
    retry_kwargs = {"max_retries": 3}

    # The time in seconds to wait before retrying the task
    retry_backoff = 5

    # Whether to apply exponential backoff when retrying:
    # When you build a custom retry strategy for your Celery task
    # (which needs to send a request to another service), you should add
    # some randomness to the delay calculation to prevent all tasks from
    # being executed simultaneously resulting in a thundering herd.
    retry_jitter = True


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
