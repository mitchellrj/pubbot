from celery import current_app, group, chord

from match import Subscriptions


def get_tasks_with_subscription(subscription):
    """
    Find all celery tasks that subscribe to a given channel
    """
    for task in current_app.tasks.values():
        # FIXME: The intention is to create a differet default task that
        # precompiles channels to a Subscriptions object for us
        if Subscriptions(getattr(task, 'subscribe', [])).match(subscription):
            yield task


def get_group_for_subscriptions(subscription):
    return group(t.subtask(kwargs) for t in get_tasks_with_subscription(kwargs['kind']))


def broadcast(**kwargs):
    """
    Invoke all tasks that subscribe to channels matching the channel on msg
    """
    return get_group_for_subscriptions(**kwargs).apply_async()

