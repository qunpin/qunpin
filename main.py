#!/usr/bin/env python
#coding:utf-8

import os.path

import tornado.database
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
from tornado.options import define,options
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

import models as  m
import config # 数据库配置 以及其他配置

define("port", default=8888, help="run on the given port", type=int)

engine = create_engine(config.DB_CONFIG)
Session = sessionmaker(bind=engine)
db = Session()




class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", HomeHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            cookie_secret="dev",
        #    login_url="/admin/login",
            autoescape=None,
            debug=config.DEBUG,
        )
        tornado.web.Application.__init__(self, handlers, **settings)



class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        users = db.query(m.User).all()
        self.render("dev_home.html",users=users)

    def post(self):
        name = self.get_argument('name',None)
        if name:
            new_user = m.User(name=name)
            db.add(new_user)
            db.commit()

        self.redirect('/')



def main():
    tornado.options.parse_command_line()
    #http_server = tornado.httpserver.HTTPServer(Application())
    #http_server.listen(options.port)
    application = Application()
    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
