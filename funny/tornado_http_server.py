import tornado.ioloop
import tornado.web
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor



class MainHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(10)

    @tornado.gen.coroutine
    def get(self):
        ret = yield self._request_get()
        self.write(ret)

    @run_on_executor
    def _request_get(self):
        return "Hello, world"

if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/", MainHandler),
    ])
    application.listen(8080)
    tornado.ioloop.IOLoop.current().start()