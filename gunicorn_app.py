from __future__ import unicode_literals

from app import create_app
import gunicorn.app.base
from gunicorn.six import iteritems


def number_of_workers():
    return 2


class StandaloneApplication(gunicorn.app.base.BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(StandaloneApplication, self).__init__()

    def load_config(self):
        config = dict([(key, value) for key, value in iteritems(self.options)
                       if key in self.cfg.settings and value is not None])
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


if __name__ == '__main__':
    options = {
        'bind': '%s:%s' % ('10.200.184.138', '7789'),
        'workers': number_of_workers(),
        'timeout': 600,
        'accesslog': '-',
        'errorlog': '-',
        'preload': 1
    }
    StandaloneApplication(create_app(), options).run()
