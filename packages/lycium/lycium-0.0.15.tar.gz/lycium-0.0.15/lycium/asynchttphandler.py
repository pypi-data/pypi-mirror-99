#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import http
import logging
import tornado.web
import tornado.gen
import tornado.escape
from .supports import singleton

LOG = logging.getLogger('tornadohandler')

@singleton
class AsyncRoutes():
    """
    """
    def __init__(self):
        self.routes = []

routes = AsyncRoutes()

class GeneralTornadoHandler(tornado.web.RequestHandler):
    """
    """

    def initialize(self, callback, methods, ac=[]):
        self.callbacks = {}
        self._ac = []
        if isinstance(methods, str):
            methods = [methods]
        for method in methods:
            method = method.upper()
            self.callbacks[method] = callback
        self.set_access_control(ac)

    def set_access_control(self, ac):
        self._ac = []
        if ac:
            if isinstance(ac, list):
                for f in ac:
                    if callable(f):
                        self._ac.append(['', f])
            elif isinstance(ac, dict):
                for k, f in ac:
                    if callable(f):
                        self._ac.append([k, f])
            elif callable(ac):
                self._ac.append(['', ac])

    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        yield self._do_callback(self.callbacks.get('GET'), *args, **kwargs)

    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        yield self._do_callback(self.callbacks.get('POST'), *args, **kwargs)
    
    @tornado.gen.coroutine
    def _do_callback(self, cb, *args, **kwargs):
        # LOG.debug(' - %s %s', self.request.host_name, self.request.uri)
        if callable(cb):
            is_reject = False
            reject_resson = ''
            for o in self._ac:
                f = o[1]
                if tornado.gen.is_coroutine_function(f):
                    ac_result, msg = yield f(self.request)
                else:
                    ac_result, msg = f(self.request)
                if not ac_result:
                    reject_resson = str(msg)
                    LOG.warning('verify %s access control %s failed with error:%s', self.request.path, str(o[0]), reject_resson)
                    is_reject = True
                    break
            if is_reject:
                self.write(reject_resson)
                self.set_status(http.HTTPStatus.FORBIDDEN)
                self.finish()
                return

            argsx = [self, self.request]
            for arg in args:
                argsx.append(arg)

            # fc = cb.__code__
            # if fc.co_name == 'wrapper':
            if tornado.gen.is_coroutine_function(cb):
                response = yield cb(*argsx, **kwargs)
            else:
                response = cb(*argsx, **kwargs)

            if isinstance(response, tuple):
                status_code = response[1]
                response = response[0]
                if status_code is not None:
                    self.set_status(status_code)

            if isinstance(response, str):
                self.write(response)
                self.finish()
            else:
                LOG.error("====== unknown response type:%s", str(response))
                if not self._finished:
                    self.finish()
        else:
            print('not callable cb:', cb)
            self.set_status(http.HTTPStatus.METHOD_NOT_ALLOWED)
            self.finish()

class PageNotFoundHandler(tornado.web.RequestHandler):
    def get(self):
        raise tornado.web.HTTPError(404)

def async_route(rule, **options):
    def decorator(f):
        # endpoint = options.pop('endpoint', None)
        # if not endpoint:
        #     endpoint = f.__name__
        ac = options.pop('ac', [])

        routes.routes.append((rule, GeneralTornadoHandler, dict(callback=f, methods=options.pop('methods', ['GET']), ac=ac)))
        return f
    return decorator

def args_as_dict(request):
    if hasattr(request, '_args_as_dict'):
        return getattr(request, '_args_as_dict')
    args = {}
    for k, v in request.arguments.items():
        if len(v) == 1:
            v0 = v[0]
            if isinstance(v0, bytes):
                v0 = v0.decode()
            args[k] = v0
        else:
            args[k] = v
    setattr(request, '_args_as_dict', args)
    return args

def request_body_as_json(request):
    if hasattr(request, '_body_as_json'):
        return getattr(request, '_body_as_json')
    params = {}
    try:
        params = tornado.escape.json_decode(request.body)
        if params is None:
            params = {}
    except Exception as e:
        LOG.error('parse request body:%s failed with error:%s', request.body.decode(), str(e))
    
    setattr(request, '_body_as_json', params)
    return params

def register_static_route(static_url_path=r'static', static_folder='static'):
    dst_static_folder = os.path.abspath(static_folder)
    routes.routes.append((static_url_path+r'/(.*)', tornado.web.StaticFileHandler, dict(path=dst_static_folder)))

def register_failover_route():
    routes.routes.append((r'.*', PageNotFoundHandler))

def check_post_params(params, must_list, must_type=None, is_or=False):
    if not isinstance(must_list, list):
        return True
    if is_or:
        for field in must_list:
            if field in params:
                return True
        return "lack %s" % ','.join(must_list)
    if isinstance(params, list):
        for p in params:
            p_result = check_post_params(p, must_list)
            if isinstance(p_result, str):
                return p_result
    if isinstance(params, dict):
        for attr in must_list:
            if attr not in params:
                return 'lack %s' % attr
    if must_type and isinstance(must_type, dict):
        for k, v in must_type.items():
            if not isinstance(params.get(k), v):
                return "%s type error, need %s" % (k, str(v))
    return True
