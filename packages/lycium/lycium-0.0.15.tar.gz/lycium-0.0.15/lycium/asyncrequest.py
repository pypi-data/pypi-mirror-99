#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import urllib
import http
import traceback
import tornado.httpclient
import tornado.gen
import tornado.escape
from tornado.ioloop import IOLoop
from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import Future, run_on_executor
import asyncio
import zeep
from .tornadozeep import TornadoAsyncTransport
from .exceptionreporter import ExceptionReporter

tornado.httpclient.AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")

logging.getLogger('tornado.curl_httpclient').setLevel(logging.WARN)
logging.getLogger('zeep.wsdl.wsdl').setLevel(logging.INFO)
logging.getLogger('zeep.xsd.schema').setLevel(logging.INFO)
logging.getLogger('zeep.transports').setLevel(logging.INFO)

LOG = logging.getLogger('async.request')

@tornado.gen.coroutine
def async_get(url, params=None, headers=None, verify_cert=True, **kwargs):
    response = yield async_http_request('GET', url, params, body=None, json=None, headers=headers, verify_cert=verify_cert, **kwargs)
    return response.code, response.body.decode()

@tornado.gen.coroutine
def async_get_bytes(url, params=None, headers=None, verify_cert=True, **kwargs):
    response = yield async_http_request('GET', url, params, body=None, json=None, headers=headers, verify_cert=verify_cert, **kwargs)
    return response.code, response.body

@tornado.gen.coroutine
def async_post(url, params=None, body='', json=None, headers=None, verify_cert=True, **kwargs):
    response = yield async_http_request('POST', url, params, body=body, json=json, headers=headers, verify_cert=verify_cert, **kwargs)
    return response.code, response.body.decode()

@tornado.gen.coroutine
def async_post_bytes(url, params=None, body='', json=None, headers=None, verify_cert=True, **kwargs):
    response = yield async_http_request('POST', url, params, body=body, json=json, headers=headers, verify_cert=verify_cert, **kwargs)
    return response.code, response.body

@tornado.gen.coroutine
def async_post_json(url, params=None, json=None, headers=None, verify_cert=True, **kwargs):
    response = yield async_http_request('POST', url, params, body=None, json=json, headers=headers, verify_cert=verify_cert, **kwargs)
    if response.code == http.HTTPStatus.OK:
        data = tornado.escape.json_decode(response.body.decode())
        return True, data
    res = str(response.reason) + ' ' + response.body.decode()
    return False, res

@tornado.gen.coroutine
def async_http_request(method, url, params=None, body='', json=None, headers=None, verify_cert=True, **kwargs):
    proxies = kwargs.pop('proxies', None)
    if params:
        qrs = [k + '=' + urllib.parse.quote(v) for k,v in params.items() ]
        sep = '&' if '?' in url else '?'
        url += sep + '&'.join(qrs)
    if json:
        body = tornado.escape.json_encode(json)
        if not headers:
            headers = {}
        headers['Content-Type'] = 'application/json'
    
    request = tornado.httpclient.HTTPRequest(url, method=method, body=body, headers=headers, validate_cert=verify_cert, **kwargs)
    client = tornado.httpclient.AsyncHTTPClient()
    prepare_request_proxies(request, proxies)
    
    response = yield client.fetch(request, raise_error=False)
    if response.code != http.HTTPStatus.OK:
        ExceptionReporter().report(key='HTTP-'+str(response.code), typ='HTTPQuery', 
            endpoint=url,
            method=method,
            inputs=body if body else tornado.escape.json_encode(params) if params else '',
            outputs=str(response.body.decode()),
            content=str(response.body.decode()),
            level='ERROR'
        )
    return response

def prepare_request_proxies(request, proxies):
    if proxies:
        if 'host' in proxies and 'port' in proxies:
            request.proxy_host = proxies.get('host')
            request.proxy_port = int(proxies.get('port'))
        else:
            schema = 'http'
            if request.url.startswith('https'):
                schema = 'https'
            if schema in proxies:
                part = proxies.get(schema)[len(schema)+3:]
                parts = part.split(':')
                request.proxy_host = parts[0]
                request.proxy_port = int(parts[1]) if len(parts) > 1 else (80 if schema == 'http' else 443)
        
