"""
A web application framework.

Strongly influenced by Aaron Swartz' "anti-framework" `web.py` this
library aims to cleanly abstract low-level web functionality through
a Pythonic API.

>   Think about the ideal way to write a web app. Write the
>   code to make it happen.

--- Aaron Swartz

"""

from base64 import b64encode, b64decode
import collections
# import errno
import getpass
import hashlib
import inspect
import os
import pkg_resources
import pathlib
import pprint
import re
import secrets
import shutil
import signal
import sys
import time
from time import sleep
import urllib

import Crypto.Random
import Crypto.Random.random
import gevent.pywsgi
import pendulum
import sh
import unidecode
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from understory import kv
from understory import mm
from understory.mm import Template
from understory import sql

from ..agent import parse, apply_dns, cache
from ..response import (Status,  # noqa
                        OK, Created, Accepted, NoContent, MultiStatus,
                        Subscription,
                        Found, SeeOther, PermanentRedirect,
                        BadRequest, Unauthorized, Forbidden, NotFound,
                        MethodNotAllowed, Conflict, Gone)
from .letsencrypt import generate_cert
from .newmath import nbencode, nbdecode, nbrandom, nb60_re
from .passphrases import generate_passphrase, verify_passphrase
from .util import tx, header, json, JSONEncoder, shift_headings

import warnings  # mf2py's beautifulsoup's unspecified parser -- force lxml?
warnings.simplefilter("ignore")

random = secrets.SystemRandom()

__all__ = ["application", "serve", "anti_csrf", "form", "secure_form",
           "get_nonce", "get_token", "best_match", "sessions",
           "require_auth", "tx", "kv", "header",
           "Application", "Resource", "nbencode", "nbdecode", "nbrandom",
           "Template", "config_templates", "generate_cert",
           "get_integrity_factory", "utcnow", "JSONEncoder",
           "default_session_timeout", "textslug", "get_host_hash",
           "config_servers", "b64encode", "b64decode", "timeslug",
           "enqueue", "run_redis", "kill_redis", "get_apps", "nb60_re",
           "generate_passphrase", "verify_passphrase", "sleep", "random",
           "session_table_sql", "resume_session"]

kvdb = kv.db("web", ":", {"auth:secret": "string",
                          "auth:nonces": "set",
                          "reload-lock": "string",
                          "sessions:{session_id}": "string",
                          "sessions:{session_id}:data": "string"},
             session_id=r"[a-z0-9]{,65}")
config_templates = mm.templates(__name__)
methods = ["head", "get", "post", "put", "delete", "options", "patch",
           "propfind"]
applications = {}
default_session_timeout = 86400


def ismethod(obj):
    """"""
    return (inspect.ismethod(obj) and obj.__name__.isupper() and
            obj.__name__.lower() in methods)


def application(name, *wrappers, prefix=r"", mount_prefix=r"",
                host=None, **path_args):
    if name in applications:
        app = applications[name]
        app.prefix = prefix  # FIXME does this have a side effect?
        app.add_wrappers(*wrappers)
        app.add_path_args(**path_args)
    else:
        app = Application(name, *wrappers, host=host, **path_args)
        app.reload_config()
        app.prefix = prefix
        app.mount_prefix = mount_prefix
        applications[name] = app
    return app


def get_host_hash(path):
    return hashlib.sha256(str(path.resolve()).encode("utf-8")).hexdigest()[:6]


def setup_servers(root, app, bot):
    """Initialize and configure servers (web, nginx, redis, supervisor)."""
    root = pathlib.Path(root).resolve()
    root_hash = get_host_hash(root)
    env = pathlib.Path(os.getenv("VIRTUAL_ENV"))
    root.mkdir()
    (root / "etc").mkdir()

    with (root / "etc/redis.conf").open("w") as fp:
        fp.write(str(config_templates.redis(root)))
    with (root / "etc/supervisor.conf").open("w") as fp:
        fp.write(str(config_templates.supervisor(root, root_hash,
                                                 getpass.getuser(),
                                                 env, app, bot)))
    with (root / "etc/nginx.conf").open("w") as fp:
        fp.write(str(config_templates.nginx(root_hash)))

    (root / "run").mkdir(parents=True)
    with (root / "etc/tor_stem_password").open("w") as fp:
        fp.write(str(random.getrandbits(100)))

    session_salt = Crypto.Random.random.randint(10**63, 10**64)
    cfg = {"root": str(root), "watch": str(env / "src"),
           "session": {"salt": str(session_salt)}}
    with (root / "etc/web.conf").open("w") as fp:
        json.dump(cfg, fp, indent=4, sort_keys=True)
    return root


