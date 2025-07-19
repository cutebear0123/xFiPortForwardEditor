import requests
import time
import re
import sys
import argparse


ip = "10.0.0.1"


def clear(token: str, cookie: str) -> None:
    while True:
        confirm = input("confirm [y/n]?")
        if confirm == "y":
            break
        if confirm != "n":
            return None
    for i in range(1, 256):
        print(i)
        res = requests.post(
            f"http://{ip}/actionHandler/ajax_port_forwarding.jst",
            data={"del": str(i), "csrfp_token": token},
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Cookie": cookie,
            },
        )
        print(f"{i}/256")


def setUFWDStatus(status: bool, token: str, cookie: str) -> str:
    res = requests.post(
        f"http://{ip}/actionHandler/ajax_port_forwarding.jst",
        data={"set": "true", "csrfp_token": token, "UFWDStatus": status},
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Cookie": cookie,
        },
    )
    return res.text


def add(data: dict, token: str, cookie: str) -> str:
    data["add"] = "true"
    data["csrfp_token"] = token
    data["ipv6addr"] = "x"
    data["startport"] = str(data["startport"])
    data["endport"] = str(data["endport"])
    res = requests.post(
        f"http://{ip}/actionHandler/ajax_port_forwarding.jst",
        data=data,
        headers={
            "Content-Type": "application/json",
            "Cookie": cookie,
        },
    )
    return res.text


def main():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest="command", required=True, help="commands")

    add_arg = subparsers.add_parser("add", help="add new port forward")
    add_arg.add_argument("name", help="name")
    add_arg.add_argument("type", type=str, help="type")
    add_arg.add_argument("ip", type=str, help="local ip of thing to add")
    add_arg.add_argument("port", type=str, help="port")
    subparsers.add_parser("clear", help="clear port forward")
    subparsers.add_parser("enable", help="enable port forward")
    subparsers.add_parser("disable", help="enable port forward")
    parser.add_argument("--username", required=True, help="Username for authentication")
    parser.add_argument("--password", required=True, help="Password for authentication")
    args = parser.parse_args()
    print(args)

    res = requests.post(
        f"http://{ip}/check.jst",
        data={"username": args.username, "password": args.password, "locale": False},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    cookie = res.headers["Set-Cookie"]
    m = re.search(r"csrfp_token=([a-zA-Z0-9]{10})", cookie)
    if not m:
        raise ValueError("wrong username or password or patched")
    token = m.group(1)
    print(cookie)

    if args.command == "add":
        local_ip_pattern = re.compile(
            r"^(10\.(?:[0-9]{1,3}\.){2}[0-9]{1,3})$"
            r"|"
            r"^(172\.(1[6-9]|2[0-9]|3[0-1])\.[0-9]{1,3}\.[0-9]{1,3})$"
            r"|"
            r"^(192\.168\.[0-9]{1,3}\.[0-9]{1,3})$"
        )
        if local_ip_pattern.match(args.ip) is None:
            raise ValueError("Invalid IP")
        if args.type.upper() not in {"TCP", "UDP", "TCP/UDP"}:
            raise ValueError("Invalid type")
        if int(args.port) < 1 or int(args.port) > 65535:
            raise ValueError("port not in range")
        data = {
            "name": args.name,
            "ip": args.ip,
            "type": args.type.upper(),
            "startport": args.port,
            "endport": args.port,
        }
        print(data)
        print(add(data, token, cookie))
        exit()
    elif args.command == "clear":
        clear(token, cookie)
    elif args.command == "enable":
        print(setUFWDStatus(True, token, cookie))
    elif args.command == "disable":
        print(setUFWDStatus(False, token, cookie))


if __name__ == "__main__":
    main()
