from .httpserver import HTTPServer
from .httprequest import HTTPRequest, HTTPResponse, testurl
from .utils import Callback
import os

class RESTServer(HTTPServer):

    def __init__(self, ip="localhost"):
        HTTPServer.__init__(self, ip)
        self._handlers={}
        self._defaulthandler=None
        self.default(RESTServer._404, self)
        self.static_dirs={}

    def static(self, baseUrl, dir, authcb=None, needauthcb=None):
        dir=os.path.abspath(dir)
        if dir[-1]=="/": dir=dir[:-1]
        if baseUrl[-1]=="/": baseUrl=baseUrl[:-1]
        self.static_dirs[baseUrl]=(dir, needauthcb, authcb)


    def route(self, methods, url, fct, obj=None, data=None):
        if isinstance(methods, str): methods = [methods]
        for method in methods:
            if not (method in self._handlers):
                self._handlers[method.upper()] = {}
            self._handlers[method.upper()][url] = Callback(fct, obj, data)

    def default(self, fct, obj=None, data=None, methods=None):
        if methods:
            self.route(methods, None, fct, obj, data)
        else:
            self._defaulthandler = Callback(fct, obj, data)

    def _404(self, req: HTTPRequest, res: HTTPResponse):
        res.code = 404
        res.msg = "Not Found"
        res.contentType("text/plain")
        res.end(req.path + " Not found")

    def handlerequest(self, req, res):
        m = req.method
        u = req.path
        if not m in self._handlers: return

        d = self._handlers[m]
        found = None

        for url in d:
            if url:
                args = testurl(url, req.path)
                if args != None:
                    found = d[url]
                    req.restparams = args

        if found == None:
            p=req.path
            for base in self.static_dirs:
                if p.startswith(base):
                    dir, needeauth, auth = self.static_dirs[base]
                    p=p[len(base):]
                    if len(p)==0: p="index.html"
                    if p[0]=="/": p=p[1:]
                    path=os.path.join(dir,p)
                    if  (not auth) or (not needeauth) or (not needeauth.call((req, res))) or auth.call((req, res)):
                        res.serveFile( path, base+"/"+p)
                    return

        if found == None:
            if None in d: found = d[None]

        if found == None and self._defaulthandler:
            found = self._defaulthandler

        if found:
            found.call(prependParams=(req, res))




