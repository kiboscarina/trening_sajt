
def CELERY_DELAY(task, *args):
    if hasattr(task, 'delay'):
        task.delay(*args)
    else:
        print('--------------- no delay on specified task')
        
def CELERY_ASYNC(task, **kwargs):
    if hasattr(task, 'apply_async'):
        task.apply_async(**kwargs)
    else:
        print('--------------- no apply_async on specified task')