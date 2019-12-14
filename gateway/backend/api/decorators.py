from functools import wraps

class TokenHeader():
    __slots__ = ('function', 'cache', 't_label', 't_type', 'requester', 'id', 'secret')

    def __init__(self, requester, cache, app_id: str, app_secret: str, t_label: str = '<service>-token', t_type: str = 'Bearer'):

        self.requester = requester
        self.cache = cache

        self.id, self.secret = app_id, app_secret
        self.t_label, self.t_type = t_label, t_type

    def __get_token(self):
        return self.cache.get(self.t_label)

    def __set_token(self, new_token: str):
        return self.cache.set(self.t_label, new_token, None)

    def __request_new_token(self):
        json, code = self.requester.token(self.id, self.secret)

        if code == 200:
            self.__set_token(json['token'])


    def __request_header(self):
        token_ = self.__get_token()

        if token_ is not None:
            return {'Authorization': f'{self.t_type} {self.__get_token()}'}

        else:
            return {}

    def  __call__(self, wrapped_func):
        return self.decorate(wrapped_func)

    def decorate(self, function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            return self.call(function, *args, **kwargs)

        return wrapper

    def call(self, f, *args, **kwargs):
        token_ = self.__get_token()

        if token_ is not None:
            kwargs['headers'] = self.__request_header()
            json, code = f(*args, **kwargs)

            if code != 402:
                # token is valid
                return (json, code)


        # token expired or not set
        self.__request_new_token()
        kwargs['headers'] = self.__request_header()
        json, code = f(*args, **kwargs)
        return (json, code)