# TODO rename
def config_servers(root, web_server_config_handler=None):
    """Update symlinks to config files and reload nginx."""
    root_hash = get_host_hash(root)
    # TODO FIXME XXX figure out what to do here...
    nginx_conf = pathlib.Path("/home/gaea/detritus/nginx/conf")
    sh.ln("-sf", (root / "etc/nginx.conf").resolve(),
          nginx_conf / "nginx.conf")
    if web_server_config_handler:
        web_server_config_handler(nginx_conf / "conf.d", root_hash)
    sh.sudo("ln", "-sf", (root / "etc/supervisor.conf").resolve(),
            "/etc/supervisor/conf.d/{}.conf".format(root_hash))


def serve(app_name, processes=2, threads=20, max_requests=100, lifespan=60):
    """Serve callable `app` at given `port`."""
    # TODO use file sockets specified as relative locations or in environ vars
    # master_fifo = os.path.expanduser("~/.web/{}-uwsgictl".format(app))

    # __import__(app)
    # for app_pkg, apps in get_apps().items():
    #     for app_name, app_instance in apps:
    #         if app == app_name:
    #             print(dir(app_pkg))
    app = applications[app_name]

    def process(line):
        # TODO log everything, filter display to relevant
        print(line.rstrip())

    root = pathlib.Path(app.cfg["root"])
    watch = app.cfg.get("watch")
    bg = False
    if watch:
        bg = True
    # XXX app_port = 8080
    proc = sh.uwsgi("-H", os.getenv("VIRTUAL_ENV"), "-w",
                    "{}.__web__:app".format(app_name),
                    "--uwsgi-socket", root / "run/web.sock",
                    "--chmod-socket=666",
                    # "--http-socket", ":{}".format(app_port),
                    "--logformat=%(method) %(host)%(uri) %(status)",
                    "--ignore-sigpipe",
                    "--max-requests", max_requests,
                    "--max-worker-lifetime", 60 * lifespan,
                    # "--master-fifo", master_fifo,
                    # "--enable-threads",
                    "-M", "-p", processes, "--async", threads, "--ugreen",
                    "--stats", root / "run/web-stats.sock",
                    # XXX "--stats", "127.0.0.1:1717", "--stats-http",
                    _bg=bg, _err=process)
    # logging.basicConfig(level=logging.INFO,
    #                     format='%(asctime)s - %(message)s',
    #                     datefmt='%Y-%m-%d %H:%M:%S')
    if watch:
        event_handler = EventHandler(proc)
        observer = Observer()
        observer.schedule(event_handler, str(watch), recursive=True)
        observer.start()
        try:
            proc.wait()
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
        proc.signal(signal.SIGQUIT)


# def serve2(app_name):
#     """Serve callable `app` at given `port`."""
#     app = applications[app_name]
#
#     def process(line):
#         # TODO log everything, filter display to relevant
#         print(line.rstrip())
#
#     app_port = 8080
#     proc = sh.uwsgi("-H", os.getenv("VIRTUAL_ENV"), "-w",
#                     "{}.__web__:app".format(app_name),
#                     "--http-socket", ":{}".format(app_port),
#                     "--logformat=%(method) %(host)%(uri) %(status)",
#                     "--ignore-sigpipe",
#                     # "--master-fifo", master_fifo,
#                     # "--enable-threads",
#                     # XXX "--stats", "127.0.0.1:1717", "--stats-http",
#                     _bg=True, _err=process)
#     def quit():
#         proc.signal(signal.SIGQUIT)
#     # proc.wait()
#     return quit


class EventHandler(FileSystemEventHandler):

    """restarts server when source directory changes"""

    def __init__(self, server_proc):
        self.server_proc = server_proc
        super(EventHandler, self).__init__()

    def _restart_server(self, event):
        if event.src_path.endswith(".py"):
            if kvdb:
                while kvdb["reload-lock"]:
                    time.sleep(2)
            self.server_proc.signal(signal.SIGHUP)

    # on_moved = on_created = on_deleted =
    on_modified = _restart_server

    # def on_moved(self, event):
    #     super(EventHandler, self).on_moved(event)
    #     # what = 'directory' if event.is_directory else 'file'
    #     # logging.info("Moved %s: from %s to %s", what, event.src_path,
    #     #              event.dest_path)

    # def on_created(self, event):
    #     super(EventHandler, self).on_created(event)
    #     # what = 'directory' if event.is_directory else 'file'
    #     # logging.info("Created %s: %s", what, event.src_path)

    # def on_deleted(self, event):
    #     super(EventHandler, self).on_deleted(event)
    #     # what = 'directory' if event.is_directory else 'file'
    #     # logging.info("Deleted %s: %s", what, event.src_path)

    # def on_modified(self, event):
    #     super(EventHandler, self).on_modified(event)
    #     # what = 'directory' if event.is_directory else 'file'
    #     # logging.info("Modified %s: %s", what, event.src_path)