class AsyncSoapExecutor():
    """
    """
    def __init__(self, ioloop = None):
        self.executor = ThreadPoolExecutor(max_workers=50)
        self.io_loop = ioloop or asyncio.new_event_loop()

    @run_on_executor
    def soap_request(self, future, endpoint, action, params, **kwargs) -> (str, str):
        proxies = kwargs.pop('proxies', None)
        transport = kwargs.pop('transport', None)
        uuid = kwargs.pop('uuid', None)
        err = ''
        context = ''
        try:
            web_client = zeep.Client(endpoint, transport=transport)
            soap_method = web_client.service[action]
            if isinstance(params, dict):
                context = soap_method(**params)
            elif isinstance(params, list):
                context = soap_method(*params)
            else:
                context = soap_method(params)
        except Exception as e:
            LOG.error(traceback.format_exc())
            err = str(e)
            ExceptionReporter().report(key='SOAP-'+str('failed'), typ='SOAPQuery', 
                endpoint=endpoint,
                method=str(action),
                inputs=str(params),
                outputs=str(context),
                content=err,
                level='ERROR'
            )
            # context = '{"code": -1, "message": %s}' % str(e)
        if future:
            future.set_result(context)
        # print('result', context)
        LOG.debug('%s %s %d response:\n%s', endpoint, action, uuid, context)
        return context, err

@tornado.gen.coroutine
def async_soap_request(endpoint, action, params, **kwargs) -> (str, str):
    # proxies = kwargs.pop('proxies', None)
    # transport = kwargs.pop('transport', None)
    # if transport is None:
    #     transport = TornadoAsyncTransport()
    # web_client = zeep.Client(endpoint, transport=transport)
    # soap_method = web_client.service[action]
    # context = soap_method(params)

    soap_executor = AsyncSoapExecutor()
    response, err = yield soap_executor.soap_request(None, endpoint, action, params, **kwargs)
    return response, err
    # future = Future()
    # # IOLoop.current().add_callback(_soap_request, future, endpoint, action, params, **kwargs)
    # return future
    # url = soap_client.location()
    # request = tornado.httpclient.HTTPRequest(url, method='POST', body=str(context.envelope), headers=context.client.headers(), **kwargs)
    # tornado_client = tornado.httpclient.AsyncHTTPClient()
    # prepare_request_proxies(request, proxies)
    # response = yield tornado_client.fetch(request)
    # print(response.body.decode())
    # # response_parser = SoapClient(web_client, action)
    # if response.code == http.HTTPStatus.OK:
    #     pass
    # else:
    #     ''
    # return response.code, response.body.decode()

def main():
    import tornado.web
    from tornado.ioloop import IOLoop

    routes = [
    ]

    class GeneralTornadoHandler(tornado.web.RequestHandler):
        """
        """

        def initialize(self, callback, methods):
            self.callbacks = {}
            if isinstance(methods, str):
                methods = [methods]
            for method in methods:
                method = method.upper()
                self.callbacks[method] = callback

        @tornado.gen.coroutine
        def get(self):
            yield self._do_callback(self.callbacks.get('GET'))

        @tornado.gen.coroutine
        def post(self):
            yield self._do_callback(self.callbacks.get('POST'))
        
        @tornado.gen.coroutine
        def _do_callback(self, cb):
            if callable(cb):
                response = yield cb(self, self.request)
                if isinstance(response, str):
                    self.write(response)
                    self.finish()
                else:
                    print("====== response", response)
                    pass
            else:
                print('not callable cb:', cb)

    def tornado_route(rule, **options):
        def decorator(f):
            # endpoint = options.pop('endpoint', None)
            # if not endpoint:
            #     endpoint = f.__name__

            routes.append((rule, GeneralTornadoHandler, dict(callback=f, methods=options.pop('methods', ['GET']))))
            return f
        return decorator

    app2 = tornado.web.Application(routes)
    app2.listen(8021)
    
    IOLoop.instance().start()

if __name__ == '__main__':
    main()
