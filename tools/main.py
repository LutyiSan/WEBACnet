from get_ips import get_interfaces_ip
from server import run_server


def get_ip():
    try:
        return get_interfaces_ip()
    except Exception as e:
        print(e)


def runner():
    ips = get_ip()
    run_server(ips)


if __name__ == "__main__":
    runner()