def get_apps():
    """"""
    apps = collections.defaultdict(list)
    for ep in pkg_resources.iter_entry_points("web.apps"):
        try:
            handler = ep.load()
        except ModuleNotFoundError:
            print(f"couldn't load entry point: {ep}")
            continue
        try:
            raw_meta = ep.dist.get_metadata("PKG-INFO")
        except FileNotFoundError:
            raw_meta = ep.dist.get_metadata("METADATA").partition("\n\n")[0]
        ep.dist.metadata = dict(line.partition(": ")[0::2]
                                for line in raw_meta.splitlines())
        apps[ep.dist].append((ep.name, handler, ep.module_name, ep.attrs))
    return apps


def get_app(object_reference):
    """"""
    for ep in pkg_resources.iter_entry_points("web.apps"):
        if f"{ep.module_name}:{ep.attrs[0]}" == object_reference:
            return ep.name, ep.handler


def best_match(handlers, *args, **kwargs):
    """"""
    handler_types = [handler for handler, _ in handlers.items()]
    best_match = tx.request.headers.accept.best_match(handler_types)
    tx.response.headers.content_type = best_match
    return dict(handlers)[best_match](*args, **kwargs)


def get_integrity_factory(template_pkg):
    """Generate integrity hashes on the fly for local assets."""
    def handler(fn):
        static_assets_dir = pathlib.Path(template_pkg).parent.parent / "static"
        return sh.base64(sh.xxd(sh.sha256sum("-b", static_assets_dir / fn),
                                "-r", "-p")).strip()
    return handler


def utcnow():
    return pendulum.now("UTC")


_punct_re = r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+'
_punct_split = re.compile(_punct_re).split


def textslug(title, delim="_", lower=True):
    """
    return a path slug containing a normalized version of `title`

    Defaults to delimiting words by "_" and enforcing all lowercase.
    Also makes intelligent path-friendly replacements (e.g. "&" to "and").

        >>> textslug("Surfing with @Alice & @Bob!")
        "surfing_with_alice_and_bob"

    """
    # TODO use formal normalization tooling:

    #   import unicodedata
    #   normalized = unicodedata.normalize("NFKC", title)

    #   title.encode("punycode")

    #   from confusable_homoglyphs import confusables
    #   bool(confusables.is_dangerous(title))

    result = []
    if lower:
        title = title.lower()
    title = title.replace(" & ", " and ")
    for word in _punct_split(title):
        result.extend(unidecode.unidecode(word).split())
    slug = delim.join(result)
    slug = slug.replace(":", "")  # XXX REMOVE WHEN MENTIONS REMOVED KV
    return slug


def timeslug(dt):
    """
    return a path slug containing date and time

    Date is encoded in standard YYYY/MM/DD form while the time is encoded
    as the NewBase60 equivalent of the day's centiseconds.

    """
    centiseconds = ((((dt.hour * 3600) + (dt.minute * 60) + dt.second) * 100) +
                    round(dt.microsecond / 10000))
    return "{}/{}/{}/{}".format(dt.year, dt.format("MM"), dt.format("DD"),
                                nbencode(centiseconds, 4))


def anti_csrf(handler):
    """"""
    # TODO csrf-ify forms with class name "x-secure"
    yield


def get_nonce():
    """"""
    return nbrandom(32)


def get_token(nonce):
    """
    return a token for given `secret` and `nonce`

    secret can be a string or a Redis instance in which key `secret`

    """
    secret = str(kvdb["auth:secret"])
    return hashlib.sha1(bytes(secret + nonce, "utf-8")).hexdigest()


def secure_form(*args, **kwargs):
    """"""
    args = list(args) + ["token", "nonce"]
    form = Form(*args, **kwargs)
    if not kvdb["auth:nonces"].add(form["nonce"]):
        raise OK("given `nonce` has already been used")
    if get_token(form["nonce"]) != form["token"]:
        raise OK("invalid `token` for given `nonce`")
    form.pop("token")
    form.pop("nonce")
    return form


class Form(dict):

    """

    """

    def __init__(self, *requireds, **defaults):
        _data = tx.request.body._data
        for required in requireds:
            if required not in _data:
                err_msg = "required `{}` not present in request"
                raise BadRequest(err_msg.format(required))
        super(Form, self).__init__(defaults)
        if isinstance(_data, str):
            return  # TODO FIXME what to do here? fix for Jupyter
        for key in _data.keys():
            if isinstance(_data[key], list):
                items = []
                for item in _data[key]:
                    if item.filename:
                        items.append(File(item.filename, item))
                    else:
                        items.append(item.value)
                self[key] = items
            else:
                if _data[key].filename:
                    value = File(key, _data[key])
                else:
                    value = _data.getfirst(key)
                if isinstance(defaults.get(key), list):
                    value = [value]
                self[key] = value

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError as e:
            raise AttributeError(e)

    def __setattr__(self, name, value):
        self[name] = value


form = Form


