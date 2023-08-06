import threading
import requests

from xander.engine.xander import logger


def post(url, headers, payload):
    try:
        res = requests.post(url=url, json=payload, headers=headers)
    except Exception as e:
        logger.network(f'Connection error while calling {url} ({e})')
        return False, -1

    if int(res.status_code) == 200:
        # logger.debug("Response code: {} while calling {}".format(res.status_code, url))
        try:
            return True, res.json()
        except:
            return True, {'message': res.text}
    else:
        if logger:
            logger.network(message="Response code: {} while calling {}".format(res.status_code, url))
        return False, int(res.status_code)


def save_changes_on_cloud(url, headers, payload):
    """
    Run a thread that execute the call to cloud server through the client.
    @param client: Xander client object
    @param function: Xander client function
    @param args: argument of the function
    @return: True if the call has been executed, False otherwise.
    """

    download_thread = threading.Thread(target=post, name="Xander Client POST", args=(url, headers, payload))
    download_thread.start()

    return True


def update(url, headers=None, payload=None, asynchronous=True):
    if asynchronous:
        save_changes_on_cloud(url, headers, payload)
    else:
        return post(url, headers, payload)

    return True
