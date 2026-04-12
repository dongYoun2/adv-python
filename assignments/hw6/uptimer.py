# uptimer_parallel.py

import requests
import logging
from threading import Thread
from multiprocessing import Pool


class WebsiteDownException(Exception):
    pass


def ping_website(address, timeout=20):
    try:
        response = requests.head(address, timeout=timeout)
        if response.status_code >= 400:
            logging.warning("Website %s returned status_code=%s",
                            address, response.status_code)
            raise WebsiteDownException()
    except requests.exceptions.RequestException:
        logging.warning("Timeout expired for website %s", address)
        raise WebsiteDownException()


def check_website(address):
    try:
        ping_website(address)
    except WebsiteDownException:
        print(f"The website {address} is down")


def _thread_worker(addresses):
    for addr in addresses:
        check_website(addr)


def run_threading(website_list, N=4):
    chunk_size = len(website_list) // N
    threads = []

    for i in range(N):
        start = i * chunk_size
        end = len(website_list) if i == N-1 else (i+1) * chunk_size
        chunk = website_list[start:end]

        t = Thread(target=_thread_worker, args=(chunk,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


def _mp_worker(address):
    check_website(address)


def run_multiprocessing(website_list, N=4):
    with Pool(N) as p:
        p.map(_mp_worker, website_list)