class File:

    """

    """

    def __init__(self, name, fileobj):
        self.name = name
        self.fileobj = fileobj

    def save(self, filepath, **options):
        """

        """
        filepath = pathlib.Path(filepath)
        # TODO handle required
        required = options.pop("required", False)
        if required:
            requireds = [required]
            if required == "jpg":
                requireds.append("jpeg")
            if not self.fileobj.filename.lower().endswith(tuple(requireds)):
                raise BadRequest("`{}` not `{}`".format(self.name, required))
        # self._ensure_dir_exists(dirpath)
        self.fileobj.file.seek(0)
        # while True:
        #     sugar = nbrandom(2)
        #     path = dirpath / self.name
        #     path = path.parent / "{}-{}{}".format(path.stem, sugar,
        #                                           path.suffix)
        if required:
            suffix = "." + required
        else:
            suffix = pathlib.Path(self.fileobj.filename).suffix
        filepath = filepath.with_suffix(suffix)
        if filepath.exists():
            raise FileExistsError("{} already exists".format(filepath))
        with filepath.open("wb") as fp:
            shutil.copyfileobj(self.fileobj.file, fp)
        return filepath

    # def _ensure_dir_exists(self, dirpath):
    #     try:
    #         os.makedirs(str(dirpath))
    #     except OSError as exc:
    #         if exc.errno == errno.EEXIST and dirpath.is_dir():
    #             pass
    #         else:
    #             raise


class Resource:

    """

    """

    def __init__(self, **kwargs):
        self.__dict__ = dict(kwargs)
        # XXX self._resources = ResourceData()
        # XXX for resource_name, value in kwargs.items():
        # XXX     table, _, column = resource_name.partition("_")
        # XXX     self._resources[table][column] = value

    def get_data(self):
        try:
            data = self.__dict__.pop("data")
        except KeyError:
            try:
                loader = self.load
            except AttributeError:
                def loader(): None
            data = loader()
        self.data = data

    def delegate(self, handler, *args, shift_headings=1, **kwargs):
        # TODO uhhmmm...
        kwargs.update(shift_headings=shift_headings)
        return handler().get(self, *args, **kwargs)

    @classmethod
    def get(resource, parent, **kwargs):
        """"""
        header_shift = kwargs.pop("shift_headings", None)
        if "_data" in parent.__dict__:
            parent._data.update(kwargs.get("data", {}))
        parent.__dict__.pop("data", None)  # NOTE magic name "data" is reserved
        kwargs.update(parent.__dict__)
        try:
            handler = resource(**kwargs)
            handler.get_data()
            content = handler._get()
        except NotFound:
            return "not found"
        if header_shift:
            try:
                content._body = shift_headings(str(content), header_shift)
            except AttributeError:
                pass
        return content

    def __contains__(self, item):
        return item in dir(self)


# XXX class ResourceData(collections.OrderedDict):
# XXX
# XXX     def __missing__(self, key):
# XXX         self[key] = collections.OrderedDict()
# XXX         return self[key]


def get_app_db(identifier):
    """"""
    db = sql.db(f"web-{identifier}.db")
    db.define(job_signatures="""module TEXT, object TEXT, args BLOB,
                                kwargs BLOB, arghash TEXT,
                                UNIQUE(module, object, arghash)""",
              job_runs="""job_signature_id INTEGER,
                          job_id TEXT UNIQUE,
                          created DATETIME NOT NULL
                            DEFAULT(STRFTIME('%Y-%m-%d %H:%M:%f',
                                             'NOW')),
                          started DATETIME, finished DATETIME,
                          start_time REAL, run_time REAL,
                          status INTEGER, output TEXT""",
              job_schedules="""job_signature_id INTEGER, minute TEXT,
                               hour TEXT, day_of_month TEXT,
                               month TEXT, day_of_week TEXT,
                               UNIQUE(job_signature_id, minute,
                                      hour, day_of_month, month,
                                      day_of_week)""")
    return db


