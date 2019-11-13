from requests import get
from requests.exceptions import RequestException
from contextlib import closing


def simple_get(url):
    try:
        with closing(get(url, stream=True)) as resp:
            print("Step1")
            if is_good_response(resp):
                print(resp)
                return resp.content
            else:
                print("Yalla! IT's bhanda")
                return None

    except RequestException as e_e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e_e))


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return None

def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

raw_html = simple_get('https://realpython.com/blog')
print(len(raw_html))