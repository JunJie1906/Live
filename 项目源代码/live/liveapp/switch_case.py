class HttpHandler:
    def handle(self, request):
        methodname = 'do_' + request.request_method
        getattr(self, methodname)(request)

    def do_GET(self, request):
        print('do_GET')

    def do_POST(self, request):
        print('do_POST')

    def do_HEAD(self, request):
        print('do_HEAD')


class Request:
    def __init__(self, method):
        self.request_method = method


if __name__ == '__main__':
    rq = Request('GET')
    HttpHandler().handle(rq)