class Application:
    """
    A web application.

        >>> app = Application("example")
        >>> @app.wrap
        ... def contextualize(handler, app):
        ...     yield
        >>> @app.route(r"")
        ... class Greeting:
        ...     def _get(self):
        ...         return "hello world"
        >>> response = app.get(r"")
        >>> response[0]
        '200 OK'
        >>> response[2][0]
        b'hello world'

    """

    def __init__(self, name, *wrappers, db=True, host=None, static=None,
                 icon=None, serve=False, **path_args):
        self.name = name
        self.wrappers = []
        self.pre_wrappers = []
        self.post_wrappers = []
        self.add_wrappers(*wrappers)
        self.host = host
        self.path_args = {}
        self.add_path_args(**path_args)
        self.mounts = []
        self.routes = []  # TODO use ordered dict

        if db:
            self.db = get_app_db(name)
            self.cache = cache(db=self.db)

        class Database:
            def _get(innerself):
                return tx.db.tables

        self.route(r".data")(Database)
        self.add_path_args(table=r"\w+")

        class Table:
            def _get(innerself):
                return pprint.pformat([dict(r)
                                       for r in tx.db.select(innerself.table)])

        self.route(r".data/{table}")(Table)

        self.kv = kv.db(f"web-{name}", ":", {"queue": "list"})
        self.sys_kv = kv.db("system", ":", {"queue": "list"})
        if static:
            static_path = pkg_resources.resource_filename(static, "static")
            self.static_path = pathlib.Path(static_path)
        # for method in http.spec.request.methods[:5]:
        #     setattr(self, method, functools.partial(self.get_handler,
        #                                             method=method))
        # XXX try:
        # XXX     self.view = mm.templates(name, tx=tx)
        # XXX except ImportError:
        # XXX     try:
        # XXX         self.view = mm.templates(name + ".__web__", tx=tx)
        # XXX     except ImportError:
        # XXX         pass
        if icon:
            def insert_icon_rels(handler, app):
                yield
                if tx.response.status == "200 OK" and \
                   tx.response.headers.content_type == "text/html":
                    doc = parse(tx.response.body)
                    head = doc.select("head")[0]
                    head.append("<link rel=icon href=/icon.png>")
                    tx.response.body = doc.html
            self.wrap(insert_icon_rels, "post")

            if str(icon).endswith("="):  # TODO better test for b64
                payload = b64decode(icon)
            else:
                icon_path = pkg_resources.resource_filename(icon, "icon.png")
                payload = pathlib.Path(icon_path)

            class Icon:
                def _get(innerself):
                    header("Content-Type", "image/png")
                    try:
                        with payload.open("rb") as fp:
                            return fp.read()
                    except AttributeError:
                        return payload
            self.route(r"icon.png")(Icon)
            self.route(r"favicon.ico")(Icon)
        if serve:
            self.serve(serve)

    def serve(self, port, host="127.0.0.1"):
        # must be called from custom jupyter kernel/head of your program:
        # XXX from gevent import monkey
        # XXX monkey.patch_all()
        class Log:
            def write(logline):
                (_, _, _, _, _, method, path,
                 _, status, _, duration) = logline.split()
                method = method.lstrip('"')
                duration = round(float(duration) * 1000)
                message = (f"<div class=httplog>"
                           f"<span>{self.host}</span>"
                           f"<span>{method}</span>"
                           f"<span>{path}</span>"
                           f"<span>{status}</span>"
                           f"<span>{duration}<span>ms</span></span>"
                           f"</div>")
                print(message)
        server = gevent.pywsgi.WSGIServer((host, port), self, log=Log)
        server.serve_forever()
        # TODO self.server = gevent.spawn(server.serve_forever)
        # TODO self.server.spawn()  # TODO start()?

    def reload_config(self, path=None):
        self.cfg = {}
        path = os.getenv("WEBCFG", path)
        try:
            with pathlib.Path(path).open() as fp:
                self.cfg = json.load(fp)
        except (FileNotFoundError, TypeError):
            pass

    def add_wrappers(self, *wrappers):
        self.wrappers.extend(wrappers)

    def add_path_args(self, **path_args):
        self.path_args.update({k: v.replace(r"\!", nb60_re)
                               for k, v in path_args.items()})

    def get(self, path):
        """"""
        env = {'HTTP_REFERER': 'http://localhost:22739/',
               'HTTP_HOST': 'lahacker.net:22739',
               'HTTP_CONNECTION': 'keep-alive',
               'HTTP_ACCEPT': 'image/png,image/*;q=0.8,*/*;q=0.5',
               'HTTP_USER_AGENT': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; '
                                  'rv:21.0) Gecko/20100101 Firefox/21.0',
               'HTTP_COOKIE': 'session=99f81fd1f5e4c13b724043336f75'
                              'e81ee51d806979220cc8cebe51bc9d0de292',
               'HTTP_ACCEPT_LANGUAGE': 'en-US,en;q=0.5',
               'HTTP_ACCEPT_ENCODING': 'gzip, deflate',
               'PATH_INFO': path,
               'QUERY_STRING': '',
               'RAW_URI': '/',
               'REMOTE_ADDR': '127.0.0.1',
               'REMOTE_PORT': '44612',
               'REQUEST_METHOD': 'GET',
               'SCRIPT_NAME': '',
               'SERVER_PROTOCOL': 'HTTP/1.1',
               'SERVER_SOFTWARE': 'gunicorn/0.17.4',
               'SERVER_NAME': 'localhost',
               'SERVER_PORT': '22739',
               'wsgi.input': open("/dev/null"),
               'wsgi.url_scheme': 'http'}
        response = []

        def start_response(status, headers):
            response.append(status)
            response.append(headers)
        response.append(self(env, start_response))
        return tuple(response)

    def wrap(self, handler, when=None):
        """
        decorate a generator to run at various stages during the request

        """
        if when == "pre":
            self.pre_wrappers.append(handler)
        elif when == "post":
            self.post_wrappers.append(handler)
        else:
            self.wrappers.append(handler)
        return handler
        # def register(controller):
        #     path = path_template.format(**{k: "(?P<{}>{})".format(k, v) for
        #                                    k, v in self.path_args.items()})
        #     self.routes.append((path, controller))
        #     return controller
        # return register

    # @property
    # def resource(self):
    #     class Resource(type):
    #         def __new__(cls, name, bases, attrs):
    #             resource = type(name, bases, attrs)
    #           path = attrs["path"].format(**{k: "(?P<{}>{})".format(k, v) for
    #                                          k, v in self.path_args.items()})
    #             self.routes.append((path, resourcer))
    #             controller.__web__ = path
    #             return resource
    #     return Resource

    def route(self, path_template=None):
        """
        decorate a class to run when request path matches template

        """
        def register(controller):
            # TODO allow for reuse of parent_app's path_arg definitions
            # XXX try:
            # XXX     path_args = dict(self.parent_app.path_args,
            #                          **self.path_args)
            # XXX except AttributeError:
            # XXX     path_args = self.path_args
            templates = {k: "(?P<{}>{})".format(k, v) for
                         k, v in self.path_args.items()}
            try:
                path = path_template.format(**templates)
            except KeyError as err:
                raise KeyError("undefined URI fragment"
                               " type `{}`".format(err.args[0]))

            # TODO metaclass for `__repr__` -- see `app.routes`
            class Route(controller, Resource):

                __doc__ = controller.__doc__
                __web__ = path_template, templates
                handler = controller

            try:
                path = "/".join((self.prefix, path))
            except AttributeError:
                pass
            self.routes.append((path.strip("/"), Route))
            return Route
        return register

    def mount(self, *apps):
        """
        add an `application` to run when request path matches template

        """
        for app in apps:
            app.parent_app = self
            self.add_wrappers(*app.wrappers)  # TODO add pre and post wrappers
            path = app.mount_prefix.format(**{k: "(?P<{}>{})".format(k, v) for
                                              k, v in self.path_args.items()})
            self.mounts.append((path, app))

    def __repr__(self):
        return "<web.application: {}>".format(self.name)

    def __call__(self, environ, start_response):
        """The WSGI callable."""
        tx.request._contextualize(environ)
        tx.response._contextualize()
        path = tx.request.uri.path

        if path.startswith("static/"):
            asset_path = path.partition("/")[2]
            if asset_path.startswith((".", "/")):
                raise BadRequest("bad filename")
            asset = self.static_path / asset_path
            try:
                with asset.open() as fp:
                    content = fp.read()
            except FileNotFoundError:
                asset = pathlib.Path(__file__).parent / "static" / asset_path
                try:
                    with asset.open() as fp:
                        content = fp.read()
                except FileNotFoundError:
                    raise NotFound("file not found")
            content_types = {".css": "text/css",
                             ".js": "application/javascript"}
            # tx.response.headers.content_type = content_types[asset.suffix]
            header("Content-Type", content_types[asset.suffix])
            start_response("200 OK", tx.response.headers.wsgi)
            return [bytes(content, "utf-8")]

        try:
            tx.host._contextualize(self, tx.request.headers.host.name,
                                   tx.request.headers.host.port)
        except AttributeError:
            raise NotFound("no hostname provided")
        tx.user._contextualize(environ)
        tx.log._contextualize()
        tx.response.headers.content_type = "text/plain"
        # XXX tx.app_name = self.name
        response_hooks = []

        def exhaust_hooks():
            for hook in response_hooks:
                try:
                    next(hook)
                except StopIteration:
                    pass

        try:
            tx.request.controller = self.get_controller(path)
            tx.response.headers.x_powered_by = "understory"

            for hook in self.pre_wrappers + self.wrappers + self.post_wrappers:
                if not inspect.isgeneratorfunction(hook):
                    msg = "`{}.{}` is not an iterator, give it a yield"
                    modname = getattr(hook, "__module__", "??")
                    raise TypeError(msg.format(modname, hook.__name__))
                _hook = hook(tx.request.controller, self)
                next(_hook)
                response_hooks.append(_hook)

            method = tx.request.method
            tx.response.status = "200 OK"
            if method == "GET":
                forced_method = Form().get("_http_method")
                if forced_method:
                    method = forced_method.upper()
            tx.request.controller.get_data()
            body = self.get_handler(tx.request.controller, method)()
            if body is None:
                raise NoContent()
            if isinstance(body, tuple) and isinstance(body[0], dict):
                body = best_match(body[0], *body[1:])
            try:
                header("Content-Type", body.content_type)
            except AttributeError:
                pass
            tx.response.body = body
            exhaust_hooks()  # TODO see below to pull hook exhaustion out
        except Status as exc:
            tx.response.status = str(exc)  # TODO exc.status
            tx.response.body = exc.body
            if exc.code == "201":
                tx.response.headers.location = exc.location
            if exc.code in ("301", "302", "303", "307", "308"):
                redirect_uri = apply_dns(str(tx.response.body))
                if redirect_uri.startswith("/"):  # relative HTTP(S) URL
                    tx.response.headers.location = \
                        urllib.parse.quote(redirect_uri)
                else:  # anything else (moz-extension, etc..)
                    tx.response.headers.location = redirect_uri
            if exc.code == "405":
                tx.response.headers.allow = ", ".join(dict(exc.allowed))
        except Exception:
            # raise  # NOTE leave to bubble naturally -- debug in terminal
            tx.response.status = "500 Internal Server Error"
            if getattr(tx.user, "is_owner", False):
                body = config_templates.debug(*sys.exc_info())
            else:
                # TODO body = "Internal server error."
                body = config_templates.debug(*sys.exc_info())
                # TODO body = self.view.error.internal()
            tx.response.body = body
            # TODO logging
            # if os.environ["WWW_DEBUG"]:
            #     raise
        # exhaust_hooks()
        # try:
        #     # exhaust_hooks()
        #     pass
        # except:
        #     print("BREAK IN THE HOOK")  # TODO provide debug
        #     raise
        try:
            header("Content-Type", tx.response.body.content_type)
        except AttributeError:
            pass
        try:
            start_response(tx.response.status, tx.response.headers.wsgi)
        except OSError:  # websocket connection broken
            # TODO close websocket connection?
            return []
        if getattr(tx.response, "naked"):
            return tx.response.body
        elif isinstance(tx.response.body, bytes):
            return [tx.response.body]
        elif tx.response.headers.get("content-type") == "application/json":
            # XXX return [bytes(json.dumps(tx.response.body), "utf-8")]
            return [bytes(JSONEncoder().encode(tx.response.body), "utf-8")]
        return [bytes(str(tx.response.body), "utf-8")]

    # def __gevent_call__(self, environ, start_response):
    #     """gevent's WSGI callable."""
    #     tx.request._contextualize(environ)
    #     tx.response._contextualize()
    #     path = tx.request.uri.path
    #     controller = self.get_controller(path)
    #     if tx.request.headers.get("Subscribe") == "keep-alive":
    #         handler = controller._subscribe
    #     else:
    #         handler = controller._get
    #     start_response("200 OK", [("Content-Type", "application/json")])
    #     return handler()

    def get_controller(self, path):
        """

        """
        # TODO softcode `static/` reference
        if path.endswith("/") and not path.startswith("static/"):
            raise PermanentRedirect("/" + path.rstrip("/"))

        for mount, app in self.mounts:
            m = re.match(mount, path)
            if m:
                controller = app.get_controller(path[m.span()[1]:].lstrip("/"))
                for k, v in m.groupdict().items():
                    setattr(controller, k, v)
                return controller

        class ResourceNotFound(Resource):
            def _get(inner_self):
                raise NotFound("Resource not found")
                error = self.view.error
                # TODO recursively ascend app ancestors
                # try:
                #     error = self.parent_app.view.error
                # except AttributeError:
                #     error = self.parent_app.parent_app.view.error
                raise NotFound(error.resource_not_found())

        def get_resource():
            for pattern, resource in self.routes:
                if isinstance(resource, str):
                    mod = __import__(resource.__module__)
                    resource = getattr(mod, resource)
                match = re.match(r"^{}$".format(pattern),
                                 urllib.parse.unquote(path))
                if match:
                    return resource, match
            return ResourceNotFound, None

        resource, match = get_resource()  # TODO for-else or try-block instead?
        unquoted = {k: urllib.parse.unquote(v) for k, v
                    in match.groupdict().items() if v} if match else {}
        return resource(**unquoted)

    def get_handler(self, controller, method="get"):
        method = f"_{method.lower()}"
        try:
            return getattr(controller, method)
        except AttributeError:
            if method == "_head":
                try:
                    return getattr(controller, "_get")
                except AttributeError:
                    pass
            exc = MethodNotAllowed(self.view.error.method_not_allowed(method))
            exc.allowed = inspect.getmembers(controller, ismethod)
            raise exc


