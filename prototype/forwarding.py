import tornado
import tornado.web
import tornado.httpserver
import tornado.httpclient


class ForwardingRequestHandler (tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.forward()

    def handle_response(self, response):
        print('Handle response: {0}'.format(response))
        if response.error and not isinstance(response.error, tornado.httpclient.HTTPError):
            print('     ...response error seen: {0}'.format(response.error))
            self.set_status(500)
            self.write("Internal server error: '{0}'\n".format(str(response.error)))
            self.finish()
        else:
            print('     ...response success seen: {0}'.format(response.code))
            self.set_status(response.code)
            for header in ("Date", "Cache-Control", "Server", "Content- Type", "Location"):
                v = response.headers.get(header)
                if v:
                    self.set_header(header, v)
            if response.body:
                self.write(response.body)
            self.finish()

    def forward(self, port=None, host=None):
        try:
            print('In forward() try block...')
            tornado.httpclient.AsyncHTTPClient().fetch(
                request = "http://www.google.com",
                callback=self.handle_response)
                # tornado.httpclient.HTTPRequest(
                #     #url="%s://%s:%s%s" % (
                #     #    self.request.protocol, host or "127.0.0.1", port or 80, self.request.uri),
                #     url = "http://www.google.com",
                #     method=self.request.method,
                #     body=self.request.body,
                #     headers=self.request.headers,
                #     follow_redirects=False),
                # self.handle_response)
        except tornado.httpclient.HTTPError, x:
            print('Error http: {0}'.format(x))
            if hasattr(x, response) and x.response:
                self.handle_response(x.response)
        # except tornado.httpclient.CurlError, x:
        #     print('Error curl: {0}'.format(x))
        #     self.set_status(500)
        #     self.write("Internal server error:\n" + ''.join(traceback.format_exception(*sys.exc_info())))
        #     self.finish()
        except Exception, x:
            print('Error misc: {0}'.format(x))
            self.set_status(500)
            # self.write("Internal server error:\n" + ''.join(traceback.format_exception(*sys.exc_info())))
            self.finish()


if __name__ == '__main__':
    application = tornado.web.Application([
        ('/$', ForwardingRequestHandler, ),
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8000)
    print('Starting up server...')
    tornado.ioloop.IOLoop.instance().start()
