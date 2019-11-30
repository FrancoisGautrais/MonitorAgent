from .httpserver import HTTPServer
from .httprequest import HTTPRequest, HTTPResponse, testurl
from .utils import Callback

class RESTServer(HTTPServer):

    def __init__(self, ip="localhost"):
        HTTPServer.__init__(self, ip)
        self._handlers={}
        self._defaulthandler=None
        self.default(RESTServer._404, self)



    def create(self, req : HTTPRequest, res : HTTPResponse):
        res.end("Create "+str(req.restparams))

    def delete(self, req : HTTPRequest, res : HTTPResponse):
        res.end("delete")

    def update(self, req : HTTPRequest, res : HTTPResponse):
        res.end("update")



    def route(self, methods, url, fct, obj=None, data=None):
        if isinstance(methods, str): methods=[methods]
        for method in methods:
            if not (method in self._handlers):
                self._handlers[method.upper()]={}
            self._handlers[method.upper()][url]=Callback(fct, obj, data)

    def default(self, fct, obj=None, data=None, methods=None ):
        if methods:
            self.route(methods, None, fct, obj, data)
        else:
            self._defaulthandler=Callback(fct, obj, data)

    def _404(self,req : HTTPRequest, res : HTTPResponse):
        res.code=404
        res.msg="Not Found"
        res.end(req.path+" Not found")

    def handlerequest(self, req, res):
        m=req.method
        u=req.path
        if not m in self._handlers: return

        d=self._handlers[m]
        found=None

        for url in d:
            if url:
                args=testurl(url, req.path)
                if args!=None:
                    found=d[url]
                    req.restparams=args



        if found==None:
            if None in d: found=d[None]

        if found==None and self._defaulthandler:
            found=self._defaulthandler

        if found:
            found.call( prependParams=(req, res))
        """
        if found:
            fct, obj, data = found
            if obj:
                if data:
                    fct(obj, req, res, data)
                else:
                    fct(obj, req, res)
            else:
                if data: fct(req, res, data)
                else: fct(req, res)

        """