def sessions(**defaults):
    """
    returns an application hook for session handling using given redis `db`

    """
    def hook(handler, app):
        try:
            identifier = tx.request.headers["cookie"].morsels["session"]
        except KeyError:
            identifier = 0
        if ("sessions", identifier) not in kvdb:
            while True:
                secret = "{}{}{}{}".format(random.getrandbits(128),
                                           app.cfg["session"]["salt"],
                                           time.time(), tx.user.ip)
                secret_hash = hashlib.sha256(secret.encode("utf-8"))
                identifier = secret_hash.hexdigest()
                if kvdb["sessions", identifier].setnx("anonymous"):
                    break
        session_timeout = app.cfg["session"].get("timeout",
                                                 default_session_timeout)
        kvdb["sessions", identifier].expire(session_timeout)
        # FIXME user.session = kvdb.hgetall(kvdb(user.identifier, "data"))
        data = kvdb["sessions", identifier, "data"]
        if data:
            data = json.loads(str(data))
        else:
            data = Session(defaults)
        # XXX print(identifier, data)
        tx.user.session = data
        tx.user.identifier = identifier
        yield
        kvdb["sessions", identifier, "data"] = \
            JSONEncoder().encode(tx.user.session)
        kvdb["sessions", identifier, "data"].expire(session_timeout)
        # FIXME kvdb.delete("data")
        # FIXME if user.session:
        # FIXME     kvdb.hmset("data", **user.session)
        # XXX print(identifier, data, tx.user.identifier, tx.user.session)
        tx.response.headers["set-cookie"] = (("session", tx.user.identifier),)
        # ("Domain", tx.host.name))
    return hook


