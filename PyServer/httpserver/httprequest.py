import json
import io
import os
from .utils import mime
HTTP_OK=200
HTTP_BAD_REQUEST=400
HTTP_UNAUTHORIZED=401
HTTP_NOT_FOUND=404
HTTP_TEMPORARY_REDIRECT=307

STR_HTTP_ERROR={
    HTTP_OK: "OK",
    HTTP_UNAUTHORIZED: "Unauthorized",
    HTTP_BAD_REQUEST: "Bad request",
    HTTP_NOT_FOUND: "Not Found",
    HTTP_TEMPORARY_REDIRECT: "Temporary redirect"
}

def fromutf8(x): return bytes(x, "utf8")

def stripemptystr(p):
    out=[]
    for v in p:
        if v!='': out.append(v)
    return out



def testurl(template, url):
        url=stripemptystr(url.split("/"))
        template=stripemptystr(template.split("/"))
        args={}

        if len(url) != len(template): return None

        for i in range(0,len(template)):
            v=template[i]
            if v[0]=='#':
                args[v[1:]]=url[i]
            elif v!=url[i]: return None

        return args





class _HTTP:

    def __init__(self):
        self.headers={}
        self.data=None


    def getPostParams(self):
        post=str(self.data)
        out={}
        for k in post.split("&"):
            n=k.find("=")
            key=""
            value=""
            v=""
            if n>0:
                key=k[:n]
                value=k[n+1:]
            else:
                key=k
            out[key]=value
        return out

    def json(self):
        return json.loads(self.data)

    def hasheader(self, x):
        return x in self.headers

    def headerasint(self, x):
        return int(self.headers[x])

    def headerasstr(self, x):
        return self.headers[x]

    def contentLength(self):
        return self.headerasint("Content-Length") if self.hasheader("Content-Length") else 0

    def contentType(self, x=None):
        if x:
            self.headers["Content-Type"]=x
            return x
        else: return self.headerasint("Content-Type")

    def addHeader(self, key, val):
        self.headers[key]=str(val)

    def length(self):
        return len(self.data) if self.data else 0



class HTTPRequest(_HTTP):

    def __init__(self):
        _HTTP.__init__(self)
        self.method=""
        self.version=""
        self.url="/"
        self.path="/"
        self.urlparams={}
        self.restparams={}
        self.cookies={}
        self.filename=""



    def setUrl(self, url):
        self.path=self.url=url
        n=self.url.find("?")
        if n>=0:
            self.path=self.url[:n]
            tmp=self.url[n+1:]
            for k in tmp.split("&"):
                n=k.find("=")
                key=""
                value=""
                v=""
                if n>0:
                    key=k[:n]
                    value=k[n+1:]
                else:
                    key=k
                self.urlparams[key]=value
            self.filename=os.path.basename(self.path)


    def length(self):
        return self.data if self.data else 0

    def setheader(self, key, value):
        self.headers[key]=value
        if key.lower()=="cookie":
            list = value.split(";")
            for x in list:
                x = x.split("=")
                k = x[0].rstrip()
                v = x[1].lstrip() if len(x) > 1 else ""
                self.cookies[k] = v


class HTTPResponse(_HTTP):

    def __init__(self, code=200, jsondata=None):
        _HTTP.__init__(self)
        self.version = "HTTP/1.1"
        self.code=code
        self.msg=STR_HTTP_ERROR[code]
        self._isStreaming=False


    def _setJsonResponse(self, httpcode, code, msg, js):
        self.addHeader("Content-Type", "application/json")
        self.code=httpcode
        self.msg=STR_HTTP_ERROR[httpcode]
        self.data=bytes(json.dumps({ "code": code, "message": msg, "data": js }), "utf8")

    def ok(self, code, msg, js): self._setJsonResponse(HTTP_OK, code, msg, js)
    def unauthorized(self, code, msg, js): self._setJsonResponse(HTTP_UNAUTHORIZED, code, msg, js)
    def bad_request(self, code, msg, js): self._setJsonResponse(HTTP_BAD_REQUEST, code, msg, js)
    def not_found(self, code, msg, js): self._setJsonResponse(HTTP_NOT_FOUND, code, msg, js)
    def temporary_redirect(self, url):
        self.code=HTTP_TEMPORARY_REDIRECT
        self.msg=STR_HTTP_ERROR[HTTP_TEMPORARY_REDIRECT]
        self.headers["Location"]=url
        self.end("")



    def getheadersbytes(self):
        s = fromutf8(self.version + " " + str(self.code) + " " + self.msg + "\r\n")
        for k in self.headers:
            s += fromutf8(k + ": " + self.headers[k] + "\r\n")
        s += fromutf8("\r\n")
        return s

    def isStreaming(self):
        return self._isStreaming

    def serveFile(self, path, urlReq=None):

        fd=None
        try:
            fd=open(path, "rb")
        except Exception as err:
            self.code = HTTP_NOT_FOUND
            self.msg = STR_HTTP_ERROR[HTTP_NOT_FOUND]
            self.contentType("text/plain")
            if urlReq:
                self.end(str(urlReq)+" not found")
            else:
                self.end("File not found : "+str(err))
            return

        #self._isStreaming=True
        self.contentType(mime(path))
        self.headers["Content-Length"] = str(os.stat(path).st_size)
        print("Serving file : "+path)
        self.end(open(path, "rb").read())
        #self.end(open(path, "rb"))

    def getbodybytes(self):
        return self.data




    def end(self, s):
        if isinstance(s, str): s=fromutf8(s)
        self.data=s


