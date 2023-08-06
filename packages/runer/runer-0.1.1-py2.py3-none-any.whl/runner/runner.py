import os
from runer.modules import module_get
import sys
import json
# sys.path.append(os.path.dirname(__file__))
try:
    from modules import Modules, AutoLoadModules
except:
    from .modules import register, AutoLoadModules
else:
    from . import register, AutoLoadModules


if sys.version < '3':
    import urllib
    import httplib

    def urlencode(x):
        return urllib.urlencode(x)

    def httprequest(x, usessl):
        try:
            # conn = httplib.HTTPConnection("api.ip2location.com")
            if (usessl is True):
                conn = httplib.HTTPSConnection("api.ip2location.com")
            else:
                conn = httplib.HTTPConnection("api.ip2location.com")
            conn.request("GET", "/v2/?" + x)
            res = conn.getresponse()
            return json.loads(res.read())
        except:
            return None

    def u(x):
        return x.decode('utf-8')

    def b(x):
        return str(x)
else:
    import urllib.parse
    import http.client

    def urlencode(x):
        return urllib.parse.urlencode(x)

    def httprequest(x, usessl):
        try:
            # conn = http.client.HTTPConnection("api.ip2location.com")
            if (usessl is True):
                conn = http.client.HTTPSConnection("api.ip2location.com")
            else:
                conn = http.client.HTTPConnection("api.ip2location.com")
            conn.request("GET", "/v2/?" + x)
            res = conn.getresponse()
            return json.loads(res.read())
        except:
            return None

    def u(x):
        if isinstance(x, bytes):
            return x.decode()
        return x

    def b(x):
        if isinstance(x, bytes):
            return x
        return x.encode('ascii')


def set_relative_envs(dirs: list):
    ''' set_relative_envs(["utility",])    '''
    d = sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.abspath(".")
    for dir in dirs:
        p = d + os.sep + dir
        if not p in os.environ['PATH']:
            os.environ["PATH"] = p + os.pathsep + os.environ["PATH"]
        # print(os.environ["PATH"])



def run(cmd, *args, **kwargs):
    m = module_get(**kwargs)
    runer = m.get('runer', None)
    envs = m.get("envs", [])
    # param = m.get("param",{})
    # print(m,runer,envs)
    if runer and callable(runer):
        # print(kwargs)
        set_relative_envs(envs)
        try:
            print("aaaaa")
            result = runer(m, cmd, *args, **kwargs)
            print(type(result))
            if isinstance(result, dict):
                m['rc'] = result.get('output', None)
                m['output'] = result.get('output', None)
                m['ignored'] = result.get('ignored', None)
            elif isinstance(result, tuple):
                m['rc'] = result[0]
                if result[0]:
                    m['output'] = result[2]
                else:
                    m['output'] = result[1]
        except Exception as err:
            m['rc'] = -1
            m['output'] = u(err)
            print(err)
        return m
    return {}




def close(cmd, *args, **kwargs):
    pass


def upload(src, dst, *args, **kwargs):
    m = module_get(**kwargs)
    uploader = m.get('uploader', None)
    if uploader and callable(uploader):
        result = uploader(m, src, dst * args, **kwargs)
        return m


class Run(object):
    def __init__(self) -> None:
        super().__init__()

    def __init__(self, *args, **kwargs):
        raise TypeError(
            f"{self.__class__.__name__} does not have a public "
            f"constructor. Instances are returned by SSLContext.wrap_bio()."
        )

    def __init__(self, filename=None, mode='FILE_IO'):
        ''' Creates a database object and opens a file if filename is given

        '''
        self.mode = mode

        if os.path.isfile(filename) == False:
            raise ValueError("The database file does not seem to exist.")

        if filename:
            self.open(filename)

    def __enter__(self):
        if not hasattr(self, '_f') or self._f.closed:
            raise ValueError("Cannot enter context with closed file")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def run(self):

        pass


if __name__ == "__main__":
    AutoLoadModules()
    run("pwd", t="shell")
