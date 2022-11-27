from get_ips import get_interfaces_ip
from server import run_server
from loguru import logger


def get_ip():
    try:
        return get_interfaces_ip()
    except Exception as e:
        logger.exception('Can not get interfaces', e)


def runner():
    ips = get_ip()
    run_server(ips)


if __name__ == "__main__":
    runner()
