# -*- coding: utf-8 -*-
"""
Created on Wed May 27 22:47:19 2015

@author: Administrator
"""

import web

urls = ("/.*", "hello")
app = web.application(urls, globals())

class hello:
    def GET(self):
        return 'Hello, world!'

if __name__ == "__main__":
    app.run()