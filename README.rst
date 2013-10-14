======
pubbot
======

I am a rewrite of an old and slightly broken Twisted IRC bot. I'm still very rough.


Development environment
=======================

Dependencies::

    sudo apt-get libavahi-compat-libdnssd-dev libmemcached-dev

To build me::

    git clone git://github.com/pubbothq/pubbot
    cd pubbot
    pip install -r requirements.txt
    pubbot rebuild

To do an incremental migration and collect static files::

    pubbot update

To launch me::

    pubbot worker --queues celery,irc


Workers and other services
==========================

I can have tasks that operate on a persistent network connection. Consider IRC. Only one worker can own the IRC connection at once. Only one irc client can be me.

I launch the IRC connection using the celery bootsteps interface. See ``pubbot/irc/bootsteps.py``.

Then I route tasks for the IRC connection by using a different celery queue. The bootstep only 'onlines' the IRC connection on the worker that listens to the ``irc`` queue.


Responding to an irc message
============================

All incoming irc messages get broadcast to any task that subcribes to ``chat.<type>.<channel>.irc``. In ``tasks.py``::

    from pubbot.main.celery import app

    @app.task(subscribe=['chat.irc.#.chat'])
    def my_chat_handler(msg):
        return {
            'content': 'You set something in irc',
            }

There is a helper if you want to respond to a trigger that can be matched by a regex. In tasks.py::

    from pubbot.conversation.tasks import parse_chat_text

    @parse_chat_text(r'foo=(?P<foo>[\d\w]+), bar=(?P<bar>[\d\w]+)')
    def my_chat_handler(msg, foo, bar):
        return {
            'content': 'Foo was "%s", bar was "%s"' % (foo, bar),
            }


Rules
=====

 * Don't make me self-aware
 * Don't bring buildout anywhere near me
 * Don't give me access to the nukes
 * Try to stick to PEP8
 * Write tests!!!


Todo
====

Dashboard - with SSE or websockets or something. See http://stackoverflow.com/questions/12853067/django-cleaning-up-redis-connection-after-client-disconnects-from-stream