session_table_sql = """timestamp DATETIME NOT NULL
                           DEFAULT CURRENT_TIMESTAMP,
                       identifier TEXT NOT NULL UNIQUE,
                       data TEXT NOT NULL"""


def resume_session(handler, app):
    """."""
    # TODO monitor expiration (default_session_timeout)
    data = {}
    try:
        identifier = tx.request.headers["cookie"].morsels["session"]
    except KeyError:
        identifier = None
    else:
        try:
            session = tx.db.select("sessions", where="identifier = ?",
                                   vals=[identifier])[0]
        except IndexError:
            identifier = None
        else:
            try:
                data = json.loads(session["data"])
            except json.decoder.JSONDecodeError:
                identifier = None
    tx.user.session = data
    yield
    if tx.user.session:
        if identifier is None:
            salt = "abcdefg"  # FIXME
            secret = f"{random.getrandbits(64)}{salt}{time.time()}{tx.user.ip}"
            identifier = hashlib.sha256(secret.encode("utf-8")).hexdigest()
            tx.user.session.update(ip=tx.user.ip,
                                   ua=str(tx.request.headers["user-agent"]))
            # TODO FIXME add Secure for HTTPS sites (eg. canopy)!
            tx.response.headers["set-cookie"] = (("session", identifier),
                                                 ("path", "/"),
                                                 # "Secure",
                                                 "HttpOnly")
        tx.db.replace("sessions", identifier=identifier,
                      data=JSONEncoder().encode(tx.user.session))
    else:
        tx.response.headers["set-cookie"] = (("session", identifier),
                                             ("path", "/"), ("max-age", 0))


