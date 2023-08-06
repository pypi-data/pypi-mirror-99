import os

from .tools import non_empty_value


def api_url() -> str: return os.environ.get('API_URL', 'https://api.hestia.earth')


def web_url() -> str: return os.environ.get('WEB_URL', 'https://www.hestia.earth')


def join_args(values) -> str: return '&'.join(list(filter(non_empty_value, values))).strip()


def request_url(base_url: str, **kwargs) -> str:
    args = list(map(lambda key: '='.join([key, str(kwargs.get(key))]) if kwargs.get(key) else None, kwargs.keys()))
    return '?'.join(list(filter(non_empty_value, [base_url, join_args(args)]))).strip()
