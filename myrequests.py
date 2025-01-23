from requests import Session
from requests.adapters import HTTPAdapter, Retry


def session_get(url):
    with Session() as s:
        retries = Retry(total=5, backoff_factor=1)
        s.mount("https://", HTTPAdapter(max_retries=retries))
        r = s.get(url)

        return r.text


def session_post(url):
    data = {

    }

    with Session() as s:
        retries = Retry(total=5, backoff_factor=1)
        s.mount("https://", HTTPAdapter(max_retries=retries))
        r = s.post(url=url, data=data)

        return r.text