# TODO roles eg. owner, guest (personal context) && admin, user (service)
def require_auth(*roles):
    def decorate(func):
        def handler(*args, **kwargs):
            if tx.user.session["role"] not in roles:  # TODO role -> roles
                raise Unauthorized("no auth to access this resource")
            return func(*args, **kwargs)
        return handler
    return decorate


class Session(dict):

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            return super(Session, self).__getattr__(name)

    def __setattr__(self, name, value):
        self[name] = value


def run_redis(socket):
    sh.redis_server("--daemonize", "yes", "--unixsocket", socket, "--port", 0)


def kill_redis(socket):
    sh.redis_cli("-s", socket, "shutdown")


def enqueue(callable, *args, **kwargs):
    """
    append a function call to the end of the job queue

    """
    job_signature_id = get_job_signature(callable, *args, **kwargs)
    job_run_id = nbrandom(9)
    tx.app.db.insert("job_runs", job_signature_id=job_signature_id,
                     job_id=job_run_id)
    # TODO add a "seen" column
    tx.app.kv["jobqueue"].append(f"{tx.app.name}:{job_run_id}")


def get_job_signature(callable, *args, **kwargs):
    """
    return a job signature id creating a record if necessary

    """
    _module = callable.__module__
    _object = callable.__name__
    _args = json.dumps(args)
    _kwargs = json.dumps(kwargs)
    arghash = hashlib.sha256((_args + _kwargs).encode("utf-8")).hexdigest()
    try:
        job_signature_id = tx.db.insert("job_signatures", module=_module,
                                        object=_object, args=_args,
                                        kwargs=_kwargs, arghash=arghash)
    except tx.db.IntegrityError:
        job_signature_id = tx.db.select("job_signatures", what="rowid, *",
                                        where="""module = ? AND object = ? AND
                                                 arghash = ?""",
                                        vals=[_module, _object,
                                              arghash])[0]["rowid"]
    return job_signature_id
