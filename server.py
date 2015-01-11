import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.gen
import tornadoredis
from tornado import gen
import redis
import brukva
import docker
from docker import client
from CodernityDB.database import Database




#sudo docker -H tcp://0.0.0.0:2375 -H unix:///var/run/docker.sock -d &
#http://docker-py.readthedocs.org/en/latest/change_log/
#https://www.digitalocean.com/community/tutorials/how-to-install-and-use-redis
#http://marios.io/2013/01/15/truly-async-with-tornado/
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", UserHandler),
            (r"/r", RedisHandler),
      (r"/r2", MainHandler),
      (r"/r3", MainHandlerAsync),
        ]
        tornado.web.Application.__init__(self, handlers)


class UserHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine    
    def get(self):
        self.write("Hello")
#        user = AsyncUser()
#        response = yield (user.save())

#        response2 = yield (user.send_email())
#        response3 = yield (user.social_api())
#        self.finish()

class RedisHandler(tornado.web.RequestHandler):
#    @tornado.web.asynchronous
 #   @tornado.gen.engine
    def get(self):
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        k=r.get('foo')
        self.write(k)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        from docker import Client
        cli=Client(base_url='tcp://127.0.0.1:2375')
        for k,v in cli.version().items():
            self.write(k + "             " +   v)
            self.write("\n")

class MainHandlerAsync(tornado.web.RequestHandler):
    @tornado.web.asynchronous

    @gen.engine
    def get(self):
        req = httpclient.HTTPRequest(pretend_service_url, method='GET')
        client = tornado.httpclient.AsyncHTTPClient()
        # don't let the yield call confuse you, it's just Tornado helpers to make
        # writing async code a bit easier. This is the same as doing
        # client.fetch(req, callback=_some_other_helper_function)
        response = yield gen.Task(client.fetch, req)
        ### do something with the response ###
        self.finish()

def main():
    http_server = tornado.httpserver.HTTPServer(Application())
    PORT = 8001
    print("serving at port", PORT)
    http_server.listen(PORT)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()

