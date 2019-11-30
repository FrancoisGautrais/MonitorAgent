import json

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


    def hasheader(self, x):
        return x in self.headers

    def headerasint(self, x):
        return int(self.headers[x])

    def headerasstr(self, x):
        return self.headers[x]

    def contentLength(self):
        return self.headerasint("Content-Length") if self.hasheader("Content-Length") else 0

    def contentType(self):
        return self.headerasint("Content-Type")

    def addHeader(self, key, val):
        self.headers[key]=str(val)

    def length(self):
        return self.data if self.data else 0



class HTTPRequest(_HTTP):

    def __init__(self):
        _HTTP.__init__(self)
        self.method=""
        self.version=""
        self.url="/"
        self.path="/"
        self.urlparams={}
        self.restparams={}


    def setUrl(self, url):
        self.path=self.url=url
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

    def length(self):
        return self.data if self.data else 0


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

