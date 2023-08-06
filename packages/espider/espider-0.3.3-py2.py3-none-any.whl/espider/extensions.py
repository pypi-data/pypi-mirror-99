import json
import redis
from w3lib.url import canonicalize_url
from espider.utils.tools import get_md5


class RequestFilter(redis.client.Redis):
    __REDIS_KEYS__ = [
        'db', 'password', 'socket_timeout',
        'socket_connect_timeout',
        'socket_keepalive', 'socket_keepalive_options',
        'connection_pool', 'unix_socket_path',
        'encoding', 'encoding_errors',
        'charset', 'errors',
        'decode_responses', 'retry_on_timeout',
        'ssl', 'ssl_keyfile', 'ssl_certfile',
        'ssl_cert_reqs', 'ssl_ca_certs',
        'ssl_check_hostname',
        'max_connections', 'single_connection_client',
        'health_check_interval', 'client_name', 'username'
    ]

    def __init__(self, host='localhost', port=6379, set_key=None, timeout=None, **kwargs):
        self.redis_kwargs = {k: v for k, v in kwargs.items() if k in self.__REDIS_KEYS__}
        super().__init__(host=host, port=port, **self.redis_kwargs)

        self.set_key = set_key or 'urls'
        self.timeout = timeout

    def __call__(self, request, *args, **kwargs):
        skey = self.set_key

        if self.timeout:
            if self.exists(skey) and self.ttl(skey) == -1:
                self.expire(skey, self.timeout)

        kwargs = {
            'url': request.url,
            'method': request.method,
            'body': request.request_kwargs.get('data'),
            'json': request.request_kwargs.get('json')
        }
        code = self.sadd(skey, self._fingerprint(request))
        if not code:
            print(f'<RequestFilter Drop>: {json.dumps(kwargs)}')
        else:
            return request

    @staticmethod
    def _fingerprint(request):
        """
        request唯一表识
        @return:
        """
        url = request.url
        # url 归一化
        url = canonicalize_url(url)
        args = [url]

        for arg in ["params", "data", "files", "auth", "cert", "json"]:
            if request.requests_kwargs.get(arg):
                args.append(request.requests_kwargs.get(arg))

        return get_md5(*args)
