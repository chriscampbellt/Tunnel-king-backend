from subprocess import check_call


def run_worker():
    check_call(["celery", "-A", "config", "worker", "--loglevel=info"])
    # os.system("celery -A config worker --loglevel=info")


def run_beat():
    check_call(["celery", "-A", "config", "beat", "--loglevel=info"])
