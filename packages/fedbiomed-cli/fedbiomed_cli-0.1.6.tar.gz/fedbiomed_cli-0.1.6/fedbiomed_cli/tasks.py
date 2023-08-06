from typing import Union

import torch
import validators
import tempfile
from persistqueue import Queue
from threading import Thread
from time import sleep

from . import QUEUE_DIR, CLIENT_ID
from .json import deserialize_msg

queue = Queue(QUEUE_DIR)


def run_model_training(msg):
    if isinstance(msg, str) or isinstance(msg, bytes):
        msg = deserialize_msg(msg)

    from .mqtt import HistoryLogger
    logger = HistoryLogger(job_id=msg['job_id'])

    # Get arguments for the model and training
    model_kwargs = msg.get('model_args') or {}
    training_kwargs = msg.get('training_args') or {}
    repository_url = msg.get('repository_url')
    hub_function = msg.get('hub_function')

    assert repository_url is not None, 'URL for repository not found.'
    assert validators.url(repository_url), 'Repository URL is not valid.'
    assert hub_function is not None, 'function for loading the model and training routine was not found in message.'
    assert isinstance(hub_function, str), '`hub_function` must be a string corresponding to the function to load the ' \
                                          'model and the training routine in `hubconf.py`.'

    # Download model, training routine, execute it and return model results
    from git import Repo
    from .utils.requests import upload

    with tempfile.TemporaryDirectory() as f:
        # Clone repository
        Repo.clone_from(repository_url, f)

        # Load model using hub
        Model, training_routine = torch.hub.load(f, hub_function, source='local')

        # If `Model` is a class and not an instantiated model
        if isinstance(Model, type):
            model = Model(**model_kwargs)
        else:
            model = Model

        # Load model initialization parameters
        try:
            from torch.utils.model_zoo import load_url
            model_params = load_url(msg['initial_params'])
            model.load_state_dict(model_params)
        except KeyError:
            pass

        # Run the training routine
        results = {}

        try:
            training_kwargs_with_history = dict(logger=logger, **training_kwargs)
            training_routine(model, **training_kwargs_with_history)
        except TypeError as e:
            print(e)
            training_routine(model, **training_kwargs)

        results['job_id'] = msg['job_id']
        results['model_params'] = model.state_dict()
        results['history'] = logger.history
        results['client_id'] = CLIENT_ID

        # Upload results
        res = upload(results)
        return res


def add_task(task: dict):
    queue.put(task)


def task_manager():
    import traceback
    from .mqtt import reply_to_server
    while True:
        item = queue.get()

        try:
            print('[QUEUE] Item:', item)
            msg = run_model_training(item)
            reply_to_server(msg)

            queue.task_done()
        except Exception as e:
            msg = {'success': False, 'msg': str(e), 'error': type(e).__name__, 'traceback': traceback.format_exc()}
            reply_to_server(msg)
            # queue.put(item)
        sleep(2)


def manage_tasks():
    t = Thread(target=task_manager)
    t.daemon = True
    t.start()
