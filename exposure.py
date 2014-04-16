#!/usr/bin/env python
import gc, sys, os
from tornado import ioloop, web, autoreload, template
import simplejson as json
import pandas as pd


def _find_name(obj):
    frame = sys._getframe()
    for frame in iter(lambda: frame.f_back, None):
        frame.f_locals
    result = []
    for referrer in gc.get_referrers(obj):
        if isinstance(referrer, dict):
            for k, v in referrer.iteritems():
                if v is obj:
                    result.append(k)
    return result[0]

INDEX_TEMPLATE = template.Template('''
<html><head>
    <title>Exposure</title>
    <link rel="stylesheet" href="//netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css">
</head>
<body>
<div class="container">
    <h2>Exposure</h2><p>overview of exposed objects:</p>
    <table class="table table-bordered table-hover">
      <thead><tr><th>Exposed object</th><th>Type</th></tr></thead>
      {% for obj in objects %}
        {% block obj %}
          <tr>
            <td><a href="/ex/{{ escape(obj['name']) }}">{{ escape(obj["name"]) }}</a></td>
            <td>{{ escape(obj["name"]) }}</td>
          </tr>
        {% end %}
      {% end %}
    </table>
</div>
</body></html>''')

class Exposure(object):
    """Easily expose your python objects as a read-only REST service"""

    def __init__(self, host='localhost', port=8888, static_files='static', objects=[]):
        self.host = host
        self.port = int(port)
        self.url = 'http://{}:{}'.format(host, port)
        self.static_files = str(static_files)
        Exposure.exposed = { _find_name(obj):obj for obj in objects }

    def add(self, obj, name=None):
        '''adds an object to be exposed'''
        if not name:
            name = _find_name(obj) # guess
        print 'ADD: {}::{}'.format(name, obj)
        Exposure.exposed[name] = obj

    class MainHandler(web.RequestHandler):
        ''' serves index.html'''
        def get(self):
            objects = [{'name': name, 'type': type(obj).__name__} for name, obj in Exposure.exposed.iteritems()]
            self.finish(INDEX_TEMPLATE.generate(objects=objects))

    class ExposureHandler(web.RequestHandler):
        '''exposes objects'''
        def get(self, obj_name):
            obj = Exposure.exposed[obj_name]
            if type(obj) in [pd.Series, pd.DataFrame]:
                self.write(obj.to_json())
            else:
                self.write(json.dumps(obj, use_decimal=True))

    class ExposureQueryHandler(web.RequestHandler):
        '''exposes queries to objects'''
        def get(self, obj_name, query):
            try:
                obj = Exposure.exposed[obj_name]

                if type(obj) in [tuple, list, dict, pd.Series]:
                    if type(obj) in [tuple, list, pd.Series]:
                        query = int(query)
                    self.write(json.dumps(obj[query], use_decimal=True))
                elif type(obj) is pd.DataFrame:
                    self.write(obj.query(query).to_json())

            except Exception, e:
                self.set_status(400)
                self.write(json.dumps(e))

    def start(self):
        '''start REST server'''
        application = web.Application([
            (r'/',              Exposure.MainHandler),
            (r'/ex/(.*)/(.*)',  Exposure.ExposureQueryHandler),
            (r'/ex/(.*)',       Exposure.ExposureHandler),
            (r'/static/(.*)',   web.StaticFileHandler, {'path': self.static_files+'/'})
        ], gzip=True)

        application.listen(self.port)
        # autoreload files in static_files directory
        autoreload.start()
        for dir, _, files in os.walk(self.static_files):
            [autoreload.watch(dir + '/' + f) for f in files if not f.startswith('.')]
        print 'listening on {} ...'.format(self.port)
        ioloop.IOLoop.instance().start()
