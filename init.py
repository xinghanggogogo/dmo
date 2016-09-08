#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.ioloop

from tornado.options import define, options
define('port', default=9000, help='run on this port', type=int)
define('debug', default=True, help='enable debug mode')
options.parse_command_line()

import app #app.py

def runserver():
    app.run() #app.py run()
    loop = tornado.ioloop.IOLoop.instance()
    loop.start()

if __name__ == '__main__':
    runserver()
