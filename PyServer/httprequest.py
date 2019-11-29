import json

def fromutf8(x): return bytes(x, "utf8")

class _HTTP:

    def __init__(self):
        self.headers={}
        self.data=None


    def hasheader(self, x):
        return x in self.headers

    def headerasint(self, x):
        return int(self.headers[x])

    def headerasstr(self):
        return self.headers[x]

    def contentLength(self):
        return self.headerasint("Content-Length") if self.hasheader("Content-Length") else 0

    def contentType(self):
        return self.headerasint("Content-Type")

    def addHeader(self, key, val):
        self.headers[key]=str(val)



class HTTPRequest(_HTTP):

    def __init__(self):
        _HTTP.__init__(self)
        self.method=""
        self.version=""
        self.url="/"
        self.path="/"
        self.urlparams={}

    def setUrl(self, url):
        self.url=url
        n=self.url.find("?")
        if n>=0:
            self.path=self.url[:n]
            tmp=self.url[n+1:]
            print("tmp=", tmp)
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




class HTTPResponse(_HTTP):

    def __init__(self, code=200, msg="OK", version="HTTP/1.1"):
        _HTTP.__init__(self)
        self.code = code
        self.version = version
        self.msg = msg

    def setJsonResponse(self, js):
        if not isinstance(js, str):
            js=json.dumps(js)
        self.addHeader("Content-Type", "application/json")
        self.data=bytes(js, "utf8")

    def getbytes(self):
        s=fromutf8(self.version+" "+str(self.code)+""+self.msg+"\r\n")
        for k in self.headers:
            s+=fromutf8(k+": "+self.headers[k]+"\r\n")
        s+=fromutf8("\r\n")
        if self.data:
            s+=self.data
        return s

    def end(self, s):
        if isinstance(s, str): s=fromutf8(s)
        self.data=s

